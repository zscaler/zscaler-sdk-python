import logging
import os
import urllib.parse
import uuid
import time
import requests
from datetime import datetime, timedelta
from box import Box, BoxList
from zscaler import __version__
from zscaler.user_agent import UserAgent
from zscaler.utils import (
    dump_request,
    dump_response,
    format_json_response,
    is_token_expired,
    retry_with_backoff,
    convert_keys_to_snake
)
from zscaler.ratelimiter.ratelimiter import RateLimiter
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
        # Initialize rate limiter
        # You may want to adjust these parameters as per your rate limit configuration
        self.rate_limiter = RateLimiter(
            get_limit=2,  # Adjust as per actual limit
            post_put_delete_limit=2,  # Adjust as per actual limit
            get_freq=2,  # Adjust as per actual frequency (in seconds)
            post_put_delete_freq=2,  # Adjust as per actual frequency (in seconds)
        )
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

    def get_paginated_data(
        self,
        path=None,
        expected_status_code=200,
        page=None,
        pagesize=None,
        search=None,
    ):
        """
        Fetches paginated data from the API based on specified parameters and handles pagination.

        Args:
            path (str): The API endpoint path to send requests to.
            expected_status_code (int): The expected HTTP status code for a successful request.
            page (int, optional): Specific page number to fetch (1-based).
            pagesize (int, optional): Number of items per page, default is 100, max is 10,000.
            search (str, optional): Search query to filter the results.

        Returns:
            tuple: A tuple containing:
                - BoxList: A list of fetched items wrapped in a BoxList for easy access.
                - str: An error message if any occurred during the data fetching process.
        """
        logger = logging.getLogger(__name__)

        ERROR_MESSAGES = {
            "UNEXPECTED_STATUS": "Unexpected status code {status_code} received for page {page}.",
            "EMPTY_RESULTS": "No results found for page {page}.",
        }

        # ✅ Ensure 'pageSize' is always converted to camelCase
        params = {
            "page": page if page is not None else 1,  # Default is 1-based page
            "pageSize": pagesize if pagesize is not None else 100,  # Default is 100, max is 10,000
        }

        # Add optional filters to the params if provided
        if search:
            params["search"] = search

        # If the user specifies a single page, fetch only that page
        if page is not None:
            response = self.send("GET", path=path, params=params)
            if response.status_code != expected_status_code:
                error_msg = ERROR_MESSAGES["UNEXPECTED_STATUS"].format(status_code=response.status_code, page=params["page"])
                logger.error(error_msg)
                return BoxList([]), error_msg

            response_data = response.json()
            if not isinstance(response_data, list):
                error_msg = ERROR_MESSAGES["EMPTY_RESULTS"].format(page=params["page"])
                logger.warn(error_msg)
                return BoxList([]), error_msg

            data = convert_keys_to_snake(response_data)
            return BoxList(data), None

        # If no page is specified, iterate through pages to fetch all items
        ret_data = []

        try:
            while True:
                should_wait, delay = self.rate_limiter.wait("GET")
                if should_wait:
                    time.sleep(delay)

                # Send the request to the API
                response = self.send("GET", path=path, params=params)

                # Check for unexpected status code
                if response.status_code != expected_status_code:
                    error_msg = ERROR_MESSAGES["UNEXPECTED_STATUS"].format(
                        status_code=response.status_code, page=params["page"]
                    )
                    logger.error(error_msg)
                    return BoxList([]), error_msg

                # Parse the response as a flat list of items
                response_data = response.json()
                if not isinstance(response_data, list):
                    error_msg = ERROR_MESSAGES["EMPTY_RESULTS"].format(page=params["page"])
                    logger.warn(error_msg)
                    return BoxList([]), error_msg

                data = convert_keys_to_snake(response_data)
                ret_data.extend(data)

                # Stop if fewer items than pageSize are returned (indicating last page)
                if len(data) < params["pageSize"]:
                    break

                # Move to the next page
                params["page"] += 1

        finally:
            time.sleep(2)  # Ensure a delay between requests regardless of outcome

        if not ret_data:
            error_msg = ERROR_MESSAGES["EMPTY_RESULTS"].format(page=params["page"])
            logger.warn(error_msg)
            return BoxList([]), error_msg

        return BoxList(ret_data), None
