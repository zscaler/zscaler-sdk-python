"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from __future__ import annotations

import logging
import os
import time
import threading
from typing import Optional, Dict, Any, Type, List, TYPE_CHECKING
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

import requests
from zscaler import __version__
from zscaler.cache.cache import Cache
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.user_agent import UserAgent
from zscaler.logger import setup_logging, dump_request, dump_response

setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")

# Import all AIGuard API classes for type hints only (to avoid circular imports)
if TYPE_CHECKING:
    from zscaler.zaiguard.policy_detection import PolicyDetectionAPI


def _sanitize_url_for_logging(url: str) -> str:
    """
    Return a version of the URL safe for logging by removing embedded credentials
    and masking obvious secret-bearing query parameters.
    """
    if not url:
        return url

    parsed = urlparse(url)

    # Strip any user:pass@ from netloc
    netloc = parsed.hostname or ""
    if parsed.port:
        netloc = f"{netloc}:{parsed.port}"

    # Mask common sensitive query parameters
    sensitive_keys = {"api_key", "apikey", "access_token", "token", "key", "secret"}
    query_params = []
    for k, v in parse_qsl(parsed.query, keep_blank_values=True):
        if k.lower() in sensitive_keys:
            query_params.append((k, "***"))
        else:
            query_params.append((k, v))
    sanitized_query = urlencode(query_params)

    sanitized = parsed._replace(netloc=netloc, query=sanitized_query)
    return urlunparse(sanitized)


