import logging
import os
import urllib.parse
import time
import requests
from datetime import datetime, timedelta
from zscaler import __version__
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.user_agent import UserAgent
from zscaler.utils import (
    is_token_expired,
    RateLimitExceededError
)
from zscaler.errors.response_checker import check_response_for_error
from zscaler.logger import setup_logging

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class LegacyZCCClientHelper:
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

    def __init__(self, api_key=None, secret_key=None, cloud=None, timeout=240, cache=None, request_executor_impl=None):
        from zscaler.request_executor import RequestExecutor

        self._api_key = api_key or os.getenv("api_key", os.getenv(f"{self._env_base}_CLIENT_ID"))
        self._secret_key = secret_key or os.getenv("secret_key", os.getenv(f"{self._env_base}_CLIENT_SECRET"))
        self._env_cloud = cloud or os.getenv(f"{self._env_base}_CLOUD", "zscaler")
        self.login_url = f"https://api-mobile.{self._env_cloud}.net/papi/auth/v1/login"
        self.url = f"https://api-mobile.{self._env_cloud}.net"

        self.timeout = timeout

        self.cache = NoOpCache()

        # Correct `config` initialization with required keys
        self.config = {
            "client": {
                "apiKey": self._api_key,
                "secretKey": self._secret_key or "",
                "cloud": self._env_cloud,
                "requestTimeout": self.timeout,
                "rateLimit": {"maxRetries": 3},
                "cache": {
                    "enabled": False,
                },
            }
        }

        # Correct initialization of the request executor
        self.request_executor = (request_executor_impl or RequestExecutor)(self.config, self.cache, zcc_legacy_client=self)

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
        data = {"apiKey": self._api_key, "secretKey": self._secret_key}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": self.user_agent,
        }
        try:
            url = self.login_url
            resp = requests.post(url, json=data, headers=headers)
            _, err = check_response_for_error(url, resp, resp.text)
            if err:
                raise err

            logger.info("Login attempt with status: %d", resp.status_code)
            return resp
        except Exception as e:
            logger.error("Login failed due to an exception: %s", str(e))
            return None

    # ---------------------------------------------------------------
    # Helper – calculate pause-time from server hints
    # ---------------------------------------------------------------
    @staticmethod
    def _get_backoff_seconds(response, default=60):
        """
        Return how many seconds to wait before the next retry.

        • /downloadDevices → X-Rate-Limit-Retry-After-Seconds
        • everything else → fixed default
        """
        retry_after_sec = response.headers.get("X-Rate-Limit-Retry-After-Seconds")
        if retry_after_sec and retry_after_sec.isdigit():
            return int(retry_after_sec) + 1        # 1-second pad
        return default

    # ------------------------------------------------------------------
    # 1.  Local counter / pre-check
    # ------------------------------------------------------------------

    def check_rate_limit(self, path):
        """
        Local rolling counters:
        • 100 calls/hour for any endpoint
        • 3 calls/day for /downloadDevices
        Raise RateLimitExceededError immediately if exhausted.
        """
        now = datetime.utcnow()

        # ----- hourly generic limit ---------------------------------
        if now - self.last_request_time >= self.RATE_LIMIT_RESET_TIME:
            self.request_count = 0
            self.last_request_time = now

        if self.request_count >= self.RATE_LIMIT:
            raise RateLimitExceededError("IP address exceeded 100 calls per hour")

        # ----- /downloadDevices daily limit ------------------------
        if "/downloadDevices" in path:
            if now - self.download_devices_last_reset >= self.DOWNLOAD_DEVICES_RESET_TIME:
                self.download_devices_count = 0
                self.download_devices_last_reset = now

            if self.download_devices_count >= self.DOWNLOAD_DEVICES_LIMIT:
                raise RateLimitExceededError("/downloadDevices exceeded 3 calls per day")

            self.download_devices_count += 1

        # ----- increment generic counter ---------------------------
        self.request_count += 1

    def get_base_url(self, endpoint):
        return self.url

    # ------------------------------------------------------------------
    # 2.  The sending logic  (three tries on 429, then fail neatly)
    # ------------------------------------------------------------------

    def send(self, method, path, json=None, params=None, stream=False):
        """
        Sends a request using the legacy ZCC client.
        Retries up to three times on HTTP-429 for general endpoints,
        but raises immediately for /downloadDevices and /downloadServiceStatus.
        """
        api = self.url
        params = params or {}
        url = f"{api}/{path.lstrip('/')}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"

        headers_with_user_agent = self.headers.copy()
        headers_with_user_agent["User-Agent"] = self.user_agent
        headers_with_user_agent.update(self.request_executor.get_custom_headers())

        # ---------- pre-flight local quota -------------------------
        try:
            self.check_rate_limit(path)
        except RateLimitExceededError as err:
            raise ValueError(
                "This endpoint has a rate limit of 3 calls per day, try again in 24 hours."
                if "/downloadDevices" in path or "/downloadServiceStatus" in path
                else "Specific IP addresses are subjected to a rate limit of 100 calls per hour."
            ) from err

        max_attempts = 3
        attempts = 0

        while True:
            try:
                self.refreshToken()

                response = requests.request(
                    method=method,
                    url=url,
                    json=json,
                    headers=headers_with_user_agent,
                    stream=stream,
                    timeout=self.timeout,
                )

                # ---------- 429 handling -----------------------------
                if response.status_code == 429:
                    if "/downloadDevices" in path or "/downloadServiceStatus" in path:
                        retry_after = self._get_backoff_seconds(response, default=86400)
                        raise ValueError(
                            f"This endpoint has a rate limit of 3 calls per day. Try again in {retry_after} seconds."
                        )

                    # for all other paths, allow limited retry
                    attempts += 1
                    if attempts == max_attempts:
                        raise ValueError(
                            "Specific IP addresses are subjected to a rate limit of 100 calls per hour."
                        )

                    backoff = self._get_backoff_seconds(response, default=60)
                    logger.warning("Rate limit (429). Retrying in %s seconds …", backoff)
                    time.sleep(backoff)
                    continue

                # ---------- proactive check of Remaining header ------
                remaining = response.headers.get("X-Rate-Limit-Remaining")
                if remaining is not None and remaining.isdigit() and int(remaining) == 0:
                    # treat as a soft-429
                    attempts += 1
                    if attempts == max_attempts:
                        raise ValueError(
                            "Specific IP addresses are subjected to a rate limit of 100 calls per hour."
                        )
                    logger.warning("Server reports 0 remaining calls. Retrying in 60 seconds …")
                    time.sleep(60)
                    continue

                # ---------- API-level errors -------------------------
                _, err = check_response_for_error(url, response, response.text)
                if err:
                    raise err

                break  # success

            except ValueError as ve:
                # Allow custom raised ValueErrors to bubble up immediately (e.g. downloadDevices rate limit)
                raise ve

            except requests.RequestException as e:
                attempts += 1
                if attempts == max_attempts:
                    raise
                logger.warning(
                    "Network error talking to %s. Retrying … (%d/%d) %s",
                    url, attempts, max_attempts, str(e)
                )
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

    @property
    def admin_user(self):
        """
        The interface object for the :ref:`ZCC admin user interface <zcc-admin_user>`.

        """
        from zscaler.zcc.admin_user import AdminUserAPI

        return AdminUserAPI(self.request_executor)

    @property
    def company(self):
        """
        The interface object for the :ref:`ZCC admin user interface <zcc-company_info>`.

        """
        from zscaler.zcc.company import CompanyInfoAPI

        return CompanyInfoAPI(self.request_executor)

    @property
    def entitlements(self):
        """
        The interface object for the :ref:`ZCC admin user interface <zcc-entitlements>`.

        """
        from zscaler.zcc.entitlements import EntitlementAPI

        return EntitlementAPI(self.request_executor)

    @property
    def forwarding_profile(self):
        """
        The interface object for the :ref:`ZCC web forwarding profile interface <zcc-forwarding_profile>`.

        """
        from zscaler.zcc.forwarding_profile import ForwardingProfileAPI

        return ForwardingProfileAPI(self.request_executor)

    @property
    def fail_open_policy(self):
        """
        The interface object for the :ref:`ZCC fail open policy interface <zcc-fail_open_policy>`.

        """
        from zscaler.zcc.fail_open_policy import FailOpenPolicyAPI

        return FailOpenPolicyAPI(self.request_executor)

    @property
    def web_policy(self):
        """
        The interface object for the :ref:`ZCC web policy interface <zcc-web_policy>`.

        """
        from zscaler.zcc.web_policy import WebPolicyAPI

        return WebPolicyAPI(self.request_executor)

    @property
    def web_app_service(self):
        """
        The interface object for the :ref:`ZCC web app service interface <zcc-web_app_service>`.

        """
        from zscaler.zcc.web_app_service import WebAppServiceAPI

        return WebAppServiceAPI(self.request_executor)

    @property
    def web_privacy(self):
        """
        The interface object for the :ref:`ZCC web privacy interface <zcc-web_privacy>`.

        """
        from zscaler.zcc.web_privacy import WebPrivacyAPI

        return WebPrivacyAPI(self.request_executor)

    @property
    def trusted_networks(self):
        """
        The interface object for the :ref:`ZCC trusted networks interface <zcc-trusted_networks>`.

        """
        from zscaler.zcc.trusted_networks import TrustedNetworksAPI

        return TrustedNetworksAPI(self.request_executor)

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
