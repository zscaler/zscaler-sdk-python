import json
import logging
import os
import time
import urllib.parse
from time import sleep
import uuid
import requests
from box import BoxList

from zscaler.cache.no_op_cache import NoOpCache
from zscaler.zpa.errors import ZpaAPIError, ZpaAPIException, HTTPError, HTTPException
from zscaler.cache.zscaler_cache import ZPACache
from zscaler.constants import ZPA_BASE_URLS
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import (
    convert_keys_to_snake,
    format_json_response,
    is_token_expired,
    retry_with_backoff,
    dump_request,
    dump_response,
)
from zscaler.zpa.client import ZPAClient
from zscaler.zpa.app_segments import ApplicationSegmentAPI
from zscaler.zpa.app_segments_inspection import AppSegmentsInspectionAPI
from zscaler.zpa.app_segments_pra import AppSegmentsPRAAPI
from zscaler.zpa.certificates import CertificatesAPI
from zscaler.zpa.client_types import ClientTypesAPI
from zscaler.zpa.cbi_profile import CBIProfileAPIControllerAPI
from zscaler.zpa.cloud_connector_groups import CloudConnectorGroupsAPI
from zscaler.zpa.connectors import AppConnectorControllerAPI
from zscaler.zpa.idp import IDPControllerAPI
from zscaler.zpa.inspection import InspectionControllerAPI
from zscaler.zpa.isolation_profile import IsolationProfileAPI
from zscaler.zpa.lss import LSSConfigControllerAPI
from zscaler.zpa.machine_groups import MachineGroupsAPI
from zscaler.zpa.platforms import PlatformsAPI
from zscaler.zpa.policies import PolicySetsAPI
from zscaler.zpa.posture_profile import PostureProfilesAPI
from zscaler.zpa.provisioning import ProvisioningKeyAPI
from zscaler.zpa.saml_attributes import SAMLAttributesAPI
from zscaler.zpa.scim_attributes import ScimAttributeHeaderAPI
from zscaler.zpa.scim_groups import SCIMGroupsAPI
from zscaler.zpa.segment_groups import SegmentGroupsAPI
from zscaler.zpa.server_groups import ServerGroupsAPI
from zscaler.zpa.servers import AppServersAPI
from zscaler.zpa.service_edges import ServiceEdgesAPI
from zscaler.zpa.trusted_networks import TrustedNetworksAPI

