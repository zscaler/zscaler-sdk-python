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

import datetime
import logging
import os
import re
from time import sleep

import requests
from zscaler import __version__
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.logger import setup_logging
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import obfuscate_api_key

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class LegacyZCONClientHelper:
    """
    A Controller to access Endpoints in the ZCON API.

    The ZCON object stores the session token and simplifies access to CRUD options within the ZCON platform.

    Attributes:
        api_key (str): The ZCON API key generated from the ZCON console.
        username (str): The ZCON administrator username.
        password (str): The ZCON administrator password.
        cloud (str): The ZCON cloud for your tenancy, accepted values are:
    """

    _vendor = "Zscaler"
    _product = "Zscaler Cloud and Branch Connector"
    _build = __version__
    _env_base = "ZCON"
    env_cloud = "zscaler"

    def __init__(self, cloud=None, timeout=240, cache=None, fail_safe=False, request_executor_impl=None, **kw):
        from zscaler.request_executor import RequestExecutor

        self.api_key = kw.get("api_key", os.getenv(f"{self._env_base}_API_KEY"))
        self.username = kw.get("username", os.getenv(f"{self._env_base}_USERNAME"))
        self.password = kw.get("password", os.getenv(f"{self._env_base}_PASSWORD"))
        # The 'cloud' parameter should have precedence over environment variables
        self.env_cloud = cloud or kw.get("cloud") or os.getenv(f"{self._env_base}_CLOUD")
        if not self.env_cloud:
            raise ValueError(
                f"Cloud environment must be set via the 'cloud' argument or the {self._env_base}_CLOUD environment variable."
            )

        # URL construction
        self.url = f"https://connector.{self.env_cloud}.net"
        self.conv_box = True
        self.timeout = timeout
        self.fail_safe = fail_safe

        ua = UserAgent()
        self.user_agent = ua.get_user_agent_string()
        # Initialize rate limiter
        # You may want to adjust these parameters as per your rate limit configuration
        self.rate_limiter = RateLimiter(
            get_limit=2,  # Adjust as per actual limit
            post_put_delete_limit=2,  # Adjust as per actual limit
            get_freq=2,  # Adjust as per actual frequency (in seconds)
            post_put_delete_freq=2,  # Adjust as per actual frequency (in seconds)
        )
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        self.session_timeout_offset = datetime.timedelta(minutes=5)
        self.session_refreshed = None
        self.auth_details = None
        self.session_id = None
        self.authenticate()

        self.cache = NoOpCache()

        self.config = {
            "client": {
                "cloud": self.env_cloud,
                "requestTimeout": self.timeout,
                "rateLimit": {"maxRetries": 3},
                "cache": {
                    "enabled": False,
                },
            }
        }
        self.request_executor = (request_executor_impl or RequestExecutor)(self.config, self.cache, zcon_legacy_client=self)

    def extractJSessionIDFromHeaders(self, header):
        session_id_str = header.get("Set-Cookie", "")

        if not session_id_str:
            raise ValueError("no Set-Cookie header received")

        regex = re.compile(r"JSESSIONID=(.*?);")
        result = regex.search(session_id_str)

        if not result:
            raise ValueError("couldn't find JSESSIONID in header value")

        return result.group(1)

    def is_session_expired(self):
        if self.auth_details is None:
            return True
        now = datetime.datetime.now()
        if self.auth_details["passwordExpiryTime"] > 0 and (
            self.session_refreshed + datetime.timedelta(seconds=-self.session_timeout_offset) < now
        ):
            return True
        return False

    def authenticate(self):
        """
        Creates a ZCON authentication session.
        """
        api_key_chars = list(self.api_key)
        api_obf = obfuscate_api_key(api_key_chars)

        payload = {
            "apiKey": api_obf["key"],
            "username": self.username,
            "password": self.password,
            "timestamp": api_obf["timestamp"],
        }
        resp = requests.request(
            "POST",
            self.url + "/api/v1/auth",
            json=payload,
            headers=self.headers,
            timeout=self.timeout,
        )
        if resp.status_code > 299:
            return resp
        self.session_refreshed = datetime.datetime.now()
        self.session_id = self.extractJSessionIDFromHeaders(resp.headers)
        self.auth_details = resp.json()
        return resp

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("deauthenticating...")
        self.deauthenticate()

    def deauthenticate(self):
        """
        Ends the ZCON authentication session.
        """
        logout_url = self.url + "/auth"

        headers = self.headers.copy()
        headers.update({"Cookie": f"JSESSIONID={self.session_id}"})

        try:
            response = requests.delete(logout_url, headers=headers, timeout=self.timeout)
            if response.status_code == 204:
                self.session_id = None
                self.auth_details = None
                return True
            else:
                return False
        except requests.RequestException as e:
            return False

    def __enter__(self):
        if self.is_session_expired():
            resp = self.authenticate()
            if resp.status_code > 299:
                raise Exception(f"Error auth:{resp.json()}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("deauthenticating...")
        self.deauthenticate()

    def get_base_url(self, endpoint):
        return self.url

    def send(self, method, path, json=None, params=None, data=None, headers=None):
        """
        Send a request to the ZIA API using JSESSIONID-based authentication.

        Args:
            method (str): The HTTP method.
            path (str): API endpoint path.
            json (dict, optional): Request payload. Defaults to None.
            params (dict, optional): URL query parameters. Defaults to None.
            data (dict, optional): Raw request data. Defaults to None.
            headers (dict, optional): Additional request headers. Defaults to None.

        Returns:
            requests.Response: Response object from the request.
        """
        url = f"{self.url}/{path.lstrip('/')}"

        # Prepare headers
        headers_with_user_agent = self.headers.copy()
        headers_with_user_agent.update(headers or {})
        headers_with_user_agent.update(self.request_executor.get_custom_headers())
        headers_with_user_agent["Cookie"] = f"JSESSIONID={self.session_id}"
        attempts = 0
        while attempts < 5:
            try:
                # Refresh session if expired
                if self.is_session_expired():
                    logger.warning("Session expired. Refreshing...")
                    self.authenticate()

                # Execute the request
                resp = requests.request(
                    method=method,
                    url=url,
                    json=json,
                    data=data,
                    params=params,
                    headers=headers_with_user_agent,
                    timeout=self.timeout,
                )

                if resp.status_code == 429:  # Handle rate-limiting
                    sleep_time = int(resp.headers.get("Retry-After", 2))
                    logger.warning(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
                    sleep(sleep_time)
                    attempts += 1
                    continue

                if resp.status_code in [401, 403]:  # Authentication failure
                    logger.error("Authentication failed, refreshing session.")
                    self.authenticate()
                    continue

                if resp.status_code >= 400:
                    logger.error(f"Request failed: {resp.status_code}, {resp.text}")
                    raise ValueError(f"Request failed with status {resp.status_code}")

                return resp, {
                    "method": method,
                    "url": url,
                    "params": params or {},
                    "headers": headers_with_user_agent,
                    "json": json or {},
                }
            except requests.RequestException as e:
                logger.error(f"Request to {url} failed: {e}")
                if attempts == 4:
                    raise
                logger.warning(f"Retrying... ({attempts + 1}/5)")
                attempts += 1
                sleep(5)

        raise ValueError("Request execution failed after maximum retries.")

    def set_session(self, session):
        """Dummy method for compatibility with the request executor."""
        self._session = session

    @property
    def account_details(self):
        """
        The interface object for the :ref:`ZCON Account Details interface <zcon-account_details>`.

        """
        from zscaler.zcon.account_details import AccountDetailsAPI

        return AccountDetailsAPI(self.request_executor)

    @property
    def activate(self):
        """
        The interface object for the :ref:`ZCON Activation interface <zcon-activate>`.

        """
        from zscaler.zcon.activation import ActivationAPI

        return ActivationAPI(self.request_executor)

    @property
    def admin_roles(self):
        """
        The interface object for the :ref:`ZCON Admin and Role Management interface <zcon-admin_roles>`.

        """
        from zscaler.zcon.admin_roles import AdminRolesAPI

        return AdminRolesAPI(self.request_executor)

    @property
    def admin_users(self):
        """
        The interface object for the :ref:`ZCON Admin Users interface <zcon-admin_users>`.

        """
        from zscaler.zcon.admin_users import AdminUsersAPI

        return AdminUsersAPI(self.request_executor)

    @property
    def ec_groups(self):
        """
        The interface object for the :ref:`ZCON EC Groups interface <zcon-ec_groups>`.

        """
        from zscaler.zcon.ec_groups import ECGroupsAPI

        return ECGroupsAPI(self.request_executor)

    @property
    def location_management(self):
        """
        The interface object for the :ref:`ZCON Locations interface <zcon-location_management>`.

        """
        from zscaler.zcon.location_management import LocationManagementAPI

        return LocationManagementAPI(self.request_executor)

    @property
    def location_template(self):
        """
        The interface object for the :ref:`ZCON Locations interface <zcon-location_template>`.

        """
        from zscaler.zcon.location_template import LocationTemplateAPI

        return LocationTemplateAPI(self.request_executor)

    @property
    def api_keys(self):
        """
        The interface object for the :ref:`ZCON Provisioning API Key interface <zcon-api_keys>`.

        """
        from zscaler.zcon.api_keys import ProvisioningAPIKeyAPI

        return ProvisioningAPIKeyAPI(self.request_executor)

    @property
    def provisioning_url(self):
        """
        The interface object for the :ref:`ZCON Provisioning URL interface <zcon-provisioning_url>`.

        """

        from zscaler.zcon.provisioning_url import ProvisioningURLAPI

        return ProvisioningURLAPI(self.request_executor)

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
