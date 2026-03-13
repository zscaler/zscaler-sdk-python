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
import random
import time
import uuid
from time import sleep
from typing import Optional, Dict, Any, Tuple, Type, Callable, TYPE_CHECKING

import requests
from zscaler import __version__
from zscaler.cache.cache import Cache
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.logger import setup_logging, dump_request, dump_response
from zscaler.errors.response_checker import check_response_for_error

setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")

if TYPE_CHECKING:
    from zscaler.ztb.alarms import AlarmsAPI
    from zscaler.ztb.api_key import APIKeyAuthRouterAPI
    from zscaler.ztb.app_connector_config import AppConnectorConfigAPI
    from zscaler.ztb.devices import DevicesAPI
    from zscaler.ztb.groups_router import GroupsRouterAPI
    from zscaler.ztb.logs import LogsAPI
    from zscaler.ztb.policy_comments import PolicyCommentsAPI
    from zscaler.ztb.ransomware_kill import RansomwareKillAPI
    from zscaler.ztb.site import SiteAPI
    from zscaler.ztb.site2site_vpn import Site2SiteVPNAPI
    from zscaler.ztb.template_router import TemplateRouterAPI

# ASSUMPTION: ZTB rate limits are unknown.  We use conservative defaults.
_DEFAULT_GET_LIMIT = 5
_DEFAULT_POST_PUT_DELETE_LIMIT = 5
_DEFAULT_GET_FREQ = 1
_DEFAULT_POST_PUT_DELETE_FREQ = 1

_MAX_RETRY_BACKOFF_SECONDS = 30
_DEFAULT_MAX_RETRIES = 5

_RETRYABLE_5XX = frozenset({502, 503, 504})

_ZTB_LOGIN_PATH = "/api/v3/api-key-auth/login"