# Setup the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ZPAClientHelper(ZPAClient):
    """
    Client helper for ZPA operations.

    Attributes:
    - client_id (str): The client ID.
    - client_secret (str): The client secret.
    - customer_id (str): The customer ID.
    - cloud (str): The cloud endpoint to be used.
    - timeout (int): Request timeout duration in seconds.
    - cache (object): Cache object to be used.
    - baseurl (str): Base URL for API requests.
    - access_token (str): Access token for API requests.
    - headers (dict): Headers for API requests.
    """

    def __init__(self, client_id, client_secret, customer_id, cloud, timeout=240, cache=None, fail_safe=False):
        """
        Initialize ZPAClientHelper.

        Parameters:
        - client_id (str): The client ID.
        - client_secret (str): The client secret.
        - customer_id (str): The customer ID.
        - cloud (str): The cloud endpoint to be used.
        - cache (object, optional): Cache object. Defaults to None.
        - fail_safe (bool, optional): Log an error and continue on failure. Defaults to False.
        """

        # Initialize rate limiter
        # You may want to adjust these parameters as per your rate limit configuration
        self.rate_limiter = RateLimiter(
            get_limit=10,  # Adjust as per actual limit
            post_put_delete_limit=5,  # Adjust as per actual limit
            get_freq=1,  # Adjust as per actual frequency (in seconds)
            post_put_delete_freq=1,  # Adjust as per actual frequency (in seconds)
        )

        # Validate cloud value
        if cloud not in ZPA_BASE_URLS:
            valid_clouds = ", ".join(ZPA_BASE_URLS.keys())
            raise ValueError(
                f"The provided ZPA_CLOUD value '{cloud}' is not supported. "
                f"Please use one of the following supported values: {valid_clouds}"
            )

        # Continue with existing initialization...
        # Select the appropriate URL
        self.baseurl = ZPA_BASE_URLS.get(cloud, ZPA_BASE_URLS["PRODUCTION"])

        self.timeout = timeout
        self.client_id = client_id
        self.client_secret = client_secret
        self.customer_id = customer_id
        self.cloud = cloud
        self.url = f"{self.baseurl}/mgmtconfig/v1/admin/customers/{customer_id}"
        self.user_config_url = f"{self.baseurl}/userconfig/v1/customers/{customer_id}"
        self.v2_url = f"{self.baseurl}/mgmtconfig/v2/admin/customers/{customer_id}"
        self.cbi_url = f"{self.baseurl}/cbiconfig/cbi/api/customers/{customer_id}"
        self.fail_safe = fail_safe
        # Cache setup
        cache_enabled = os.environ.get("ZSCALER_CLIENT_CACHE_ENABLED", "true").lower() == "true"
        if cache is None:
            if cache_enabled:
                ttl = int(os.environ.get("ZSCALER_CLIENT_CACHE_DEFAULT_TTL", 3600))
                tti = int(os.environ.get("ZSCALER_CLIENT_CACHE_DEFAULT_TTI", 1800))
                self.cache = ZPACache(ttl=ttl, tti=tti)
            else:
                self.cache = NoOpCache()
        else:
            self.cache = cache

        # Initialize user-agent
        ua = UserAgent()
        self.user_agent = ua.get_user_agent_string()
        self.refreshToken()

    def refreshToken(self):
        # login
        response = self.login()
        if response is None or response.status_code > 299 or not response.json():
            logger.error("Failed to login using provided credentials, response: %s", response)
            raise Exception("Failed to login using provided credentials.")
        self.access_token = response.json().get("access_token")
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": self.user_agent,
        }

    @retry_with_backoff(retries=5)
    def login(self):
        """Log in to the ZPA API and set the access token for subsequent requests."""
        data = urllib.parse.urlencode({"client_id": self.client_id, "client_secret": self.client_secret})
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        try:
            url = f"{self.baseurl}/signin"
            resp = requests.post(url, data=data, headers=headers, timeout=self.timeout)
            # Avoid logging all data from the response, focus on the status and a summary instead
            logger.info("Login attempt with status: %d", resp.status_code)
            return resp
        except Exception as e:
            logger.error("Login failed due to an exception: %s", str(e))
            return None

    def send(self, method, path, json=None, params=None, api_version: str = None):
        """
        Send a request to the ZPA API.

        Parameters:
        - method (str): The HTTP method.
        - path (str): API endpoint path.
        - json (dict, optional): Request payload. Defaults to None.
        Returns:
        - Response: Response object from the request.
        """
        api = self.url
        if api_version is None:
            api = self.url
        elif api_version == "v2":
            api = self.v2_url
        elif api_version == "userconfig_v1":
            api = self.user_config_url
        elif api_version == "cbiconfig_v1":
            api = self.cbi_url

        url = f"{api}/{path.lstrip('/')}"
        start_time = time.time()
        # Update headers to include the user agent
        headers_with_user_agent = self.headers.copy()
        headers_with_user_agent["User-Agent"] = self.user_agent
        # Generate a unique UUID for this request
        request_uuid = uuid.uuid4()
        dump_request(logger, url, method, json, headers_with_user_agent, request_uuid)
        # Check cache before sending request
        cache_key = self.cache.create_key(url)
        if method == "GET" and self.cache.contains(cache_key):
            resp = self.cache.get(cache_key)
            dump_response(
                logger=logger,
                url=url,
                method=method,
                resp=resp,
                request_uuid=request_uuid,
                start_time=start_time,
                from_cache=True,
            )
            return resp

        attempts = 0
        while attempts < 5:  # Trying a maximum of 5 times
            try:
                # If the token is None or expired, fetch a new token
                if is_token_expired(self.access_token):
                    self.logger.warning("The provided or fetched token was already expired. Refreshing...")
                    self.refreshToken()
                resp = requests.request(method, url, json=json, headers=headers_with_user_agent, timeout=self.timeout)
                dump_response(
                    logger=logger, url=url, method=method, resp=resp, request_uuid=request_uuid, start_time=start_time
                )
                if resp.status_code == 429:  # HTTP Status code 429 indicates "Too Many Requests"
                    sleep_time = int(
                        resp.headers.get("Retry-After", 2)
                    )  # Default to 60 seconds if 'Retry-After' header is missing
                    logger.warning(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
                    sleep(sleep_time)
                    attempts += 1
                    continue
                else:
                    break
            except requests.RequestException as e:
                if attempts == 4:  # If it's the last attempt, raise the exception
                    logger.error(f"Failed to send {method} request to {url} after 5 attempts. Error: {str(e)}")
                    raise e
                else:
                    logger.warning(f"Failed to send {method} request to {url}. Retrying... Error: {str(e)}")
                    attempts += 1
                    sleep(5)  # Sleep for 5 seconds before retrying

        # If Non-GET call, clear the
        if method != "GET":
            self.cache.delete(cache_key)

        # Detailed logging for request and response
        try:
            response_data = resp.json()
        except ValueError:  # Using ValueError for JSON decoding errors
            response_data = resp.text
        # check if call was succesful
        if 200 > resp.status_code or resp.status_code > 299:
            # create errors
            try:
                error = ZpaAPIError(url, resp, response_data)
                if self.fail_safe:
                    raise ZpaAPIException(response_data)
            except ZpaAPIException:
                raise
            except Exception:
                error = HTTPError(url, resp, response_data)
                if self.fail_safe:
                    logger.error(response_data)
                    raise HTTPException(response_data)
            logger.error(error)
        # Cache the response if it's a successful GET request
        if method == "GET" and resp.status_code == 200:
            self.cache.add(cache_key, resp)
        return resp

    def get(self, path, json=None, params=None, api_version: str = None):
        """
        Send a GET request to the ZPA API.

        Parameters:
        - path (str): API endpoint path.
        - data (dict, optional): Request payload. Defaults to None.
        Returns:
        - Response: Response object from the request.
        """

        # Use rate limiter before making a request
        should_wait, delay = self.rate_limiter.wait("GET")
        if should_wait:
            time.sleep(delay)

        # Now proceed with sending the request
        resp = self.send("GET", path, json, params, api_version=api_version)
        formatted_resp = format_json_response(resp, box_attrs=dict())
        return formatted_resp

    def put(self, path, json=None, params=None, api_version: str = None):
        should_wait, delay = self.rate_limiter.wait("PUT")
        if should_wait:
            time.sleep(delay)
        resp = self.send("PUT", path, json, params, api_version=api_version)
        formatted_resp = format_json_response(resp, box_attrs=dict())
        return formatted_resp

    def post(self, path, json=None, params=None, api_version: str = None):
        should_wait, delay = self.rate_limiter.wait("POST")
        if should_wait:
            time.sleep(delay)
        resp = self.send("POST", path, json, params, api_version=api_version)
        formatted_resp = format_json_response(resp, box_attrs=dict())
        return formatted_resp

    def delete(self, path, json=None, params=None, api_version: str = None):
        should_wait, delay = self.rate_limiter.wait("DELETE")
        if should_wait:
            time.sleep(delay)
        return self.send("DELETE", path, json, params, api_version=api_version)

    ERROR_MESSAGES = {
        "UNEXPECTED_STATUS": "Unexpected status code {status_code} received for page {page}.",
        "MISSING_DATA_KEY": "The key '{data_key_name}' was not found in the response for page {page}.",
        "EMPTY_RESULTS": "No results found for page {page}.",
    }

    def get_paginated_data(
        self, path=None, data_key_name=None, data_per_page=500, expected_status_code=200, api_version: str = None
    ):
        """
        Fetch paginated data from the ZPA API.
        ...

        Returns:
        - list: List of fetched items.
        - str: Error message, if any occurred.
        """

        page = 1
        ret_data = []
        error_message = None

        while True:
            required_url = f"{path}?page={page}&pagesize={data_per_page}"
            should_wait, delay = self.rate_limiter.wait("GET")
            if should_wait:
                time.sleep(delay)

            # Now proceed with sending the request
            response = self.send("GET", required_url, api_version=api_version)

            if response.status_code != expected_status_code:
                error_message = self.ERROR_MESSAGES["UNEXPECTED_STATUS"].format(status_code=response.status_code, page=page)
                logger.error(error_message)
                break

            data = response.json().get(data_key_name)

            if data is None:
                error_message = self.ERROR_MESSAGES["MISSING_DATA_KEY"].format(data_key_name=data_key_name, page=page)
                logger.error(error_message)
                break

            if not data:  # Checks for empty data
                logger.info(self.ERROR_MESSAGES["EMPTY_RESULTS"].format(page=page))
                break

            ret_data.extend(convert_keys_to_snake(data))

            # Check for more pages
            if response.json().get("totalPages") is None or int(response.json().get("totalPages")) <= page + 1:
                break

            page += 1

        return BoxList(ret_data), error_message

    @property
    def app_segments(self):
        """
        The interface object for the :ref:`ZPA Application Segments interface <zpa-app_segments>`.

        """
        return ApplicationSegmentAPI(self)

    @property
    def app_segments_pra(self):
        """
        The interface object for the :ref:`ZPA Application Segments PRA interface <zpa-app_segments_pra>`.

        """
        return AppSegmentsPRAAPI(self)

    @property
    def app_segments_inspection(self):
        """
        The interface object for the :ref:`ZPA Application Segments PRA interface <zpa-app_segments_inspection>`.

        """
        return AppSegmentsInspectionAPI(self)

    @property
    def certificates(self):
        """
        The interface object for the :ref:`ZPA Browser Access Certificates interface <zpa-certificates>`.

        """
        return CertificatesAPI(self)

    @property
    def platforms(self):
        """
        The interface object for the :ref:`ZPA Access Policy platform interface <zpa-platforms>`.

        """
        return PlatformsAPI(self)

    @property
    def client_types(self):
        """
        The interface object for the :ref:`ZPA Access Policy client types interface <zpa-client_types>`.

        """
        return ClientTypesAPI(self)

    @property
    def isolation_profile(self):
        """
        The interface object for the :ref:`ZPA Isolation Profiles <zpa-isolation_profile>`.

        """
        return IsolationProfileAPI(self)

    @property
    def cbi_profile(self):
        """
        The interface object for the :ref:`ZPA Cloud Browser Isolation External Profile interface <zpa-cbi_profile>`.

        """
        return CBIProfileAPIControllerAPI(self)

    @property
    def cloud_connector_groups(self):
        """
        The interface object for the :ref:`ZPA Cloud Connector Groups interface <zpa-cloud_connector_groups>`.

        """
        return CloudConnectorGroupsAPI(self)

    @property
    def connectors(self):
        """
        The interface object for the :ref:`ZPA Connectors interface <zpa-connectors>`.

        """
        return AppConnectorControllerAPI(self)

    @property
    def idp(self):
        """
        The interface object for the :ref:`ZPA IDP interface <zpa-idp>`.

        """
        return IDPControllerAPI(self)

    @property
    def inspection(self):
        """
        The interface object for the :ref:`ZPA Inspection interface <zpa-inspection>`.

        """
        return InspectionControllerAPI(self)

    @property
    def lss(self):
        """
        The interface object for the :ref:`ZIA Log Streaming Service Config interface <zpa-lss>`.

        """
        return LSSConfigControllerAPI(self)

    @property
    def machine_groups(self):
        """
        The interface object for the :ref:`ZPA Machine Groups interface <zpa-machine_groups>`.

        """
        return MachineGroupsAPI(self)

    @property
    def policies(self):
        """
        The interface object for the :ref:`ZPA Policy Sets interface <zpa-policies>`.

        """
        return PolicySetsAPI(self)

    @property
    def posture_profiles(self):
        """
        The interface object for the :ref:`ZPA Posture Profiles interface <zpa-posture_profiles>`.

        """
        return PostureProfilesAPI(self)

    @property
    def provisioning(self):
        """
        The interface object for the :ref:`ZPA Provisioning interface <zpa-provisioning>`.

        """
        return ProvisioningKeyAPI(self)

    @property
    def saml_attributes(self):
        """
        The interface object for the :ref:`ZPA SAML Attributes interface <zpa-saml_attributes>`.

        """
        return SAMLAttributesAPI(self)

    @property
    def scim_attributes(self):
        """
        The interface object for the :ref:`ZPA SCIM Attributes interface <zpa-scim_attributes>`.

        """
        return ScimAttributeHeaderAPI(self)

    @property
    def scim_groups(self):
        """
        The interface object for the :ref:`ZPA SCIM Groups interface <zpa-scim_groups>`.

        """
        return SCIMGroupsAPI(self)

    @property
    def segment_groups(self):
        """
        The interface object for the :ref:`ZPA Segment Groups interface <zpa-segment_groups>`.

        """
        return SegmentGroupsAPI(self)

    @property
    def server_groups(self):
        """
        The interface object for the :ref:`ZPA Server Groups interface <zpa-server_groups>`.

        """
        return ServerGroupsAPI(self)

    @property
    def servers(self):
        """
        The interface object for the :ref:`ZPA Application Servers interface <zpa-app_servers>`.

        """
        return AppServersAPI(self)

    @property
    def service_edges(self):
        """
        The interface object for the :ref:`ZPA Service Edges interface <zpa-service_edges>`.

        """
        return ServiceEdgesAPI(self)

    @property
    def trusted_networks(self):
        """
        The interface object for the :ref:`ZPA Trusted Networks interface <zpa-trusted_networks>`.

        """
        return TrustedNetworksAPI(self)