class LegacyZGuardClientHelper:
    """
    A Controller to access Endpoints in the Zscaler AI Guard API.

    The AIGuard object stores the API key and simplifies access to the AI Guard platform.

    Attributes:
        api_key (str): The AIGuard API key (Bearer token).
        cloud (str): The Zscaler cloud for your tenancy. Default is 'us1'.
        timeout (int): Request timeout in seconds. Default is 240.

    """

    _vendor = "Zscaler"
    _product = "Zscaler AI Guard"
    _build = __version__
    _env_base = "AIGUARD"
    url = "https://api.us1.zseclipse.net"
    env_cloud = "us1"

    def __init__(
        self,
        cloud: str = "us1",
        timeout: int = 240,
        cache: Optional[Cache] = None,
        fail_safe: bool = False,
        request_executor_impl: Optional[Type] = None,
        auto_retry_on_rate_limit: bool = True,
        max_rate_limit_retries: int = 3,
        **kw: Any
    ) -> None:
        self.api_key = kw.get("api_key", os.getenv(f"{self._env_base}_API_KEY"))

        # Set cloud environment (default to us1)
        self.env_cloud = cloud or kw.get("cloud") or os.getenv(f"{self._env_base}_CLOUD", "us1")

        # URL construction
        self.url = (
            kw.get("override_url")
            or os.getenv(f"{self._env_base}_OVERRIDE_URL")
            or f"https://api.{self.env_cloud}.zseclipse.net"
        )

        self.timeout = timeout
        self.fail_safe = fail_safe
        self.conv_box = True

        # Initialize cache
        if cache:
            self.cache = cache
        else:
            self.cache = NoOpCache()

        # Setup logging
        setup_logging(logger_name="zscaler-sdk-python")
        self.logger = logging.getLogger("zscaler-sdk-python")

        # Validate API key
        if not self.api_key:
            raise ValueError(
                f"API key is required. Please set 'api_key' or '{self._env_base}_API_KEY' environment variable."
            )

        self.logger.info(f"Initializing {self._product} client")
        self.logger.debug(f"Base URL: {_sanitize_url_for_logging(self.url)}")
        # Do not log any portion of the API key to avoid exposing sensitive information
        self.logger.debug("API key configured")

        # Setup user agent
        ua = UserAgent()
        self.user_agent = ua.get_user_agent_string()

        # Setup headers
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }

        # Initialize rate limiting (AIGuard uses response-based throttling)
        self.auto_retry_on_rate_limit = auto_retry_on_rate_limit
        self.max_rate_limit_retries = max_rate_limit_retries
        self._rate_limit_lock = threading.Lock()
        self._request_count_wait_until = 0  # Timestamp when "rq" limit resets
        self._content_size_wait_until = 0   # Timestamp when "cs" limit resets

        # Rate limit statistics
        self._total_throttles = 0
        self._rq_throttles = 0
        self._cs_throttles = 0

        # Initialize request executor
        if request_executor_impl:
            self.request_executor = request_executor_impl(self)
        else:
            from zscaler.request_executor import RequestExecutor

            # Create a minimal config for the request executor
            config = {
                "client": {
                    "requestTimeout": timeout,
                    "rateLimit": {"maxRetries": 2},
                    "cache": {"enabled": False},
                    "service": "zguard",
                    "cloud": self.env_cloud,
                }
            }

            self.request_executor = RequestExecutor(
                config=config,
                cache=self.cache,
                http_client=None,
                zguard_legacy_client=self,
            )

        self._session = None

    @property
    def policy_detection(self) -> "PolicyDetectionAPI":
        """
        The interface object for the AIGuard Policy Detection API.

        Returns:
            PolicyDetectionAPI: Interface for policy detection operations
        """
        from zscaler.zaiguard.policy_detection import PolicyDetectionAPI

        return PolicyDetectionAPI(self.request_executor)

    def _should_wait_before_request(self) -> Optional[float]:
        """
        Check if we should wait before making a new request based on previous rate limits.

        Returns:
            Optional[float]: Seconds to wait, or None if no wait needed
        """
        with self._rate_limit_lock:
            now = time.time()

            # Check request count limit
            rq_wait = max(0, self._request_count_wait_until - now)

            # Check content size limit
            cs_wait = max(0, self._content_size_wait_until - now)

            max_wait = max(rq_wait, cs_wait)

            if max_wait > 0:
                logger.debug(f"Pre-request rate limit check: waiting {max_wait:.1f}s")
                return max_wait

            return None

    def _wait_if_rate_limited(self) -> bool:
        """
        Wait if needed based on previous rate limits (proactive).

        Returns:
            bool: True if wait was applied, False otherwise
        """
        wait_time = self._should_wait_before_request()
        if wait_time and wait_time > 0:
            logger.info(f"AIGuard proactive rate limit wait: {wait_time:.1f}s")
            time.sleep(wait_time)
            return True
        return False

    def _handle_throttling_details(self, throttling_details: List[Any]) -> bool:
        """
        Handle throttling details from API response.

        Args:
            throttling_details: List of RateLimitThrottlingDetail from API response

        Returns:
            bool: True if rate limiting was applied, False otherwise
        """
        if not throttling_details or len(throttling_details) == 0:
            return False

        with self._rate_limit_lock:
            now = time.time()
            max_wait_seconds = 0
            throttle_info = []

            for throttle in throttling_details:
                self._total_throttles += 1

                # Calculate wait time
                retry_after_millis = getattr(throttle, 'retry_after_millis', None)
                wait_seconds = (retry_after_millis or 0) / 1000.0
                max_wait_seconds = max(max_wait_seconds, wait_seconds)

                metric = getattr(throttle, 'metric', None)
                rlc_id = getattr(throttle, 'rlc_id', None)

                # Track by metric type
                if metric == "rq":
                    self._rq_throttles += 1
                    self._request_count_wait_until = now + wait_seconds
                    throttle_info.append(f"Request rate limit (wait {wait_seconds:.1f}s)")

                elif metric == "cs":
                    self._cs_throttles += 1
                    self._content_size_wait_until = now + wait_seconds
                    throttle_info.append(f"Content size limit (wait {wait_seconds:.1f}s)")

                else:
                    throttle_info.append(f"Unknown metric '{metric}' (wait {wait_seconds:.1f}s)")

                # Log details
                logger.warning(
                    f"AIGuard rate limit triggered: "
                    f"rlcId={rlc_id}, metric={metric}, "
                    f"retryAfter={retry_after_millis}ms"
                )

            # Apply rate limiting if auto_retry is enabled
            if self.auto_retry_on_rate_limit and max_wait_seconds > 0:
                logger.info(
                    f"AIGuard rate limit: {', '.join(throttle_info)}. "
                    f"Sleeping for {max_wait_seconds:.1f} seconds..."
                )
                time.sleep(max_wait_seconds)
                return True

            elif max_wait_seconds > 0:
                logger.warning(
                    f"AIGuard rate limit detected but auto_retry disabled: "
                    f"{', '.join(throttle_info)}. "
                    f"Application should wait {max_wait_seconds:.1f} seconds before next request."
                )
                return True

        return False

    def get_rate_limit_stats(self) -> Dict[str, Any]:
        """
        Get rate limiting statistics.

        Returns:
            dict: Statistics about rate limiting including:
                - total_throttles: Total number of times throttled
                - request_count_throttles: Number of request count throttles
                - content_size_throttles: Number of content size throttles
                - currently_limited: Whether currently rate limited
        """
        with self._rate_limit_lock:
            return {
                "total_throttles": self._total_throttles,
                "request_count_throttles": self._rq_throttles,
                "content_size_throttles": self._cs_throttles,
                "currently_limited": self._should_wait_before_request() is not None,
            }

    def reset_rate_limit_stats(self) -> None:
        """Reset rate limiting statistics."""
        with self._rate_limit_lock:
            self._total_throttles = 0
            self._rq_throttles = 0
            self._cs_throttles = 0
            logger.debug("AIGuard rate limit statistics reset")

    def clear_rate_limits(self) -> None:
        """
        Clear all active rate limits (use with caution).

        This will allow requests to proceed even if the API indicated you should wait.
        """
        with self._rate_limit_lock:
            self._request_count_wait_until = 0
            self._content_size_wait_until = 0
            logger.info("AIGuard rate limits cleared")

    def get_base_url(self, endpoint: str = "") -> str:
        """
        Returns the base URL for the AIGuard API.

        Args:
            endpoint: The API endpoint (not used, kept for compatibility)

        Returns:
            str: The base URL
        """
        return self.url

    def get_jsessionid(self, request: requests.PreparedRequest) -> Optional[str]:
        """
        Returns None for AIGuard as it uses Bearer token authentication.
        This method exists for compatibility with the SDK framework.

        Args:
            request: The prepared request object

        Returns:
            None
        """
        return None

    def set_auth_header(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """
        Sets the Authorization header with the Bearer token for AIGuard API requests.

        Args:
            request: The prepared request object

        Returns:
            requests.PreparedRequest: The request with Authorization header set
        """
        if self.api_key:
            request.headers["Authorization"] = f"Bearer {self.api_key}"

        # Set Content-Type for JSON requests
        if request.body and not request.headers.get("Content-Type"):
            request.headers["Content-Type"] = "application/json"

        # Set User-Agent
        request.headers["User-Agent"] = self.user_agent

        return request

    def send(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Send an HTTP request to the AIGuard API with automatic rate limiting.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            path: API endpoint path
            json: JSON payload for the request body
            params: Query parameters
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response: The HTTP response object
        """
        # Proactive rate limiting - wait if we know we should from previous responses
        self._wait_if_rate_limited()

        url = f"{self.url}{path}"

        # Prepare request
        req = requests.Request(method=method.upper(), url=url, json=json, params=params, **kwargs)
        prepared = req.prepare()

        # Set authentication and headers
        prepared = self.set_auth_header(prepared)

        # Log request (with proper parameters for dump_request)
        import uuid
        import time
        request_uuid = str(uuid.uuid4())
        start_time = time.time()

        dump_request(
            self.logger,
            url=url,
            method=method.upper(),
            json=json,
            params=params or {},
            headers=dict(prepared.headers),
            request_uuid=request_uuid
        )

        # Create session if not exists
        if not hasattr(self, "_session") or self._session is None:
            self._session = requests.Session()

        # Send request
        response = self._session.send(prepared, timeout=self.timeout)

        # Log response (with proper parameters)
        dump_response(
            self.logger,
            url=url,
            method=method.upper(),
            resp=response,
            params=params or {},
            request_uuid=request_uuid,
            start_time=start_time,
            from_cache=False
        )

        return response

    """
    Misc
    """

    def set_custom_headers(self, headers: Dict[str, str]) -> None:
        """Set custom headers for requests."""
        self.request_executor.set_custom_headers(headers)

    def clear_custom_headers(self) -> None:
        """Clear custom headers."""
        self.request_executor.clear_custom_headers()

    def get_custom_headers(self) -> Dict[str, str]:
        """Get custom headers."""
        return self.request_executor.get_custom_headers()

    def get_default_headers(self) -> Dict[str, str]:
        """Get default headers."""
        return self.request_executor.get_default_headers()

    def __enter__(self):
        """Context manager entry."""
        if not hasattr(self, "_session") or self._session is None:
            self._session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if hasattr(self, "_session") and self._session is not None:
            self._session.close()
            self._session = None