class LegacyZTBClientHelper:
    """
    A Controller to access Endpoints in the Zero Trust Branch (ZTB) API.

    ZTB authenticates via API key: the client calls
    ``POST /api/v3/api-key-auth/login`` with ``{"api_key": "..."}`` and
    receives a ``delegate_token`` used as ``Authorization: Bearer <token>``
    for all subsequent requests.

    If a request returns 401, the client automatically re-authenticates
    and retries once.

    Attributes:
        api_key (str): The ZTB API key (created in the ZTB UI).
        cloud (str): The Zscaler cloud subdomain for your tenancy
            (e.g. ``zscalerbd-api``). Used to construct the base URL:
            ``https://{cloud}.goairgap.com``

        override_url (str):
            If supplied, this attribute can be used to override the production URL
            that is derived from supplying the ``cloud`` attribute. Use this attribute
            if you have a non-standard tenant URL (e.g. internal test instance etc).
            When using this attribute, there is no need to supply the ``cloud``
            attribute. The override URL will be prepended to the API endpoint suffixes.
            The protocol must be included i.e. ``https://``.
    """

    _vendor = "Zscaler"
    _product = "Zero Trust Branch"
    _build = __version__
    _env_base = "ZTB"
    url = "https://goairgap.com"
    env_cloud = ""

    def __init__(
        self,
        cloud: str,
        timeout: int = 240,
        cache: Optional[Cache] = None,
        fail_safe: bool = False,
        request_executor_impl: Optional[Type] = None,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        **kw: Any,
    ) -> None:
        from zscaler.request_executor import RequestExecutor

        # --- API key resolution ---
        self.api_key: Optional[str] = kw.get("api_key") or os.getenv(f"{self._env_base}_API_KEY")
        if not self.api_key:
            raise ValueError(
                "A ZTB API key is required. Supply 'api_key' kwarg or set the " "ZTB_API_KEY environment variable."
            )

        # --- Cloud ---
        self.env_cloud = cloud or kw.get("cloud") or os.getenv(f"{self._env_base}_CLOUD")
        if not self.env_cloud:
            raise ValueError(
                f"Cloud environment must be set via the 'cloud' argument or the "
                f"{self._env_base}_CLOUD environment variable."
            )

        # --- URL construction ---
        self.url = (
            kw.get("override_url") or os.getenv(f"{self._env_base}_OVERRIDE_URL") or f"https://{self.env_cloud}.goairgap.com"
        )

        # --- Misc ---
        self.partner_id: Optional[str] = kw.get("partner_id") or os.getenv("ZSCALER_PARTNER_ID")
        self.timeout: int = timeout
        self.fail_safe: bool = fail_safe
        self.max_retries: int = max_retries

        # --- Delegate token (populated by authenticate()) ---
        self._delegate_token: Optional[str] = None

        # --- Cache ---
        cache_enabled = os.environ.get("ZSCALER_CLIENT_CACHE_ENABLED", "false").lower() == "true"
        self.cache: Cache = NoOpCache()
        if cache is None and cache_enabled:
            ttl = int(os.environ.get("ZSCALER_CLIENT_CACHE_DEFAULT_TTL", 3600))
            tti = int(os.environ.get("ZSCALER_CLIENT_CACHE_DEFAULT_TTI", 1800))
            self.cache = ZscalerCache(ttl=ttl, tti=tti)
        elif isinstance(cache, Cache):
            self.cache = cache

        # --- User-Agent ---
        ua = UserAgent()
        self.user_agent: str = ua.get_user_agent_string()

        # --- Rate limiter ---
        self.rate_limiter = RateLimiter(
            get_limit=_DEFAULT_GET_LIMIT,
            post_put_delete_limit=_DEFAULT_POST_PUT_DELETE_LIMIT,
            get_freq=_DEFAULT_GET_FREQ,
            post_put_delete_freq=_DEFAULT_POST_PUT_DELETE_FREQ,
        )

        # --- Default headers ---
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        if self.partner_id:
            self.headers["x-partner-id"] = self.partner_id

        # --- Authenticate (obtain delegate_token) ---
        self.authenticate()

        # --- RequestExecutor config block ---
        self.config: Dict[str, Any] = {
            "client": {
                "cloud": self.env_cloud or "",
                "partnerId": self.partner_id or "",
                "requestTimeout": self.timeout,
                "rateLimit": {"maxRetries": self.max_retries},
                "cache": {"enabled": cache_enabled},
            }
        }
        self.request_executor = (request_executor_impl or RequestExecutor)(self.config, self.cache, ztb_legacy_client=self)

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self) -> None:
        """
        Authenticates with the ZTB API by posting the api_key to
        ``/api/v3/api-key-auth/login`` and extracts the ``delegate_token``
        from the response.
        """
        url = f"{self.url}{_ZTB_LOGIN_PATH}"
        method = "POST"
        payload = {"api_key": self.api_key}
        request_uuid = str(uuid.uuid4())
        start_time = time.time()

        dump_request(logger, url, method, payload, {}, self.headers, request_uuid)

        resp = requests.post(
            url,
            json=payload,
            headers=self.headers,
            timeout=self.timeout,
        )

        dump_response(logger, url, method, resp, {}, request_uuid, start_time)

        parsed_response, err = check_response_for_error(url, resp, resp.text)
        if err:
            raise err

        try:
            result = parsed_response["result"]
            token = result["delegate_token"]
            if not token:
                raise KeyError("empty delegate_token")
        except (KeyError, TypeError) as e:
            raise ValueError(
                f"Unexpected authentication response shape. "
                f'Expected {{"result": {{"delegate_token": "..."}}}}, '
                f"got: {parsed_response}"
            ) from e

        self._delegate_token = token
        logger.info("ZTB authentication successful. Delegate token obtained.")

    # ------------------------------------------------------------------
    # Token helpers
    # ------------------------------------------------------------------

    def _build_auth_header_value(self) -> str:
        """Build the ``Authorization: Bearer <delegate_token>`` header value."""
        if not self._delegate_token:
            raise ValueError("No ZTB delegate token available. Call authenticate() first.")
        return f"Bearer {self._delegate_token}"

    # ------------------------------------------------------------------
    # URL helpers
    # ------------------------------------------------------------------

    def get_base_url(self, endpoint: str = "") -> str:
        """Return the base URL for ZTB API requests."""
        return self.url

    # ------------------------------------------------------------------
    # Core request method
    # ------------------------------------------------------------------

    def send(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Tuple[requests.Response, Dict[str, Any]]:
        """
        Send an HTTP request to the ZTB API.

        Uses ``Authorization: Bearer <delegate_token>`` obtained from the
        login flow. On 401 responses, automatically re-authenticates and
        retries once.

        Also handles:
          - 429 (Too Many Requests) with Retry-After parsing and exponential backoff.
          - 5xx transient errors (502/503/504) with exponential backoff.
          - Transient network errors with exponential backoff.

        Returns:
            Tuple of (response, request_context_dict).
        """
        url = f"{self.url}/{path.lstrip('/')}"
        attempts = 0
        did_reauth = False

        while attempts <= self.max_retries:
            try:
                merged_headers = self.headers.copy()
                merged_headers.update(headers or {})
                merged_headers["Authorization"] = self._build_auth_header_value()

                request_uuid = str(uuid.uuid4())
                start_time = time.time()

                dump_request(logger, url, method, json, params, merged_headers, request_uuid)

                resp = requests.request(
                    method=method,
                    url=url,
                    json=json,
                    data=data,
                    params=params,
                    headers=merged_headers,
                    timeout=self.timeout,
                )

                dump_response(logger, url, method, resp, params, request_uuid, start_time)

                # --- 401 handling: re-authenticate and retry once ---
                if resp.status_code == 401 and not did_reauth:
                    logger.warning("Received 401 Unauthorized. Re-authenticating and retrying...")
                    self.authenticate()
                    did_reauth = True
                    continue

                # --- 429 handling ---
                if resp.status_code == 429:
                    sleep_time = self._parse_retry_after(resp.headers, attempts)
                    logger.warning(
                        "Rate limit exceeded (429). Retrying in %.1f seconds. " "(Attempt %d/%d)",
                        sleep_time,
                        attempts + 1,
                        self.max_retries,
                    )
                    sleep(sleep_time)
                    attempts += 1
                    continue

                # --- Retryable 5xx ---
                if resp.status_code in _RETRYABLE_5XX:
                    sleep_time = self._exponential_backoff(attempts)
                    logger.warning(
                        "Transient server error (%d). Retrying in %.1f seconds. " "(Attempt %d/%d)",
                        resp.status_code,
                        sleep_time,
                        attempts + 1,
                        self.max_retries,
                    )
                    sleep(sleep_time)
                    attempts += 1
                    continue

                _, err = check_response_for_error(url, resp, resp.text)
                if err:
                    raise err

                return resp, {
                    "method": method,
                    "url": url,
                    "params": params or {},
                    "headers": merged_headers,
                    "json": json or {},
                }

            except requests.RequestException as e:
                if attempts >= self.max_retries:
                    logger.error("Request to %s failed after %d retries: %s", url, self.max_retries, e)
                    raise
                sleep_time = self._exponential_backoff(attempts)
                logger.warning(
                    "Network error for %s: %s. Retrying in %.1f seconds (%d/%d)",
                    url,
                    e,
                    sleep_time,
                    attempts + 1,
                    self.max_retries,
                )
                sleep(sleep_time)
                attempts += 1

        raise ValueError("Request execution failed after maximum retries.")

    # ------------------------------------------------------------------
    # Retry helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_retry_after(headers: Dict[str, str], attempt: int) -> float:
        """
        Parse the Retry-After header.  Handles values like ``"0 seconds"``,
        ``"2"``, or plain integers.  Falls back to exponential backoff if the
        header is missing or unparseable.
        """
        raw = headers.get("Retry-After") or headers.get("retry-after")
        if raw is not None:
            cleaned = raw.replace("seconds", "").replace("second", "").strip()
            try:
                parsed = int(cleaned)
                return max(parsed, 1)
            except (ValueError, TypeError):
                pass
        return LegacyZTBClientHelper._exponential_backoff(attempt)

    @staticmethod
    def _exponential_backoff(attempt: int) -> float:
        """Exponential backoff with jitter, capped at _MAX_RETRY_BACKOFF_SECONDS."""
        base = min(2**attempt, _MAX_RETRY_BACKOFF_SECONDS)
        jitter = random.uniform(0, base * 0.25)
        return min(base + jitter, _MAX_RETRY_BACKOFF_SECONDS)

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "LegacyZTBClientHelper":
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any],
    ) -> None:
        pass

    # ------------------------------------------------------------------
    # Compatibility stubs
    # ------------------------------------------------------------------

    def set_session(self, session: Any) -> None:
        """Compatibility stub for RequestExecutor integration."""
        self._session = session

    # ------------------------------------------------------------------
    # API properties
    # ------------------------------------------------------------------

    @property
    def alarms(self) -> "AlarmsAPI":
        """
        The interface object for the :ref:`ZTB Alarms interface <ztb-alarms>`.

        """
        from zscaler.ztb.alarms import AlarmsAPI

        return AlarmsAPI(self.request_executor)

    @property
    def api_keys(self) -> "APIKeyAuthRouterAPI":
        """
        The interface object for the :ref:`ZTB API Key Auth interface <ztb-api_keys>`.

        """
        from zscaler.ztb.api_key import APIKeyAuthRouterAPI

        return APIKeyAuthRouterAPI(self.request_executor)

    @property
    def app_connector_config(self) -> "AppConnectorConfigAPI":
        """
        The interface object for the :ref:`ZTB App Connector Config interface <ztb-app_connector_config>`.

        """
        from zscaler.ztb.app_connector_config import AppConnectorConfigAPI

        return AppConnectorConfigAPI(self.request_executor)

    @property
    def devices(self) -> "DevicesAPI":
        """
        The interface object for the :ref:`ZTB Devices interface <ztb-devices>`.

        """
        from zscaler.ztb.devices import DevicesAPI

        return DevicesAPI(self.request_executor)

    @property
    def groups_router(self) -> "GroupsRouterAPI":
        """
        The interface object for the :ref:`ZTB Groups Router interface <ztb-groups_router>`.

        """
        from zscaler.ztb.groups_router import GroupsRouterAPI

        return GroupsRouterAPI(self.request_executor)

    @property
    def logs(self) -> "LogsAPI":
        """
        The interface object for the :ref:`ZTB Logs interface <ztb-logs>`.

        """
        from zscaler.ztb.logs import LogsAPI

        return LogsAPI(self.request_executor)

    @property
    def policy_comments(self) -> "PolicyCommentsAPI":
        """
        The interface object for the :ref:`ZTB Policy Comments interface <ztb-policy_comments>`.

        """
        from zscaler.ztb.policy_comments import PolicyCommentsAPI

        return PolicyCommentsAPI(self.request_executor)

    @property
    def ransomware_kill(self) -> "RansomwareKillAPI":
        """
        The interface object for the :ref:`ZTB Ransomware Kill interface <ztb-ransomware_kill>`.

        """
        from zscaler.ztb.ransomware_kill import RansomwareKillAPI

        return RansomwareKillAPI(self.request_executor)

    @property
    def site(self) -> "SiteAPI":
        """
        The interface object for the :ref:`ZTB Site interface <ztb-site>`.

        """
        from zscaler.ztb.site import SiteAPI

        return SiteAPI(self.request_executor)

    @property
    def site2site_vpn(self) -> "Site2SiteVPNAPI":
        """
        The interface object for the :ref:`ZTB Site2Site VPN interface <ztb-site2site_vpn>`.

        """
        from zscaler.ztb.site2site_vpn import Site2SiteVPNAPI

        return Site2SiteVPNAPI(self.request_executor)

    @property
    def template_router(self) -> "TemplateRouterAPI":
        """
        The interface object for the :ref:`ZTB Template Router interface <ztb-template_router>`.

        """
        from zscaler.ztb.template_router import TemplateRouterAPI

        return TemplateRouterAPI(self.request_executor)

    # ------------------------------------------------------------------
    # Custom headers (consistent with other legacy clients)
    # ------------------------------------------------------------------

    def set_custom_headers(self, headers: Dict[str, str]) -> None:
        self.request_executor.set_custom_headers(headers)

    def clear_custom_headers(self) -> None:
        self.request_executor.clear_custom_headers()

    def get_custom_headers(self) -> Dict[str, str]:
        return self.request_executor.get_custom_headers()

    def get_default_headers(self) -> Dict[str, str]:
        return self.request_executor.get_default_headers()
