import logging
import os
import time
import json
import requests
from zscaler import __version__
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.logger import setup_logging
from zscaler.user_agent import UserAgent

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class LegacyZWAClientHelper:
    """
    A Controller to access Endpoints in the Zscaler Workflow Automation (ZWA) API.

    The ZWA object handles authentication and simplifies interactions within the ZWA API.

    Attributes:
        key_id (str): The ZWA Client ID generated from the ZWA Portal.
        key_secret (str): The ZWA Client Secret generated from the ZWA Portal.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are:

            * ``us1``

        override_url (str, optional): Allows overriding the default production URL for non-standard tenant URLs.
                                      The protocol (http:// or https://) must be included.
    """

    _vendor = "Zscaler"
    _product = "Zscaler Workflow Automation"
    _build = __version__
    _env_base = "ZWA"

    def __init__(
        self,
        key_id=None,
        key_secret=None,
        cloud=None,
        timeout=240,
        request_executor_impl=None,  # Uses centralized request executor
    ):
        self._key_id = key_id or os.getenv(f"{self._env_base}_CLIENT_ID")
        self._key_secret = key_secret or os.getenv(f"{self._env_base}_CLIENT_SECRET")
        self._env_cloud = cloud or os.getenv(f"{self._env_base}_CLOUD", "us1")
        self.url = f"https://api.{self._env_cloud}.zsworkflow.net"
        self.timeout = timeout

        # Validate required credentials
        if not self._key_id or not self._key_secret:
            raise ValueError("Both key_id and key_secret are required for ZWA authentication.")
        from zscaler.request_executor import RequestExecutor

        self.cache = NoOpCache()
        # Correct `config` initialization with required keys
        self.config = {
            "client": {
                "key_id": self._key_id,
                "key_secret": self._key_secret,
                "cloud": self._env_cloud,
                "requestTimeout": self.timeout,
                "rateLimit": {"maxRetries": 3},
                "cache": {"enabled": False},
            }
        }

        self.request_executor = (request_executor_impl or RequestExecutor)(self.config, self.cache, zwa_legacy_client=self)

        self.user_agent = UserAgent().get_user_agent_string()
        self.auth_token = None
        self.headers = {}

        self.session = self._build_session()

    def _get_with_rate_limiting(self, session, url):
        """
        Helper method to perform a GET request with rate limiting retry logic.
        """
        max_retries = self.config["client"]["rateLimit"].get("maxRetries", 3)
        for attempt in range(max_retries):
            response = session.get(url, timeout=self.timeout)
            if response.status_code == 429:
                rate_limit_reset = response.headers.get("RateLimit-Reset")
                try:
                    delay = int(rate_limit_reset) + 1 if rate_limit_reset else 1
                except Exception:
                    delay = 1
                logger.info(f"Rate limit hit on GET {url}. Retrying in {delay} seconds (attempt {attempt + 1}/{max_retries}).")
                time.sleep(delay)
                continue
            try:
                response.raise_for_status()
            except Exception as e:
                logger.error("GET request failed: %s", e)
                raise Exception(f"Failed GET request for {url}: {e}")
            return response

        raise Exception(f"Failed GET request for {url} after {max_retries} attempts due to rate limiting.")

    def _build_session(self):
        """Creates a ZWA API session using the requests library and performs token validation and JWKS retrieval."""
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent, "Content-Type": "application/json"})

        token_data = self.create_token()
        token = token_data.get("token")
        if not token:
            raise Exception("Token creation failed: no token returned.")

        session.headers.update({"Authorization": f"Bearer {token}"})

        return session

    def create_token(self):
        """
        Creates a ZWA authentication token.
        Returns:
            dict: The authentication token response.
        Raises:
            Exception: If token retrieval fails.
        """
        max_retries = self.config["client"]["rateLimit"].get("maxRetries", 3)
        for attempt in range(max_retries):

            payload = {
                "key_id": self._key_id,
                "key_secret": self._key_secret,
            }

            token_url = f"{self.url}/v1/auth/api-key/token"
            logger.debug(f"Token request URL: {token_url}")
            response = requests.post(
                token_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": self.user_agent,
                },
                timeout=self.timeout,
            )

            if response.status_code == 429:
                rate_limit_reset = response.headers.get("RateLimit-Reset")
                try:
                    delay = int(rate_limit_reset) + 1 if rate_limit_reset else 1
                except Exception:
                    delay = 1
                logger.info(
                    f"Rate limit hit on token request. Retrying in {delay} seconds (attempt {attempt + 1}/{max_retries})."
                    # Ensure no sensitive data (e.g., key_secret) is logged.
                )
                time.sleep(delay)
                continue

            try:
                response.raise_for_status()  # Raise exception for non-2xx responses
            except Exception as e:
                logger.error("Failed to retrieve token: %s", e)
                raise Exception(f"Failed to retrieve token: {e}")

            token_data = response.json()
            token = token_data.get("token")
            if not token:
                raise Exception("No token found in the authentication response.")

            # Save the token and update default headers for subsequent requests
            self.auth_token = token
            self.request_executor._default_headers["Authorization"] = f"Bearer {token}"

            return token_data

        raise Exception(f"Failed to retrieve token after {max_retries} attempts due to rate limiting.")

    def get_base_url(self, endpoint):
        return self.url

    def send(self, method, path, json=None, params=None, data=None, headers=None):
        """
        Sends a request to the ZWA API directly (bypassing the central request executor)
        to avoid recursion. This implementation mimics the approach used in the LegacyZWA
        and LegacyZIA clients.

        Args:
            method (str): The HTTP method (GET, POST, PUT, DELETE).
            path (str): The API endpoint path.
            json (dict, optional): Request payload (for POST/PUT requests).
            params (dict, optional): Query parameters.
            data (dict, optional): Form data.
            headers (dict, optional): Additional request headers.

        Returns:
            tuple: A tuple (response, req_info) where response is the requests.Response
                and req_info is a dictionary containing request details.

        Raises:
            ValueError: If the HTTP request fails.
        """
        url = f"{self.url}/{path.lstrip('/')}"

        if headers is None:
            headers = {}

        # Ensure the User-Agent header is set
        headers["User-Agent"] = self.user_agent
        headers.update(self.request_executor.get_custom_headers())
        # **Add the Authorization header if a token is available**
        if self.auth_token:
            headers.setdefault("Authorization", f"Bearer {self.auth_token}")

        try:
            # Make the HTTP request directly
            response = requests.request(
                method=method, url=url, json=json, data=data, params=params, headers=headers, timeout=self.timeout
            )

            logger.info(f"Legacy ZWA client request executed successfully. " f"Status: {response.status_code}, URL: {url}")

            req_info = {
                "method": method,
                "url": url,
                "params": params or {},
                "headers": headers,
                "json": json or {},
            }
            return response, req_info

        except requests.RequestException as error:
            logger.error(f"Error sending request: {error}")
            raise ValueError(f"Request execution failed: {error}")

    @property
    def audit_logs(self):
        """
        The interface object for the :ref:`ZWA Audit Logs interface <zwa-audit_logs>`.

        """
        from zscaler.zwa.audit_logs import AuditLogsAPI

        return AuditLogsAPI(self.request_executor)

    @property
    def dlp_incidents(self):
        """
        The interface object for the :ref:`ZWA DLP Incidents interface <zwa-dlp_incidents>`.

        """
        from zscaler.zwa.dlp_incidents import DLPIncidentsAPI

        return DLPIncidentsAPI(self.request_executor)

    """
    Misc
    """

    def set_custom_headers(self, headers):
        self.request_executor.set_custom_headers(headers)

    def clear_custom_headers(self):
        self.request_executor.clear_custom_headers()

    def get_custom_headers(self):
        return self.request_executor.get_custom_headers()

    def get_default_headers(self):
        return self.request_executor.get_default_headers()
