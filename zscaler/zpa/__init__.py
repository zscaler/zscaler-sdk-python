import logging
import os
import time
import urllib.parse
import uuid
from time import sleep

import requests
from box import BoxList

from zscaler import __version__
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.constants import ZPA_BASE_URLS
from zscaler.errors.http_error import HTTPError, ZscalerAPIError
from zscaler.exceptions.exceptions import HTTPException, ZscalerAPIException
from zscaler.logger import setup_logging
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import (
    convert_keys_to_snake,
    dump_request,
    dump_response,
    format_json_response,
    is_token_expired,
    retry_with_backoff,
    snake_to_camel,
)
from zscaler.zpa.app_segments import ApplicationSegmentAPI
from zscaler.zpa.app_segments_inspection import AppSegmentsInspectionAPI
from zscaler.zpa.app_segments_pra import AppSegmentsPRAAPI
from zscaler.zpa.certificates import CertificatesAPI
from zscaler.zpa.client import ZPAClient
from zscaler.zpa.cloud_connector_groups import CloudConnectorGroupsAPI
from zscaler.zpa.connectors import AppConnectorControllerAPI
from zscaler.zpa.emergency_access import EmergencyAccessAPI
from zscaler.zpa.idp import IDPControllerAPI
from zscaler.zpa.inspection import InspectionControllerAPI
from zscaler.zpa.isolation_profile import IsolationProfileAPI
from zscaler.zpa.lss import LSSConfigControllerAPI
from zscaler.zpa.machine_groups import MachineGroupsAPI
from zscaler.zpa.policies import PolicySetsAPI
from zscaler.zpa.posture_profiles import PostureProfilesAPI
from zscaler.zpa.privileged_remote_access import PrivilegedRemoteAccessAPI
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
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class ZPAClientHelper(ZPAClient):
    """A Controller to access Endpoints in the Zscaler Private Access (ZPA) API.

    The ZPA object stores the session token and simplifies access to API interfaces within ZPA.

    Attributes:
        client_id (str): The ZPA API client ID generated from the ZPA console.
        client_secret (str): The ZPA API client secret generated from the ZPA console.
        customer_id (str): The ZPA tenant ID found in the Administration > Company menu in the ZPA console.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are:

            * ``production``
            * ``beta``
            * ``gov``
            * ``govus``
            * ``zpatwo``
    """

    def __init__(
        self,
        client_id,
        client_secret,
        customer_id,
        cloud,
        timeout=240,
        cache=None,
        fail_safe=False,
    ):
        # Initialize rate limiter
        # You may want to adjust these parameters as per your rate limit configuration
        self.rate_limiter = RateLimiter(
            get_limit=20,  # Adjusted to allow 20 GET requests per 10 seconds
            post_put_delete_limit=10,  # Adjusted to allow 10 POST/PUT/DELETE requests per 10 seconds
            get_freq=10,  # Adjust frequency to 10 seconds
            post_put_delete_freq=10,  # Adjust frequency to 10 seconds
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
                self.cache = ZscalerCache(ttl=ttl, tti=tti)
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

        url = f"{api}/{path.lstrip('/')}"
        start_time = time.time()
        # Update headers to include the user agent
        headers_with_user_agent = self.headers.copy()
        headers_with_user_agent["User-Agent"] = self.user_agent
        # Generate a unique UUID for this request
        request_uuid = uuid.uuid4()
        dump_request(logger, url, method, json, params, headers_with_user_agent, request_uuid)
        # Check cache before sending request
        cache_key = self.cache.create_key(url, params)
        if method == "GET" and self.cache.contains(cache_key):
            resp = self.cache.get(cache_key)
            dump_response(
                logger=logger,
                url=url,
                method=method,
                params=params,
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
                    logger.warning("The provided or fetched token was already expired. Refreshing...")
                    self.refreshToken()
                resp = requests.request(
                    method,
                    url,
                    json=json,
                    headers=headers_with_user_agent,
                    timeout=self.timeout,
                )
                dump_response(
                    logger=logger,
                    url=url,
                    params=params,
                    method=method,
                    resp=resp,
                    request_uuid=request_uuid,
                    start_time=start_time,
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
                error = ZscalerAPIError(url, resp, response_data)
                if self.fail_safe:
                    raise ZscalerAPIException(response_data)
            except ZscalerAPIException:
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

    def get_paginated_data(
        self,
        path=None,
        params=None,
        expected_status_code=200,
        api_version: str = None,
        search=None,
        search_field="name",
        max_pages=None,
        max_items=None,
        sort_order=None,
        sort_by=None,
        sort_dir=None,
        start_time=None,
        end_time=None,
        idp_group_id=None,
        scim_user_id=None,
        page=None,
        pagesize=20,
    ):
        """
        Fetches paginated data from the ZPA API based on specified parameters and handles various types of API pagination.

        Args:
            path (str): The API endpoint path to send requests to.
            params (dict): Initial set of query parameters for the API request.
            expected_status_code (int): The expected HTTP status code for a successful request. Defaults to 200.
            api_version (str): Specifies the version of the API to be used. Helps in routing within the API service.
            search (str): Search query to filter the results based on specific conditions.
            search_field (str): The field name against which to search the query. Default is "name".
            max_pages (int): The maximum number of pages to fetch. If None, fetches all available pages.
            max_items (int): The maximum number of items to fetch across all pages. Stops fetching once reached.
            sort_order (str): Specifies the order of sorting (e.g., 'ASC' or 'DSC').
            sort_by (str): Specifies the field name by which the results should be sorted.
            sort_dir (str): Specifies the direction of sorting. Supported values: ASC, DESC.
            start_time (str): The start of a time range for filtering data based on modification time.
            end_time (str): The end of a time range for filtering data based on modification time.
            idp_group_id (str): Identifier for a specific IDP group, used for fetching data related to that group.
            scim_user_id (str): Identifier for a specific SCIM user, used for fetching data related to that user.
            page (int): Specific page number to fetch. Overrides automatic pagination.
            pagesize (int): Number of items per page, default is 20 as per API specification, maximum is 500.

        Returns:
            tuple: A tuple containing:
                - BoxList: A list of fetched items wrapped in a BoxList for easy access.
                - str: An error message if any occurred during the data fetching process.

        Raises:
            Logs errors and warnings through the configured logger when requests fail or if no data is found.
        """
        logger = logging.getLogger(__name__)

        ERROR_MESSAGES = {
            "UNEXPECTED_STATUS": "Unexpected status code {status_code} received for page {page}.",
            "MISSING_DATA_KEY": "The key 'list' was not found in the response for page {page}.",
            "EMPTY_RESULTS": "No results found for all requested pages.",
        }

        if params is None:
            params = {}

        if (page is not None or pagesize != 20) and (max_pages is not None or max_items is not None):
            raise ValueError(
                "Do not mix 'page' or 'pagesize' with 'max_pages' or 'max_items'. Choose either set of parameters."
            )

        params["pagesize"] = min(pagesize, 500)  # Apply maximum constraint and handle default

        if page:
            params["page"] = page

        if search:
            api_search_field = snake_to_camel(search_field)
            params["search"] = f"{api_search_field} EQ {search}"
        if sort_order:
            params["sortOrder"] = sort_order
        if sort_by:
            params["sortBy"] = sort_by
        if sort_dir:
            params["sortdir"] = sort_dir
        if start_time and end_time:
            params["startTime"] = start_time
            params["endTime"] = end_time
        if idp_group_id:
            params["idpGroupId"] = idp_group_id
        if scim_user_id:
            params["scimUserId"] = scim_user_id

        total_collected = 0
        ret_data = []

        try:
            while True:
                if max_pages is not None and (page is not None and page > max_pages):
                    break

                should_wait, delay = self.rate_limiter.wait("GET")
                if should_wait:
                    time.sleep(delay)

                url = f"{path}?{urllib.parse.urlencode(params)}"
                response = self.send("GET", url, api_version=api_version)

                if response.status_code != expected_status_code:
                    error_msg = ERROR_MESSAGES["UNEXPECTED_STATUS"].format(status_code=response.status_code, page=page)
                    logger.error(error_msg)
                    return BoxList([]), error_msg

                response_data = response.json()
                data = response_data.get("list", [])
                if not data and (page is None or page == 1):
                    error_msg = ERROR_MESSAGES["EMPTY_RESULTS"]
                    logger.warn(error_msg)
                    return BoxList([]), error_msg

                data = convert_keys_to_snake(data)
                ret_data.extend(data[: max_items - total_collected] if max_items is not None else data)
                total_collected += len(data)

                if max_items is not None and total_collected >= max_items:
                    break

                nextPage = response_data.get("nextPage")
                if not nextPage or (max_pages is not None and page >= max_pages):
                    break

                page = nextPage if page is None else page + 1
                params["page"] = page

        finally:
            time.sleep(1)  # Ensure a delay between requests regardless of outcome

        if not ret_data:
            error_msg = ERROR_MESSAGES["EMPTY_RESULTS"]
            logger.warn(error_msg)
            return BoxList([]), error_msg

        return BoxList(ret_data), None

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
    def isolation_profile(self):
        """
        The interface object for the :ref:`ZPA Isolation Profiles <zpa-isolation_profile>`.

        """
        return IsolationProfileAPI(self)

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
    def emergency_access(self):
        """
        The interface object for the :ref:`ZPA Emergency Access interface <zpa-emergency_access>`.

        """
        return EmergencyAccessAPI(self)

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
    def privileged_remote_access(self):
        """
        The interface object for the :ref:`ZPA Privileged Remote Access interface <zpa-privileged_remote_access>`.

        """
        return PrivilegedRemoteAccessAPI(self)

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
