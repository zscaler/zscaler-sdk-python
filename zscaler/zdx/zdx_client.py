import logging
import os
import time
import uuid
import requests
from hashlib import sha256

from zscaler.utils import (
    format_json_response,
    dump_request,
    dump_response,
)
from zscaler import __version__
from zscaler.logger import setup_logging
from zscaler.user_agent import UserAgent
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class ZDXClientHelper:
    """
    A Controller to access Endpoints in the Zscaler Digital Experience (ZDX) API.

    The ZDX object stores the session token and simplifies access to CRUD options within the ZDX Portal.

    Attributes:
        client_id (str): The ZDX Client ID generated from the ZDX Portal.
        client_secret (str): The ZDX Client Secret generated from the ZDX Portal.
        cloud (str): The Zscaler cloud for your tenancy, accepted values are below. Defaults to ``zdxcloud``.

            * ``zdxcloud``
            * ``zdxbeta``

        override_url (str):
            If supplied, this attribute can be used to override the production URL that is derived
            from supplying the `cloud` attribute. Use this attribute if you have a non-standard tenant URL
            (e.g. internal test instance etc). When using this attribute, there is no need to supply the `cloud`
            attribute. The override URL will be prepended to the API endpoint suffixes. The protocol must be included
            i.e. http:// or https://.
    """

    _vendor = "Zscaler"
    _product = "zscaler"
    _build = __version__
    _env_base = "ZDX"
    env_cloud = "zdxcloud"
    url = "https://api.zdxcloud.net/v1"

    def __init__(self, **kw):
        setup_logging()
        self.logger = logging.getLogger("zscaler-sdk-python")

        self.client_id = kw.get("client_id", os.getenv(f"{self._env_base}_CLIENT_ID"))
        self.client_secret = kw.get("client_secret", os.getenv(f"{self._env_base}_CLIENT_SECRET"))
        self.cloud = kw.get("cloud", os.getenv(f"{self._env_base}_CLOUD", self.env_cloud))
        self.url = kw.get("override_url", os.getenv(f"{self._env_base}_OVERRIDE_URL")) or f"https://api.{self.cloud}.net/v1"

        self.rate_limiter = RateLimiter(get_limit=5, post_put_delete_limit=5, get_freq=60, post_put_delete_freq=60)

        ua = UserAgent()
        self.user_agent = ua.get_user_agent_string()
        cache_enabled = os.environ.get("ZSCALER_CLIENT_CACHE_ENABLED", "true").lower() == "true"
        if cache_enabled:
            ttl = int(os.getenv("ZSCALER_CLIENT_CACHE_DEFAULT_TTL", 3600))
            tti = int(os.getenv("ZSCALER_CLIENT_CACHE_DEFAULT_TTI", 1800))
            self.cache = ZscalerCache(ttl=ttl, tti=tti)
        else:
            self.cache = NoOpCache()

        self.session = self._build_session()

    def _build_session(self):
        """Creates a ZDX API session using the requests library."""
        session = requests.Session()
        session.headers.update(
            {"User-Agent": self.user_agent, "Content-Type": "application/json"}  # Ensure content type is set
        )
        token = self.create_token()
        session.headers.update({"Authorization": f"Bearer {token}"})
        return session

    def create_token(self):
        """Creates a ZDX authentication token."""
        epoch_time = int(time.time())
        api_secret_format = f"{self.client_secret}:{epoch_time}"
        api_secret_hash = sha256(api_secret_format.encode("utf-8")).hexdigest()

        payload = {
            "key_id": self.client_id,
            "key_secret": api_secret_hash,
            "timestamp": epoch_time,
        }

        # Mask the client_id and key_secret for logging
        masked_client_id = f"****{self.client_id[-3:]}" if self.client_id else None
        masked_key_secret = "****"

        self.logger.debug(
            "Token request payload: {'key_id': '%s', 'key_secret': '%s', 'timestamp': %d}",
            masked_client_id,
            masked_key_secret,
            epoch_time,
        )
        token_url = f"{self.url}/oauth/token"
        self.logger.debug(f"Token request URL: {token_url}")

        response = requests.post(token_url, json=payload, headers={"Content-Type": "application/json"})

        self.logger.debug(f"Token request response status: {response.status_code}")
        self.logger.debug(f"Token request response content: {response.text}")

        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("token")

    def validate_token(self):
        """
        Validates the current ZDX JWT token.

        Returns:
            :obj:`Box`: The validated session information.

        Examples:
            >>> validation = zdx.session.validate()
        """
        resp = self.session.get(f"{self.url}/oauth/validate")
        resp.raise_for_status()
        return format_json_response(resp, box_attrs=dict())

    def get_jwks(self):
        """
        Returns a JSON Web Key Set (JWKS) that contains the public keys that can be used to verify the JWT tokens.

        Returns:
            :obj:`Box`: The JSON Web Key Set (JWKS).

        Examples:
            >>> jwks = zdx.session.get_jwks()
        """
        resp = self.session.get(f"{self.url}/oauth/jwks")
        resp.raise_for_status()
        return format_json_response(resp, box_attrs=dict())

    def send(self, method, path, json=None, params=None, data=None, headers=None):
        """
        Send a request to the ZDX API.

        Parameters:
        - method (str): The HTTP method.
        - path (str): API endpoint path.
        - json (dict, optional): Request payload. Defaults to None.
        - params (dict, optional): Query parameters. Defaults to None.
        - data (dict, optional): Request data. Defaults to None.
        - headers (dict, optional): Request headers. Defaults to None.

        Returns:
        - Response: Response object from the request.
        """
        url = f"{self.url}/{path.lstrip('/')}"
        start_time = time.time()

        if headers is None:
            headers = {}

        # Use rate limiter before making a request
        should_wait, delay = self.rate_limiter.wait(method)
        if should_wait:
            self.logger.info(f"Rate limit exceeded. Waiting for {delay} seconds.")
            time.sleep(delay)

        # Add a constant delay before making the request
        additional_delay = 5  # Extra 5 seconds delay
        time.sleep(additional_delay)

        # Update headers to include the user agent
        headers["User-Agent"] = self.user_agent

        # Generate a unique UUID for this request
        request_uuid = uuid.uuid4()
        self.logger.info(f"Sending {method} request to {url} with UUID {request_uuid}")

        # Check cache before sending request
        cache_key = self.cache.create_key(url, params)
        if method == "GET" and self.cache.contains(cache_key):
            resp = self.cache.get(cache_key)
            self.logger.info(f"Cache hit for key {cache_key}")
            dump_response(
                logger=self.logger,
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
        max_attempts = 5
        backoff_factor = 1  # Initial backoff factor

        while attempts < max_attempts:
            try:
                dump_request(
                    logger=self.logger,
                    url=url,
                    method=method,
                    json=json,
                    params=params,
                    headers=headers,
                    request_uuid=request_uuid,
                    body=True,
                )

                resp = self.session.request(method=method, url=url, json=json, data=data, params=params, headers=headers)

                # Log rate limit headers
                rate_limit_limit = resp.headers.get("RateLimit-Limit")
                rate_limit_remaining = resp.headers.get("RateLimit-Remaining")
                rate_limit_reset = resp.headers.get("RateLimit-Reset")
                rate_limit_reset_time = int(rate_limit_reset) if rate_limit_reset else None

                if rate_limit_limit and rate_limit_remaining and rate_limit_reset:
                    self.logger.info(f"RateLimit-Limit: {rate_limit_limit}")
                    self.logger.info(f"RateLimit-Remaining: {rate_limit_remaining}")
                    self.logger.info(f"RateLimit-Reset: {rate_limit_reset}")

                    # Update rate limits based on headers
                    self.rate_limiter.update_limits(resp.headers)

                if resp.status_code == 429:  # HTTP Status code 429 indicates "Too Many Requests"
                    if rate_limit_reset_time:
                        sleep_time = rate_limit_reset_time - int(time.time())
                    else:
                        sleep_time = min(2**backoff_factor, 60)  # Exponential backoff with a max limit
                    self.logger.warning(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
                    time.sleep(sleep_time + additional_delay)  # Adding additional delay here too
                    attempts += 1
                    backoff_factor += 1  # Increment backoff factor
                    continue

                # Log response
                self.logger.info(f"Received response for {method} request to {url} with UUID {request_uuid}")
                self.logger.debug(f"Response status code: {resp.status_code}")
                self.logger.debug(f"Response content: {resp.text}")

                dump_response(
                    logger=self.logger,
                    url=url,
                    method=method,
                    params=params,
                    resp=resp,
                    request_uuid=request_uuid,
                    start_time=start_time,
                )

                # Cache the response if it's a successful GET request
                if method == "GET" and resp.status_code == 200:
                    self.cache.add(cache_key, resp)
                    self.logger.info(f"Cache updated for key {cache_key}")

                return resp

            except requests.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                if attempts == max_attempts - 1:  # If it's the last attempt, raise the exception
                    raise e
                attempts += 1
                backoff_factor += 1  # Increment backoff factor
                self.logger.warning(f"Failed to send {method} request to {url}. Retrying... Error: {e}")
                time.sleep(min(2**backoff_factor, 60) + additional_delay)  # Adding additional delay here too

        return None

    def get(self, path, json=None, params=None):
        """
        Send a GET request to the ZDX API.

        Parameters:
        - path (str): API endpoint path.
        - json (dict, optional): Request payload. Defaults to None.
        - params (dict, optional): Query parameters. Defaults to None.

        Returns:
        - Response: Response object from the request.
        """

        # Use rate limiter before making a request
        should_wait, delay = self.rate_limiter.wait("GET")
        if should_wait:
            time.sleep(delay + 5)

        # Now proceed with sending the request
        resp = self.send("GET", path, json, params)

        if not isinstance(resp, requests.Response):
            self.logger.error(f"Unexpected response type: {type(resp)}")
            return None

        if resp.status_code != 200:
            self.logger.error(f"Request failed with status code {resp.status_code}: {resp.text}")
            return None

        formatted_resp = format_json_response(resp, box_attrs=dict())
        return formatted_resp

    def post(self, path, json=None, params=None, data=None, headers=None):
        """
        Send a POST request to the ZDX API.

        Parameters:
        - path (str): API endpoint path.
        - json (dict, optional): Request payload. Defaults to None.
        - params (dict, optional): Query parameters. Defaults to None.
        - data (dict, optional): Request data. Defaults to None.
        - headers (dict, optional): Request headers. Defaults to None.

        Returns:
        - Response: Response object from the request.
        """

        should_wait, delay = self.rate_limiter.wait("POST")
        if should_wait:
            time.sleep(delay)

        # Now proceed with sending the request
        resp = self.send("POST", path, json, params, data=data, headers=headers)

        if not isinstance(resp, requests.Response):
            self.logger.error(f"Unexpected response type: {type(resp)}")
            return None

        if resp.status_code != 200:
            self.logger.error(f"Request failed with status code {resp.status_code}: {resp.text}")
            return None

        formatted_resp = format_json_response(resp, box_attrs=dict())
        return formatted_resp

    def delete(self, path, json=None, params=None):
        """
        Send a DELETE request to the ZDX API.

        Parameters:
        - path (str): API endpoint path.
        - json (dict, optional): Request payload. Defaults to None.
        - params (dict, optional): Query parameters. Defaults to None.

        Returns:
        - Response: Response object from the request.
        """

        should_wait, delay = self.rate_limiter.wait("DELETE")
        if should_wait:
            time.sleep(delay)

        # Now proceed with sending the request
        resp = self.send("DELETE", path, json, params)

        if not isinstance(resp, requests.Response):
            self.logger.error(f"Unexpected response type: {type(resp)}")
            return None

        if resp.status_code != 200:
            self.logger.error(f"Request failed with status code {resp.status_code}: {resp.text}")
            return None

        formatted_resp = format_json_response(resp, box_attrs=dict())
        return formatted_resp
