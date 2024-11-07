# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import datetime
import logging
import os
import re
import time
import uuid
from time import sleep

import requests
from box import Box, BoxList

from zscaler import __version__
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.errors.http_error import HTTPError, ZscalerAPIError
from zscaler.exceptions.exceptions import HTTPException, ZscalerAPIException
from zscaler.logger import setup_logging
from zscaler.ratelimiter.ratelimiter import RateLimiter
from zscaler.user_agent import UserAgent
from zscaler.utils import (
    convert_keys_to_snake,
    dump_request,
    dump_response,
    format_json_response,
    obfuscate_api_key,
    retry_with_backoff,
)

from zscaler.zcon.client import ZCONClient
from zscaler.zcon.activation import ActivationAPI
from zscaler.zcon.admin_and_role_management import AdminAndRoleManagementAPI
from zscaler.zcon.provisioning import ProvisioningAPI
from zscaler.zcon.ecgroups import EcGroupAPI
from zscaler.zcon.locations import LocationAPI

# Setup the logger
setup_logging(logger_name="zscaler-sdk-python")
logger = logging.getLogger("zscaler-sdk-python")


class ZCONClientHelper(ZCONClient):
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

    def __init__(self, cloud=None, timeout=240, cache=None, fail_safe=False, **kw):
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
        self.url = f"https://connector.{self.env_cloud}.net/api/v1"
        self.conv_box = True
        self.sandbox_token = kw.get("sandbox_token") or os.getenv(f"{self._env_base}_SANDBOX_TOKEN")
        self.timeout = timeout
        self.fail_safe = fail_safe
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
        # Initialize user-agent
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

    @retry_with_backoff(retries=5)
    def authenticate(self) -> Box:
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
            self.url + "/auth",
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

    def send(self, method, path, json=None, params=None, data=None, headers=None):
        """
        Send a request to the ZCON API.

        Parameters:
        - method (str): The HTTP method.
        - path (str): API endpoint path.
        - json (dict, optional): Request payload. Defaults to None.
        Returns:
        - Response: Response object from the request.
        """
        api = self.url
        url = f"{api}/{path.lstrip('/')}"
        start_time = time.time()
        # Update headers to include the user agent
        headers_with_user_agent = self.headers.copy()
        headers_with_user_agent["User-Agent"] = self.user_agent
        # Generate a unique UUID for this request
        request_uuid = uuid.uuid4()
        if headers is not None:
            headers_with_user_agent.update(headers)
        dump_request(
            logger,
            url,
            method,
            json,
            params,
            headers_with_user_agent,
            request_uuid,
            body=True,
        )
        # Check cache before sending request
        cache_key = self.cache.create_key(url, params)
        if method == "GET" and self.cache.contains(cache_key):
            resp = self.cache.get(cache_key)
            dump_response(
                logger=logger,
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
        while attempts < 5:  # Trying a maximum of 5 times
            try:
                # If the token is None or expired, fetch a new token
                if self.is_session_expired():
                    logger.warning("The provided sesion expired. Refreshing...")
                    self.authenticate()
                resp = requests.request(
                    method=method,
                    url=url,
                    json=json,
                    data=data,
                    params=params,
                    headers=headers_with_user_agent,
                    timeout=self.timeout,
                    cookies={"JSESSIONID": self.session_id},
                )
                dump_response(
                    logger=logger,
                    url=url,
                    params=params,
                    method=method,
                    resp=resp,
                    request_uuid=request_uuid,
                    start_time=start_time,
                )
                if resp.status_code == 429:  # HTTP Status code 429 indicates "Too Many Requests"
                    sleep_time = int(
                        resp.headers.get("Retry-After", 2)
                    )  # Default to 60 seconds if 'Retry-After' header is missing
                    logger.warning(f"Rate limit exceeded. Retrying in {sleep_time} seconds.")
                    sleep(sleep_time)
                    attempts += 1
                    continue
                else:
                    break
            except requests.RequestException as e:
                if attempts == 4:  # If it's the last attempt, raise the exception
                    logger.error(f"Failed to send {method} request to {url} after 5 attempts. Error: {str(e)}")
                    raise e
                else:
                    logger.warning(f"Failed to send {method} request to {url}. Retrying... Error: {str(e)}")
                    attempts += 1
                    sleep(5)  # Sleep for 5 seconds before retrying

        # If Non-GET call, clear the
        if method != "GET":
            self.cache.delete(cache_key)

        # Detailed logging for request and response
        try:
            response_data = resp.json()
        except ValueError:  # Using ValueError for JSON decoding errors
            response_data = resp.text
        # check if call was succesful
        if 200 > resp.status_code or resp.status_code > 299:
            # create errors
            try:
                error = ZscalerAPIError(url, resp, response_data)
                if self.fail_safe:
                    raise ZscalerAPIException(url, resp, response_data)
            except ZscalerAPIException:
                raise
            except Exception:
                error = HTTPError(url, resp, response_data)
                if self.fail_safe:
                    logger.error(response_data)
                    raise HTTPException(url, resp, response_data)
            logger.error(error)
        # Cache the response if it's a successful GET request
        if method == "GET" and resp.status_code == 200:
            self.cache.add(cache_key, resp)
        return resp

    def get(self, path, json=None, params=None):
        """
        Send a GET request to the ZCON API.

        Parameters:
        - path (str): API endpoint path.
        - data (dict, optional): Request payload. Defaults to None.
        Returns:
        - Response: Response object from the request.
        """

        should_wait, delay = self.rate_limiter.wait("GET")
        if should_wait:
            time.sleep(delay)
        response = self.send("GET", path, json, params)
        if not response.ok:
            raise Exception(f"GET request failed with status {response.status_code}: {response.json()}")
        return format_json_response(response, box_attrs=dict())

    def post(self, path, json=None, params=None, data=None, headers=None):
        should_wait, delay = self.rate_limiter.wait("POST")
        if should_wait:
            time.sleep(delay)
        response = self.send("POST", path, json, params, data=data, headers=headers)
        if not response.ok:
            raise Exception(f"POST request failed with status {response.status_code}: {response.json()}")
        return format_json_response(response, box_attrs=dict())

    def put(self, path, json=None, params=None):
        should_wait, delay = self.rate_limiter.wait("PUT")
        if should_wait:
            time.sleep(delay)
        response = self.send("PUT", path, json, params)

        # Handle 204 No Content separately
        if response.status_code == 204:
            return response

        # Handle 200 OK with content
        if response.status_code == 200 and response.headers.get("content-type", "").startswith("application/json"):
            return format_json_response(response, box_attrs=dict())

        # Raise an exception for any other unexpected status codes
        if not response.ok:
            raise Exception(f"PUT request failed with status {response.status_code}: {response.json()}")

        return response

    def delete(self, path, json=None, params=None):
        should_wait, delay = self.rate_limiter.wait("DELETE")
        if should_wait:
            time.sleep(delay)
        response = self.send("DELETE", path, json, params)
        if not response.ok:
            raise Exception(f"DELETE request failed with status {response.status_code}: {response.json()}")
        # Since DELETE typically returns 204 No Content, we don't need to format the response.
        return response

    ERROR_MESSAGES = {
        "UNEXPECTED_STATUS": "Unexpected status code {status_code} received for page {page}.",
        "MISSING_DATA_KEY": "The key '{data_key_name}' was not found in the response for page {page}.",
        "EMPTY_RESULTS": "No results found for page {page}.",
    }

    def get_paginated_data(self, path=None, data_key_name=None, data_per_page=5, expected_status_code=200):
        """
        Fetch paginated data from the ZCON API.
        ...

        Returns:
        - list: List of fetched items.
        - str: Error message, if any occurred.
        """

        page = 1
        ret_data = []
        error_message = None

        while True:
            required_url = f"{path}"
            should_wait, delay = self.rate_limiter.wait("GET")
            if should_wait:
                time.sleep(delay)

            # Now proceed with sending the request
            response = self.send(
                method="GET",
                path=required_url,
                params={"page": page, "pageSize": data_per_page},
            )

            if response.status_code != expected_status_code:
                error_message = self.ERROR_MESSAGES["UNEXPECTED_STATUS"].format(status_code=response.status_code, page=page)
                logger.error(error_message)
                break
            data_json = response.json()
            if isinstance(data_json, list):
                data = data_json
            else:
                data = data_json.get(data_key_name)

            if data is None:
                error_message = self.ERROR_MESSAGES["MISSING_DATA_KEY"].format(data_key_name=data_key_name, page=page)
                logger.error(error_message)
                break

            if not data:  # Checks for empty data
                logger.info(self.ERROR_MESSAGES["EMPTY_RESULTS"].format(page=page))
                break

            ret_data.extend(convert_keys_to_snake(data))

            # Check for more pages
            if len(data) == 0 or isinstance(data_json, dict) and int(response.json().get("totalPages")) <= page + 1:
                break

            page += 1

        return BoxList(ret_data), error_message

    @property
    def activation(self):
        """
        The interface object for the :ref:`ZCON Activation Service <zcon-activation>`.

        """
        return ActivationAPI(self)

    @property
    def admin_and_role_management(self):
        """
        The interface object for the :ref:`ZCON Admin and Role Management interface <zcon-admin_and_role_management>`.

        """
        return AdminAndRoleManagementAPI(self)

    @property
    def ecgroups(self):
        """
        The interface object for the :ref:`ZCON EC Group Service <zcon-ecgroups>`.

        """
        return EcGroupAPI(self)

    @property
    def locations(self):
        """
        The interface object for the :ref:`ZCON Location Service <zcon-locations>`.

        """
        return LocationAPI(self)

    @property
    def provisioning(self):
        """
        The interface object for the :ref:`ZCON API Key Provisioning Service <zcon-provisioning>`.

        """
        return ProvisioningAPI(self)
