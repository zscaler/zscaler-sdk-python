import logging
import os
import time
import json
import requests
from hashlib import sha256
from zscaler import __version__
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.logger import setup_logging
from zscaler.user_agent import UserAgent

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class LegacyZDXClientHelper:
    """
    A Controller to access Endpoints in the Zscaler Digital Experience (ZDX) API.

    The ZDX object handles authentication and simplifies interactions within the ZDX API.

    Attributes:
        client_id (str): The ZDX Client ID generated from the ZDX Portal.
        client_secret (str): The ZDX Client Secret generated from the ZDX Portal.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are:

            * ``zdxcloud``
            * ``zdxbeta``

        override_url (str, optional): Allows overriding the default production URL for non-standard tenant URLs.
                                      The protocol (http:// or https://) must be included.
    """

    _vendor = "Zscaler"
    _product = "Zscaler Digital Experience"
    _build = __version__
    _env_base = "ZDX"

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        cloud=None,
        timeout=240,
        request_executor_impl=None,  # Uses centralized request executor
    ):
        self._client_id = client_id or os.getenv(f"{self._env_base}_CLIENT_ID")
        self._client_secret = client_secret or os.getenv(f"{self._env_base}_CLIENT_SECRET")
        self._env_cloud = cloud or os.getenv(f"{self._env_base}_CLOUD", "zdxcloud")
        self.url = f"https://api.{self._env_cloud}.net"
        self.timeout = timeout

        # Validate required credentials
        if not self._client_id or not self._client_secret:
            raise ValueError("Both client_id and client_secret are required for ZDX authentication.")
        from zscaler.request_executor import RequestExecutor

        self.cache = NoOpCache()
        # Correct `config` initialization with required keys
        self.config = {
            "client": {
                "clientId": self._client_id,
                "clientSecret": self._client_secret,
                "cloud": self._env_cloud,
                "requestTimeout": self.timeout,
                "rateLimit": {"maxRetries": 3},
                "cache": {"enabled": False},
            }
        }

        self.request_executor = (request_executor_impl or RequestExecutor)(self.config, self.cache, zdx_legacy_client=self)

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
                sanitized_url = url.split("?")[0]
                logger.info(
                    f"Rate limit hit on GET {sanitized_url}.Retrying in {delay} seconds (attempt {attempt + 1}/{max_retries})"
                )
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
        """Creates a ZDX API session using the requests library and performs token validation and JWKS retrieval."""
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent, "Content-Type": "application/json"})

        token_data = self.create_token()
        token = token_data.get("token")
        if not token:
            raise Exception("Token creation failed: no token returned.")

        session.headers.update({"Authorization": f"Bearer {token}"})

        validate_url = f"{self.url}/v1/oauth/validate"
        try:
            validate_response = self._get_with_rate_limiting(session, validate_url)
            validate_data = validate_response.json()
            # logger.debug(f"Token validation response: {validate_data}")
            logger.debug(f"Token validation response: {{'valid': {validate_data.get('valid', False)}}}")
            if not validate_data.get("valid", False):
                raise Exception("Token validation failed: token is not valid.")
            else:
                logger.info("Token validated successfully.")
        except Exception as e:
            logger.error("Token validation failed: %s", e)
            raise Exception(f"Token validation failed: {e}")

        jwks_url = f"{self.url}/v1/oauth/jwks"
        try:
            jwks_response = self._get_with_rate_limiting(session, jwks_url)
            jwks_data = jwks_response.json()
            # logger.debug(f"JWKS response: {json.dumps(jwks_data, indent=2)}")
            sanitized_jwks_data = {"keys": [{"kid": key.get("kid")} for key in jwks_data.get("keys", [])]}
            logger.debug(f"Sanitized JWKS response: {json.dumps(sanitized_jwks_data, indent=2)}")
        except Exception as e:
            logger.error("Failed to retrieve JWKS: %s", e)
            raise Exception(f"Failed to retrieve JWKS: {e}")

        return session

    def create_token(self):
        """
        Creates a ZDX authentication token.
        Returns:
            dict: The authentication token response.
        Raises:
            Exception: If token retrieval fails.
        """
        max_retries = self.config["client"]["rateLimit"].get("maxRetries", 3)
        for attempt in range(max_retries):
            epoch_time = int(time.time())
            api_secret_format = f"{self._client_secret}:{epoch_time}"
            api_secret_hash = sha256(api_secret_format.encode("utf-8")).hexdigest()

            payload = {
                "key_id": self._client_id,
                "key_secret": api_secret_hash,
                "timestamp": epoch_time,
            }

            token_url = f"{self.url}/v1/oauth/token"
            # logger.debug(f"Token request URL: {token_url}")
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
                    # f"Rate limit hit on token request. Retrying in {delay} seconds (attempt {attempt + 1}/{max_retries})."
                    "Rate limit hit on token request. Retrying after a delay. Attempt %d of %d.",
                    attempt + 1,
                    max_retries,
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

    def validate_token(self):
        """
        Validates the current ZDX JWT token.

        Returns:
            dict: The validated session information.
        """
        response, error = self.request_executor.execute(self.request_executor.create_request("GET", "/v1/oauth/validate"))

        if error:
            raise Exception(f"Failed to validate token: {error}")

        return response.data

    def get_jwks(self):
        """
        Returns the JSON Web Key Set (JWKS) containing public keys used to verify JWT tokens.

        Returns:
            dict: The JWKS response.
        """
        response, error = self.request_executor.execute(self.request_executor.create_request("GET", "/v1/oauth/jwks"))

        if error:
            raise Exception(f"Failed to retrieve JWKS: {error}")

        return response.data

    def get_base_url(self, endpoint):
        return self.url

    def send(self, method, path, json=None, params=None, data=None, headers=None):
        """
        Sends a request to the ZDX API directly (bypassing the central request executor)
        to avoid recursion. This implementation mimics the approach used in the LegacyZPA
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

        # **Add the Authorization header if a token is available**
        if self.auth_token:
            headers.setdefault("Authorization", f"Bearer {self.auth_token}")
        headers.update(self.request_executor.get_custom_headers())
        try:
            # Make the HTTP request directly
            response = requests.request(
                method=method, url=url, json=json, data=data, params=params, headers=headers, timeout=self.timeout
            )

            logger.info(f"Legacy ZDX client request executed successfully. " f"Status: {response.status_code}, URL: {url}")

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
    def admin(self):
        """
        The interface object for the :ref:`ZDX Admin interface <zdx-admin>`.

        """
        from zscaler.zdx.admin import AdminAPI

        return AdminAPI(self.request_executor)

    @property
    def alerts(self):
        """
        The interface object for the :ref:`ZDX Alerts interface <zdx-alerts>`.

        """
        from zscaler.zdx.alerts import AlertsAPI

        return AlertsAPI(self.request_executor)

    @property
    def apps(self):
        """
        The interface object for the :ref:`ZDX Apps interface <zdx-apps>`.

        """
        from zscaler.zdx.apps import AppsAPI

        return AppsAPI(self.request_executor)

    @property
    def devices(self):
        """
        The interface object for the :ref:`ZDX Devices interface <zdx-devices>`.

        """
        from zscaler.zdx.devices import DevicesAPI

        return DevicesAPI(self.request_executor)

    @property
    def inventory(self):
        """
        The interface object for the :ref:`ZDX Inventory interface <zdx-inventory>`.

        """
        from zscaler.zdx.inventory import InventoryAPI

        return InventoryAPI(self.request_executor)

    @property
    def troubleshooting(self):
        """
        The interface object for the :ref:`ZDX Troubleshooting interface <zdx-troubleshooting>`.

        """
        from zscaler.zdx.troubleshooting import TroubleshootingAPI

        return TroubleshootingAPI(self.request_executor)

    @property
    def users(self):
        """
        The interface object for the :ref:`ZDX Users interface <zdx-users>`.

        """
        from zscaler.zdx.users import UsersAPI

        return UsersAPI(self.request_executor)

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
