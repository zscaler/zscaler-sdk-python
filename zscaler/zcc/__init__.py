import logging
import os
import urllib.parse
import uuid
import time
import requests
from datetime import datetime, timedelta

from zscaler import __version__
from zscaler.user_agent import UserAgent
from zscaler.utils import (
    dump_request,
    dump_response,
    format_json_response,
    is_token_expired,
    retry_with_backoff,
)
from zscaler.logger import setup_logging
from .devices import DevicesAPI
from .secrets import SecretsAPI

from zscaler.zcc.client import ZCCClient

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class ZCCClientHelper(ZCCClient):
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

    def __init__(self, **kw):
        self._apikey = kw.get("apikey", os.getenv(f"{self._env_base}_CLIENT_ID"))
        self._secret_key = kw.get("secret_key", os.getenv(f"{self._env_base}_CLIENT_SECRET"))
        self._env_cloud = (
            os.getenv(f"{self._env_base}_CLOUD") if os.getenv(f"{self._env_base}_CLOUD") is not None else kw.get("cloud")
        )
        self.login_url = f"https://api-mobile.{self._env_cloud}.net/papi/auth/v1/login"
        self.url = f"https://api-mobile.{self._env_cloud}.net/papi/public/v1"

        self.user_agent = UserAgent().get_user_agent_string()  # Ensure this returns a string
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

    @retry_with_backoff(retries=5)
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

    def send(self, method, path, json=None, params=None, stream=False):
        api = self.url
        if params is None:
            params = {}
        url = f"{api}/{path.lstrip('/')}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"

        start_time = time.time()
        headers_with_user_agent = self.headers.copy()
        headers_with_user_agent["User-Agent"] = self.user_agent
        request_uuid = str(uuid.uuid4())
        dump_request(logger, url, method, json, None, headers_with_user_agent, request_uuid)

        # Check rate limits
        self.check_rate_limit(path)

        attempts = 0
        while attempts < 5:
            try:
                self.refreshToken()
                resp = requests.request(
                    method,
                    url,
                    json=json,
                    params=None,
                    headers=headers_with_user_agent,
                    stream=stream,
                )
                dump_response(
                    logger=logger,
                    url=url,
                    params=None,
                    method=method,
                    resp=resp,
                    request_uuid=request_uuid,
                    start_time=start_time,
                )
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    if retry_after:
                        try:
                            sleep_time = int(retry_after)
                        except ValueError:
                            sleep_time = int(retry_after[:-1])
                        logger.warning(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
                        time.sleep(sleep_time)
                    else:
                        time.sleep(60)
                    attempts += 1
                    continue
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

        return resp

    def get(self, path, json=None, params=None, stream=False):
        """
        Send a GET request to the ZCC API.

        Parameters:
        path (str): API endpoint path.
        json (dict, optional): Request payload. Defaults to None.
        params (dict, optional): Query parameters. Defaults to None.
        stream (bool, optional): Whether to stream the response content. Defaults to False.

        Returns:
        Response: The response object from the API request.
        """
        resp = self.send("GET", path, json, params, stream=stream)
        if stream:
            return resp
        formatted_resp = format_json_response(resp, box_attrs=dict())
        return formatted_resp

    def post(self, path, json=None, params=None):
        """
        Send a POST request to the ZCC API.

        Parameters:
        path (str): API endpoint path.
        json (dict, optional): Request payload. Defaults to None.
        params (dict, optional): Query parameters. Defaults to None.

        Returns:
        dict: Formatted JSON response from the API.
        """
        resp = self.send("POST", path, json, params)
        formatted_resp = format_json_response(resp, box_attrs=dict())
        return formatted_resp

    @property
    def devices(self):
        """The interface object for the :ref:`ZCC Devices interface <zcc-devices>`."""
        return DevicesAPI(self)

    @property
    def secrets(self):
        """The interface object for the :ref:`ZCC Secrets interface <zcc-secrets>`."""
        return SecretsAPI(self)
