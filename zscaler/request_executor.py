import logging
import time
import uuid
from zscaler.oneapi_http_client import HTTPClient
from zscaler.oneapi_response import ZscalerAPIResponse
from zscaler.oneapi_oauth_client import OAuth
from zscaler.user_agent import UserAgent
from zscaler.error_messages import ERROR_MESSAGE_429_MISSING_DATE_X_RESET
from http import HTTPStatus
from zscaler.helpers import convert_keys_to_snake_case, convert_keys_to_camel_case
from zscaler.errors.response_checker import check_response_for_error
from zscaler.exceptions import exceptions
from zscaler.zcc.legacy import LegacyZCCClientHelper
from zscaler.ztw.legacy import LegacyZTWClientHelper
from zscaler.zdx.legacy import LegacyZDXClientHelper
from zscaler.zpa.legacy import LegacyZPAClientHelper
from zscaler.zia.legacy import LegacyZIAClientHelper
from zscaler.zwa.legacy import LegacyZWAClientHelper

logger = logging.getLogger('zscaler-sdk-python')


class RequestExecutor:
    """
    This class handles all of the requests sent by the Zscaler SDK Client (ZIA, ZPA, ZCC, ZDX, ZWA, ZTW).
    """

    BASE_URL = "https://api.zsapi.net"  # Default base URL for API calls

    def __init__(
        self,
        config,
        cache,
        http_client=None,
        zcc_legacy_client: LegacyZCCClientHelper = None,
        ztw_legacy_client: LegacyZTWClientHelper = None,
        zdx_legacy_client: LegacyZDXClientHelper = None,
        zpa_legacy_client: LegacyZPAClientHelper = None,
        zia_legacy_client: LegacyZIAClientHelper = None,
        zwa_legacy_client: LegacyZWAClientHelper = None,
    ):
        """
        Constructor for Request Executor object for Zscaler SDK Client.

        Args:
            config (dict): This dictionary contains the configuration of the Request Executor.
            cache (object): Cache object for storing request responses.
            http_client (object, optional): Custom HTTP client for making requests.
        """
        self.zcc_legacy_client = zcc_legacy_client
        self.ztw_legacy_client = ztw_legacy_client
        self.zdx_legacy_client = zdx_legacy_client
        self.zpa_legacy_client = zpa_legacy_client
        self.zia_legacy_client = zia_legacy_client
        self.zwa_legacy_client = zwa_legacy_client

        self.use_legacy_client = (
            zpa_legacy_client is not None
            or zia_legacy_client is not None
            or zwa_legacy_client is not None
            or zcc_legacy_client is not None
            or ztw_legacy_client is not None
            or zdx_legacy_client is not None
        )

        # Validate and set request timeout
        self._request_timeout = config["client"].get("requestTimeout", 240)  # Default to 240 seconds
        if self._request_timeout < 0:
            raise ValueError(f"Invalid request timeout: {self._request_timeout}. Must be greater than zero.")

        # Validate and set max retries for rate limiting
        self._max_retries = config["client"]["rateLimit"].get("maxRetries", 2)
        if self._max_retries < 0:
            raise ValueError(f"Invalid max retries: {self._max_retries}. Must be 0 or greater.")

        # Set configuration and cache
        self._config = config
        self._cache = cache

        # Retrieve cloud, service, and customer ID (optional)
        self.cloud = self._config["client"].get("cloud", "production").lower()
        self.sandbox_cloud = self._config["client"].get("sandboxCloud", "").lower()
        self.service = self._config["client"].get("service", "zia")  # Default to ZIA
        self.customer_id = self._config["client"].get("customerId")  # Optional for ZIA/ZCC
        self.microtenant_id = self._config["client"].get("microtenantId")  # Optional for ZIA/ZCC

        # OAuth2 setup
        self._oauth = OAuth(self, self._config)
        self._access_token = None

        # Set default headers from config
        self._default_headers = {
            "User-Agent": UserAgent(config["client"].get("userAgent", None)).get_user_agent_string(),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # Initialize the HTTP client, considering proxy and SSL context from config
        http_client_impl = http_client or HTTPClient
        self._http_client = http_client_impl(
            {
                "requestTimeout": self._request_timeout,
                "headers": self._default_headers,
                "proxy": self._config["client"].get("proxy"),
                "sslContext": self._config["client"].get("sslContext"),
            },
            zcc_legacy_client=self.zcc_legacy_client,
            ztw_legacy_client=self.ztw_legacy_client,
            zdx_legacy_client=self.zdx_legacy_client,
            zpa_legacy_client=self.zpa_legacy_client,
            zia_legacy_client=self.zia_legacy_client,
            zwa_legacy_client=self.zwa_legacy_client,
        )

        exceptions.raise_exception = self._config["client"].get("raiseException", False)
        self._custom_headers = {}

    def get_base_url(self, endpoint: str) -> str:
        """
        Gets the appropriate base URL based on the cloud value.

        Args:
            endpoint (str): The endpoint to be used to determine the base URL.
        Returns:
            str: The constructed base URL for API requests.
        """
        # logger.debug(f"Determining base URL for cloud: {self.cloud}")
        if "/zscsb" in endpoint:
            return f"https://csbapi.{self.sandbox_cloud}.net"
        if self.cloud and self.cloud != "production":
            return f"https://api.{self.cloud}.zsapi.net"
        return self.BASE_URL

    def get_service_type(self, url):
        if not url:
            raise ValueError("URL cannot be None or empty.")

        if "/zia" in url or "/zscsb" in url:
            return "zia"
        elif "/ztw" in url:
            return "ztw"
        elif "/zcc" in url:
            return "zcc"
        elif "/zdx" in url:
            return "zdx"
        elif "/zwa" in url:
            return "zwa"
        elif "/zpa" in url or "/mgmtconfig" in url:
            return "zpa"

        if self.use_legacy_client:
            url = self.remove_oneapi_endpoint_prefix(url)
            # Recheck for service type after removing the prefix
            if "/zia" in url or "/zscsb" in url:
                return "zia"
            elif "/ztw" in url:
                return "ztw"
            elif "/zcc" in url:
                return "zcc"
            elif "/zdx" in url:
                return "zdx"
            elif "/zwa" in url:
                return "zwa"
            elif "/zpa" in url or "/mgmtconfig" in url:
                return "zpa"

        raise ValueError(f"Unsupported service: {url}")

    def remove_oneapi_endpoint_prefix(self, endpoint: str) -> str:
        prefixes = ["/zia", "/zpa", "/zcc", "/ztw", "/zdx", "/zwa"]
        for prefix in prefixes:
            if endpoint.startswith(prefix):
                return endpoint[len(prefix) :]
        return endpoint

    def create_request(
        self,
        method: str,
        endpoint: str,
        body: dict = None,
        headers: dict = None,
        params: dict = None,
        use_raw_data_for_body: bool = False,
    ):
        try:
            service_type = self.get_service_type(endpoint)
        except ValueError as e:
            logger.error(f"Service detection failed: {e}")
            raise

        body = body or {}
        headers = headers or {}
        params = params or {}

        if self.use_legacy_client:
            endpoint = self.remove_oneapi_endpoint_prefix(endpoint)

            if service_type == "zpa":
                base_url = self.zpa_legacy_client.get_base_url(endpoint)
            elif service_type == "zia":
                base_url = self.zia_legacy_client.get_base_url(endpoint)
            elif service_type == "ztw":
                base_url = self.ztw_legacy_client.get_base_url(endpoint)
            elif service_type == "zcc":
                base_url = self.zcc_legacy_client.get_base_url(endpoint)
            elif service_type == "zdx":
                base_url = self.zdx_legacy_client.get_base_url(endpoint)
            elif service_type == "zwa":
                base_url = self.zwa_legacy_client.get_base_url(endpoint)
            else:
                base_url = self.get_base_url(endpoint)
        else:
            base_url = self.get_base_url(endpoint)

        final_url = f"{base_url}/{endpoint.lstrip('/')}"

        headers = self._prepare_headers(headers, endpoint)
        # [MODIFIED] Pass service_type to _prepare_params
        params = self._prepare_params(service_type, endpoint, params, body)
        final_url, params = self._extract_and_append_query_params(final_url, params)

        if "/zscsb" in endpoint:
            sandbox_token = self._config["client"].get("sandboxToken")
            if not sandbox_token:
                raise ValueError("Missing required sandboxToken in config.")
            params["api_token"] = sandbox_token

        request = {
            "method": method,
            "url": final_url,
            "params": params,
            "headers": headers,
            "uuid": uuid.uuid4(),
            "service_type": service_type,
        }
        if use_raw_data_for_body:
            request["data"] = body
        else:
            json_payload = self._prepare_body(endpoint, body)
            request["json"] = json_payload
        return request, None

    def _prepare_headers(self, headers, endpoint=""):
        headers = {**self._default_headers, **(self._custom_headers or {}), **headers}
        if "/zscsb" not in endpoint and not self.use_legacy_client:
            headers["Authorization"] = f"Bearer {self._oauth._get_access_token()}"
        return headers

    def _prepare_body(self, endpoint, body):
        if not isinstance(body, dict):
            return body

        # Ensure ZDX remains snake_case without affecting other services
        if self.use_legacy_client and self.zdx_legacy_client:
            return body  # Do not convert anything, just return as-is

        # Preserve existing logic for other services
        if body:
            body = convert_keys_to_camel_case(body)

        if "/zpa/" in endpoint and "/reorder" in endpoint and isinstance(body, list):
            return body

        return body

    def _prepare_params(self, service_type, endpoint, params, body):
        if not isinstance(params, dict):
            return params

        if self.use_legacy_client and self.zdx_legacy_client:
            return params

        # If it's ZPA, handle pagesize special rules
        if service_type.lower() == "zpa":
            # If it's specifically /emergencyAccess/users ...
            if "/emergencyAccess/users" in endpoint:
                # Convert everything to camelCase
                converted = convert_keys_to_camel_case(params)
                # Then rename `pagesize` -> `pageSize` if it exists
                if "pagesize" in converted:
                    converted["pageSize"] = converted.pop("pagesize")
                params = converted
            else:
                # For all other ZPA endpoints, keep `pagesize` in lowercase
                psize_value = None
                if "page_size" in params:
                    psize_value = params.pop("page_size")
                elif "pagesize" in params:
                    psize_value = params.pop("pagesize")

                converted = convert_keys_to_camel_case(params)

                if psize_value is not None:
                    converted["pagesize"] = psize_value

                params = converted

            # Finally, handle microtenant (unchanged)
            microtenant_id = self._get_microtenant_id(body, params)
            if microtenant_id:
                params["microtenantId"] = microtenant_id

        else:
            # Normal param conversion if not ZPA
            params = convert_keys_to_camel_case(params)
            params.pop("microtenantId", None)

        return params

    def _get_microtenant_id(self, body, params):
        if body and isinstance(body, dict) and "microtenantId" in body and body["microtenantId"]:
            return body["microtenantId"]
        if params and "microtenantId" in params and params["microtenantId"]:
            return params["microtenantId"]
        return self.microtenant_id

    def execute(self, request, response_type=None, return_raw_response=False):
        """
        High-level request execution method.
        Args:
            request (dict): Request dictionary.
            response_type (type): Expected data type.
        Returns:
            Tuple (API response, Error)
        """
        try:
            request, response, response_body, error = self.fire_request(request)
        except Exception as ex:
            logger.error(f"Exception during HTTP request: {ex}")
            return None, ex

        if response is None and error is None:
            return None, None  # silently return None without manufacturing errors

        if error:
            # logger.error(f"Error during request execution: {error}")
            return None, error

        if response.status_code == 204:
            logger.debug(f"Received 204 No Content from {request['url']}")
            return None, None

        # If raw response is requested, return it for file download purposes
        if return_raw_response:
            return response, None

        try:
            response_data, error = check_response_for_error(request["url"], response, response_body)
        except Exception as ex:
            logger.error(f"Exception while checking response for errors: {ex}")
            return None, ex

        if error:
            # logger.error(f"Error in HTTP response: {error}")
            return None, error

        logger.debug(f"Successful response from {request['url']}")
        logger.debug(f"Response Data: {response_data}")

        if isinstance(response_data, (dict, list)):
            response_data = convert_keys_to_snake_case(response_data)

        return (
            ZscalerAPIResponse(
                request_executor=self,
                req=request,
                res_details=response,
                response_body=response_body,
                data_type=response_type,
                service_type=request.get("service_type", ""),
            ),
            None,
        )

    def _extract_and_append_query_params(self, url, params):
        """
        Extracts query parameters from the URL and appends them to the params dictionary.

        Args:
            url (str): The URL containing potential query parameters.
            params (dict): The existing parameters dictionary.

        Returns:
            tuple: Cleaned URL and updated parameters dictionary with query parameters from the URL.
        """
        from urllib.parse import urlparse, parse_qs, urlunparse

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Flatten the query_params dictionary and update the params
        for key, value in query_params.items():
            if key not in params:
                params[key] = value[0] if len(value) == 1 else value

        # Reconstruct the URL without query parameters
        cleaned_url = urlunparse(parsed_url._replace(query=""))

        # Return the cleaned URL and updated params dictionary
        return cleaned_url, params

    def _cache_enabled(self):
        return self._config["client"]["cache"]["enabled"] == True

    def fire_request(self, request):
        """
        Send request using HTTP client.

        Args:
            request (dict): HTTP request in dictionary format.

        Returns:
            request, response, response_body, error
        """
        is_sandbox_request = "/zscsb" in request["url"]

        # Pass both URL and params to create_key
        url_cache_key = self._cache.create_key(request["url"], request["params"])
        if self._cache_enabled() and not is_sandbox_request:
            # Remove cache entry if not a GET call
            if request["method"].upper() != "GET":
                logger.debug(f"Deleting cache entry for non-GET request: {url_cache_key}")
                self._cache.delete(url_cache_key)

            # Check if response exists in cache
            if self._cache.contains(url_cache_key):
                logger.info(f"Cache hit for URL: {request['url']}")
                response, response_body = self._cache.get(url_cache_key)
                return request, response, response_body, None
            else:
                logger.debug(f"No cache entry found for URL: {request['url']}")

        # Send Actual Request
        try:
            request, response, response_body, error = self.fire_request_helper(request, 0, time.time())
        except Exception as e:
            logger.error(f"Request execution failed: {e}")
            return request, None, None, e

        if self._cache_enabled() and not is_sandbox_request:
            if not error and request["method"].upper() == "GET" and response and response.status_code < 300:
                logger.info(f"Caching response for URL: {request['url']}")
                self._cache.add(url_cache_key, (response, response_body))

        return request, response, response_body, error

    def fire_request_helper(self, request, attempts, request_start_time):
        """
        Helper method to perform HTTP call with retries if needed.

        Args:
            request (dict): HTTP request representation.
            attempts (int): Number of attempted HTTP calls so far.
            request_start_time (float): Original start time of request.

        Returns:
            Tuple of (request, response object, response body, error).
        """
        current_req_start_time = time.time()
        max_retries = self._max_retries
        req_timeout = self._request_timeout

        # Check if total elapsed time exceeds the configured request timeout
        if req_timeout > 0 and (current_req_start_time - request_start_time) > req_timeout:
            logger.warning("Request Timeout exceeded.")
            return None, None, None, Exception("Request Timeout exceeded.")

        # Perform the actual HTTP request
        response, error = self._http_client.send_request(request)

        # If a low-level error occurred (network, request construction, etc.)
        if error:
            return request, response, response.text if response else None, error

        # Check for 401 -> Trigger re-auth if we still have retries left
        if response.status_code == 401:
            # We only want to attempt refreshing the token if we haven't hit max_retries
            if attempts < max_retries:
                logger.info("Got 401 response; clearing token and re-authenticating.")
                self._oauth.clear_access_token()

                try:
                    fresh_token = self._oauth._get_access_token()
                except Exception as e:
                    # If re-auth fails, return immediately
                    logger.error(f"Token refresh failed after 401: {e}")
                    return request, response, response.text, e

                # Update the request with the new token
                request["headers"]["Authorization"] = f"Bearer {fresh_token}"
                attempts += 1
                return self.fire_request_helper(request, attempts, request_start_time)
            else:
                logger.error("401 Unauthorized - token refresh attempts exhausted.")
                return request, response, response.text, Exception("401 Unauthorized - token refresh attempts exhausted.")

        # Handle “retryable” statuses such as 429, 503, etc.
        if attempts < max_retries and self.is_retryable_status(response.status_code):
            backoff_seconds = self.get_retry_after(response.headers, logger)
            if backoff_seconds is None:
                return None, response, response.text, Exception(ERROR_MESSAGE_429_MISSING_DATE_X_RESET)

            logger.info(f"Hit rate limit or retryable status {response.status_code}. "
                        f"Retrying request in {backoff_seconds} seconds.")
            time.sleep(backoff_seconds)
            attempts += 1
            return self.fire_request_helper(request, attempts, request_start_time)

        # If we reach here, no further retries; return whatever we got
        return request, response, response.text, None

    def is_retryable_status(self, status):
        """
        Checks if HTTP status is retryable.

        Retryable statuses: 408, 409, 412, 429, 500, 502, 503, 504
        """
        return status is not None and status in (
            HTTPStatus.REQUEST_TIMEOUT,
            HTTPStatus.CONFLICT,
            HTTPStatus.PRECONDITION_FAILED,
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        )

    def is_too_many_requests(self, status, response):
        """
        Determines if HTTP request has been made too many times

        Args:
            status (int): HTTP response status code
            response (json): Response Body

        Returns:
            bool: Returns True if this request has been called too many times
        """
        return response is not None and status == HTTPStatus.TOO_MANY_REQUESTS

    def calculate_backoff(self, retry_limit_reset, date_time):
        """
        Calculate the backoff time based on rate limit reset and date time.

        Args:
            retry_limit_reset: The reset time from X-Rate-Limit-Reset header.
            date_time: The current time from the Date header.

        Returns:
            int: The number of seconds to backoff.
        """
        return retry_limit_reset - date_time + 1

    def pause_for_backoff(self, backoff_time):
        """
        Pauses the execution for the backoff period.

        Args:
            backoff_time (int): Number of seconds to pause.
        """
        time.sleep(float(backoff_time))

    def set_custom_headers(self, headers):
        """
        Set custom headers for all future requests.
        """
        logger.debug(f"Setting custom headers: {headers}")
        self._custom_headers.update(headers)

    def set_session(self, session):
        # logger.debug("Setting HTTP client session.")
        self._http_client.set_session(session)

    def clear_custom_headers(self):
        """
        Clear custom headers set for future requests.
        """
        logger.debug("Clearing custom headers.")
        self._custom_headers.clear()

    def get_custom_headers(self):
        """
        Get the current custom headers.
        """
        logger.debug("Getting custom headers.")
        return self._custom_headers

    def get_retry_after(self, headers, logger):
        retry_limit_reset_header = (
            headers.get("x-ratelimit-reset") or 
            headers.get("X-RateLimit-Reset") or
            headers.get("RateLimit-Reset") or
            
            # ZCC Specific Rate Limiting Headers (LegacyZCCClientHelper)
            headers.get("X-Rate-Limit-Retry-After-Seconds") or # ZCC /downloadDevices Rate Limiting Header (LegacyZCCClientHelper)
            headers.get("X-Rate-Limit-Remaining") # (LegacyZCCClientHelper)
        )
        retry_after = headers.get("Retry-After") or headers.get("retry-after")

        if retry_after:
            try:
                return int(retry_after.strip("s")) + 1  # Add 1 second padding
            except ValueError:
                logger.error(f"Error parsing Retry-After header: {retry_after}")
                return None

        if retry_limit_reset_header is not None:
            try:
                reset_seconds = float(retry_limit_reset_header)
                return reset_seconds + 1  # Add 1 second padding
            except ValueError:
                logger.error(f"Error parsing x-ratelimit-reset header: {retry_limit_reset_header}")
                return None

        logger.error("Missing Retry-After and X-Rate-Limit-Reset headers.")
        return None
