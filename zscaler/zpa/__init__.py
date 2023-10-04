# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Zscaler SDK for Python

The zscaler-sdk-python library is a SDK framework for interacting with
Zscaler Private Access (ZPA) and Zscaler Internet Access (ZIA)

Documentation available at https://zscaler-sdk-python.readthedocs.io

"""

__author__ = "Zscaler Inc."
__email__ = "zscaler-partner-labs@z-bd.com"
__version__ = "1.0.0"

import logging
import os
import time

from restfly.session import APISession, Session

from zscaler import __version__
from zscaler.constants import (
    BACKOFF_BASE_DURATION,
    BACKOFF_FACTOR,
    MAX_RETRIES,
    RETRIABLE_STATUS_CODES,
    ZPA_BASE_URLS,
)
from zscaler.errors.error import HTTPError, ZPAAPIError
from zscaler.exceptions.exceptions import (
    APIClientError,
    HeaderUpdateError,
    InvalidCloudEnvironmentError,
    RateLimitExceededError,
    RetryLimitExceededError,
    TokenRefreshError,
)
from zscaler.logger import setup_logging
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import is_token_expired, token_is_about_to_expire
from zscaler.zpa.app_segments import AppSegmentsAPI
from zscaler.zpa.app_segments_inspection import AppSegmentsInspectionAPI
from zscaler.zpa.app_segments_pra import AppSegmentsPRAAPI
from zscaler.zpa.certificates import CertificatesAPI
from zscaler.zpa.client_types import ClientTypesAPI
from zscaler.zpa.cloud_connector_groups import CloudConnectorGroupsAPI
from zscaler.zpa.connector_groups import ConnectorGroupsAPI
from zscaler.zpa.connectors import ConnectorsAPI
from zscaler.zpa.idp import IDPControllerAPI
from zscaler.zpa.inspection import InspectionControllerAPI
from zscaler.zpa.isolation_profile import IsolationProfileAPI
from zscaler.zpa.lss import LSSConfigControllerAPI
from zscaler.zpa.machine_groups import MachineGroupsAPI
from zscaler.zpa.platforms import PlatformsAPI
from zscaler.zpa.policies import PolicySetsAPI
from zscaler.zpa.posture_profiles import PostureProfilesAPI
from zscaler.zpa.provisioning import ProvisioningAPI
from zscaler.zpa.saml_attributes import SAMLAttributesAPI
from zscaler.zpa.scim_attributes import SCIMAttributesAPI
from zscaler.zpa.scim_groups import SCIMGroupsAPI
from zscaler.zpa.segment_groups import SegmentGroupsAPI
from zscaler.zpa.server_groups import ServerGroupsAPI
from zscaler.zpa.servers import AppServersAPI
from zscaler.zpa.service_edges import ServiceEdgesAPI
from zscaler.zpa.session import AuthenticatedSessionAPI
from zscaler.zpa.trusted_networks import TrustedNetworksAPI


class ZPA(APISession):
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
            * ``preview``
            * ``qa``
            * ``qa2``

            Defaults to ``production``.
        override_url (str):
            If supplied, this attribute can be used to override the production URL that is derived
            from supplying the `cloud` attribute. Use this attribute if you have a non-standard tenant URL
            (e.g. internal test instance etc). When using this attribute, there is no need to supply the `cloud`
            attribute. The override URL will be prepended to the API endpoint suffixes. The protocol must be included
            i.e. http:// or https://.
    """

    user_agent_obj = UserAgent()
    _vendor = "Zscaler"
    _product = user_agent_obj.get_user_agent_string
    _build = __version__
    _box = True
    _box_attrs = {"camel_killer_box": True}
    _env_base = "ZPA"
    _url = "https://config.private.zscaler.com"
    # Add rate limiter instance
    # 20 times in a 10 second interval for a GET call.
    # 10 times in a 10 second interval for any POST/PUT/DELETE call.
    rate_limiter = RateLimiter(get_limit=20, post_put_delete_limit=10, get_freq=10, post_put_delete_freq=10)

    def __init__(self, **kw):
        self.logger_name = UserAgent().get_user_agent_string  # Derive logger name from the user agent string.
        setup_logging(log_level=logging.DEBUG, logger_name=self.logger_name)
        self.logger = logging.getLogger(self.logger_name)  # Initialize the logger with the derived name.

        self._client_id = kw.get("client_id", os.getenv(f"{self._env_base}_CLIENT_ID"))
        self._client_secret = kw.get("client_secret", os.getenv(f"{self._env_base}_CLIENT_SECRET"))
        self._customer_id = kw.get("customer_id", os.getenv(f"{self._env_base}_CUSTOMER_ID"))

        # Step 2: Add an additional attribute for environment
        self._cloud = kw.get("cloud", os.getenv(f"{self._env_base}_CLOUD", "PRODUCTION")).upper()  # Default to PRODUCTION
        if self._cloud not in ZPA_BASE_URLS:
            raise APIClientError(
                f"Invalid cloud environment: {self._cloud}. Allowed values: {', '.join(ZPA_BASE_URLS.keys())}"
            )

        self._override_url = kw.get("override_url", os.getenv(f"{self._env_base}_OVERRIDE_URL"))
        self.conv_box = True

        # super(ZPA, self).__init__(**kw)
        super().__init__(**kw)

        # Update the User-Agent header to the desired format
        current_user_agent = self._session.headers["User-Agent"]
        new_user_agent = self.user_agent_obj.strip_unwanted_parts(current_user_agent)
        self._session.headers["User-Agent"] = new_user_agent

    def _handle_rate_limiting(self, method):
        """Handle rate limiting checks and sleeps."""
        self.rate_limiter.wait(method)

    def _handle_retry(self, response, attempts):
        """Handle retry based on the response status and exponential backoff."""
        if response.status_code in RETRIABLE_STATUS_CODES:
            if response.status_code == 429:
                # If there's a 'Retry-After' header, respect it. Otherwise, default backoff.
                sleep_time = int(response.headers.get("Retry-After", BACKOFF_FACTOR**attempts))
            else:
                # For other errors, use exponential backoff
                sleep_time = BACKOFF_FACTOR**attempts

            self.logger.warning(f"Encountered {response.status_code} status. Retrying in {sleep_time} seconds.")
            time.sleep(sleep_time)
            return True  # indicate that a retry is needed
        return False  # indicate that no retry is needed

    def _req(self, method, path, **kwargs):
        """Override the request method to integrate rate limiting, and retries."""

        attempts = 0
        while attempts < MAX_RETRIES:
            self._handle_rate_limiting(method)

            # Record that we're about to make a request
            self.rate_limiter.record_request(method)
            # Log request headers for troubleshooting
            self.logger.debug(f"Sending {method} request to {path} with headers: {self._session.headers}")

            try:
                self.logger.debug(f"Request Headers: {self._session.headers}")
                # Actual API call
                response = super(ZPA, self)._req(method, path, **kwargs)
                # Log response headers for troubleshooting
                self.logger.debug(
                    f"Received response from {method} request to {path} with headers: {response.get('headers','')}"
                )
                if response.get("status_code", 200) >= 400:
                    # If _handle_retry returns True, we need to retry. If not, we break the loop.
                    if not self._handle_retry(response, attempts):
                        break

                    if 400 <= response.status_code < 500:
                        raise ZPAAPIError(response.url, response, response.json())
                    else:
                        raise HTTPError(response.url, response, response.text)

            except (ConnectionError, TimeoutError):
                if attempts == MAX_RETRIES - 1:
                    self.logger.error(f"Failed to send {method} request to {path} after {MAX_RETRIES} attempts.")
                    raise RetryLimitExceededError(f"Max retries reached for {method} request to {path}")
                else:
                    self.logger.warning(f"Failed to send {method} request to {path}. Retrying...")
                    sleep_duration = BACKOFF_BASE_DURATION ** (
                        attempts + 1
                    )  # Calculate sleep duration based on the number of attempts
                    time.sleep(sleep_duration)

            except RateLimitExceededError:
                self.logger.error("Rate limit exceeded. Please try again later.")
                raise

            finally:
                attempts += 1

        # Log detailed request and response information
        try:
            response_data = response
        except ValueError:
            response_data = response.text

        self.logger.info(
            f"Calling: {method} {path}. Status code: {response.get('status_code', 200)}. Response data: {response_data}"
        )

        return response

    def _build_session(self, **kwargs) -> None:
        # Initialize _auth_token before calling the superclass's _build_session
        self._auth_token = None
        super(ZPA, self)._build_session(**kwargs)
        # Configure URL base for this API session based on the cloud environment
        self.url_base = ZPA_BASE_URLS.get(self._cloud, ZPA_BASE_URLS["PRODUCTION"])

        # If a specific cloud environment is required but not found in ZPA_BASE_URLS
        if self._cloud not in ZPA_BASE_URLS:
            raise InvalidCloudEnvironmentError(self._cloud)

        if self._override_url:
            self.url_base = self._override_url

        # Configure URLs for this API session
        self._url = f"{self.url_base}/mgmtconfig/v1/admin/customers/{self._customer_id}"
        self.user_config_url = f"{self.url_base}/userconfig/v1/customers/{self._customer_id}"
        self.v2_url = f"{self.url_base}/mgmtconfig/v2/admin/customers/{self._customer_id}"

        # If the token is None or expired, fetch a new token
        if is_token_expired(self._auth_token):
            self.logger.warning("The provided or fetched token was already expired. Refreshing...")
            try:
                self._auth_token = self.session.create_token(client_id=self._client_id, client_secret=self._client_secret)
                self._token_fetch_time = time.time()  # assuming the fetch time is now
            except Exception as e:
                raise TokenRefreshError(f"Failed to refresh the expired token: {e}")

        # If the token is about to expire, refresh it proactively
        elif token_is_about_to_expire(self._token_fetch_time):
            self.logger.info("Token is about to expire, refreshing...")
            try:
                self._auth_token = self.session.create_token(client_id=self._client_id, client_secret=self._client_secret)
                self._token_fetch_time = time.time()  # update the fetch time
            except Exception as e:
                raise TokenRefreshError(f"Failed to refresh the token that's about to expire: {str(e)}")

        # Update the session headers with the new or refreshed token
        try:
            self._session.headers.update({"Authorization": f"Bearer {self._auth_token}"})
            if hasattr(self, "user_agent"):
                self._session.headers.update({"User-Agent": self.user_agent})
        except Exception as e:
            raise HeaderUpdateError(f"Failed to update session headers: {str(e)}")

    @property
    def app_segments(self):
        """
        The interface object for the :ref:`ZPA Application Segments interface <zpa-app_segments>`.

        """
        return AppSegmentsAPI(self)

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
    def cloud_connector_groups(self):
        """
        The interface object for the :ref:`ZPA Cloud Connector Groups interface <zpa-cloud_connector_groups>`.

        """
        return CloudConnectorGroupsAPI(self)

    @property
    def connector_groups(self):
        """
        The interface object for the :ref:`ZPA Connector Groups interface <zpa-connector_groups>`.

        """
        return ConnectorGroupsAPI(self)

    @property
    def connectors(self):
        """
        The interface object for the :ref:`ZPA Connectors interface <zpa-connectors>`.

        """
        return ConnectorsAPI(self)

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
        return ProvisioningAPI(self)

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
        return SCIMAttributesAPI(self)

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
    def session(self):
        """
        The interface object for the :ref:`ZPA Session API calls <zpa-session>`.

        """

        return AuthenticatedSessionAPI(self)

    @property
    def trusted_networks(self):
        """
        The interface object for the :ref:`ZPA Trusted Networks interface <zpa-trusted_networks>`.

        """
        return TrustedNetworksAPI(self)
