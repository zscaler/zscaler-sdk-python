import logging
import os
import urllib.parse
import uuid
import time
import requests
from datetime import datetime, timedelta

from zscaler import __version__
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.user_agent import UserAgent
from zscaler.utils import (
    is_token_expired,
)
from zscaler.logger import setup_logging

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class LegacyZCCClientHelper():
    """
    A Controller to access Endpoints in the Zscaler Mobile Admin Portal API.

    The ZCC object stores the session token and simplifies access to CRUD options within the ZCC Portal.

    Attributes:
        client_id (str): The ZCC Client ID generated from the ZCC Portal.
        client_secret (str): The ZCC Client Secret generated from the ZCC Portal.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are:

            * ``zscaler``
            * ``zscalerone``
            * ``zscalertwo``
            * ``zscalerthree``
            * ``zscloud``
            * ``zscalerbeta``
        override_url (str):
            If supplied, this attribute can be used to override the production URL that is derived
            from supplying the `cloud` attribute. Use this attribute if you have a non-standard tenant URL
            (e.g. internal test instance etc). When using this attribute, there is no need to supply the `cloud`
            attribute. The override URL will be prepended to the API endpoint suffixes. The protocol must be included
            i.e. http:// or https://.

    """

    _vendor = "Zscaler"
    _product = "Zscaler Mobile Admin Portal"
    _backoff = 3
    _build = __version__
    _env_base = "ZCC"
    _env_cloud = "zscaler"

    RATE_LIMIT = 100  # 100 API calls per hour
    DOWNLOAD_DEVICES_LIMIT = 3  # 3 calls per day
    RATE_LIMIT_RESET_TIME = timedelta(hours=1)
    DOWNLOAD_DEVICES_RESET_TIME = timedelta(days=1)

    def __init__(self, apikey=None, secret_key=None, cloud=None, timeout=240, cache=None):
        from zscaler.request_executor import RequestExecutor

        self._apikey = apikey or os.getenv("apikey", os.getenv(f"{self._env_base}_CLIENT_ID"))
        self._secret_key = secret_key or os.getenv("secret_key", os.getenv(f"{self._env_base}_CLIENT_SECRET"))
        self._env_cloud = cloud or os.getenv(f"{self._env_base}_CLOUD", "zscaler")
        self.login_url = f"https://api-mobile.{self._env_cloud}.net/papi/auth/v1/login"
        self.url = f"https://api-mobile.{self._env_cloud}.net"
        
        self.timeout = timeout
        
        # Correct cache initialization
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

        # Correct `config` initialization with required keys
        self.config = {
            "client": {
                "apikey": self._apikey,
                "secret_key": self._secret_key or "",
                "cloud": self._env_cloud,
                "requestTimeout": self.timeout,
                "rateLimit": {
                    "maxRetries": 3
                },
                "cache": {
                    "enabled": cache_enabled,
                },
            }
        }

        # Correct initialization of the request executor
        self.request_executor = RequestExecutor(
            self.config, self.cache, zcc_legacy_client=self
        )

        self.user_agent = UserAgent().get_user_agent_string()
        self.auth_token = None
        self.headers = {}
        self.refreshToken()

        # Initialize rate limit tracking
        self.last_request_time = datetime.utcnow()
        self.request_count = 0

        # Track specific download devices endpoint usage
        self.download_devices_count = 0
        self.download_devices_last_reset = datetime.utcnow()


    def __enter__(self):
        self.refreshToken()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("Deauthenticating...")

    def refreshToken(self):
        if not self.auth_token or is_token_expired(self.auth_token):
            response = self.login()
            if response is None or response.status_code > 299 or not response.json():
                logger.error("Failed to login using provided credentials, response: %s", response)
                raise Exception("Failed to login using provided credentials.")
            self.auth_token = response.json().get("jwtToken")
            self.headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "auth-token": f"{self.auth_token}",
                "User-Agent": self.user_agent,
            }

    # @retry_with_backoff(retries=5)
    def login(self):
        data = {"apiKey": self._apikey, "secretKey": self._secret_key}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": self.user_agent,
        }
        try:
            url = self.login_url
            resp = requests.post(url, json=data, headers=headers)
            logger.info("Login attempt with status: %d", resp.status_code)
            return resp
        except Exception as e:
            logger.error("Login failed due to an exception: %s", str(e))
            return None

    def check_rate_limit(self, path):
        """
        Checks the rate limit and adjusts the request timing accordingly.
        """
        current_time = datetime.utcnow()
        time_since_last_request = current_time - self.last_request_time

        # Reset the rate limit counter if the reset time has passed
        if time_since_last_request >= self.RATE_LIMIT_RESET_TIME:
            self.request_count = 0
            self.last_request_time = current_time

        if "/downloadDevices" in path:
            time_since_last_reset = current_time - self.download_devices_last_reset
            if time_since_last_reset >= self.DOWNLOAD_DEVICES_RESET_TIME:
                self.download_devices_count = 0
                self.download_devices_last_reset = current_time
            if self.download_devices_count >= self.DOWNLOAD_DEVICES_LIMIT:
                logger.warning("Rate limit exceeded for /downloadDevices endpoint. Backing off...")
                time.sleep(24 * 60 * 60)  # Back off for a day
                self.download_devices_count = 0
                self.download_devices_last_reset = datetime.utcnow()
            self.download_devices_count += 1
        else:
            if self.request_count >= self.RATE_LIMIT:
                logger.warning("Rate limit exceeded. Backing off...")
                time.sleep(3600)  # Back off for an hour
                self.request_count = 0
                self.last_request_time = datetime.utcnow()
            self.request_count += 1

    def get_base_url(self, endpoint):
        return self.url
    
    def send(self, method, path, json=None, params=None, stream=False):
        """
        Sends a request using the legacy client.
        """
        api = self.url
        params = params or {}
        url = f"{api}/{path.lstrip('/')}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"

        headers_with_user_agent = self.headers.copy()
        headers_with_user_agent["User-Agent"] = self.user_agent

        # Check rate limits
        self.check_rate_limit(path)

        attempts = 0
        while attempts < 5:
            try:
                # Refresh token before each attempt
                self.refreshToken()

                # Execute the request
                response = requests.request(
                    method,
                    url,
                    json=json,
                    headers=headers_with_user_agent,
                    stream=stream,
                    timeout=self.timeout,
                )

                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    sleep_time = int(retry_after) if retry_after and retry_after.isdigit() else 60
                    logger.warning(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
                    time.sleep(sleep_time)
                    attempts += 1
                    continue
                elif response.status_code >= 400:
                    logger.error(f"Request failed: {response.status_code}, {response.text}")
                    raise ValueError(f"Request failed with status {response.status_code}")
                else:
                    break
            except requests.RequestException as e:
                if attempts == 4:
                    logger.error(f"Failed to send {method} request to {url} after 5 attempts. Error: {str(e)}")
                    raise e
                else:
                    logger.warning(f"Failed to send {method} request to {url}. Retrying... Error: {str(e)}")
                    attempts += 1
                    time.sleep(5)

        return response, {
            "method": method,
            "url": url,
            "params": params,
            "headers": headers_with_user_agent,
            "json": json or {},
        }

    def set_session(self, session):
        """Dummy method for compatibility with the request executor."""
        self._session = session

    @property
    def devices(self):
        """
        The interface object for the :ref:`ZCC devices interface <zcc-devices>`.

        """
        from zscaler.zcc.devices import DevicesAPI
        return DevicesAPI(self.request_executor)
    