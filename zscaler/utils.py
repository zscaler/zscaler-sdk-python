# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import argparse
import base64
import datetime
import json
import json as jsonp
import logging
import random
import re
import time
from typing import Dict, Optional
from urllib.parse import urlencode

import pytz
from box import Box, BoxList
from dateutil import parser
from requests import Response
from restfly import APIIterator

from zscaler.constants import RETRYABLE_STATUS_CODES

logger = logging.getLogger("zscaler-sdk-python")


# Recursive function to convert all keys and nested keys from camel case
# to snake case.
def convert_keys_to_snake(data):
    if isinstance(data, (list, BoxList)):
        return [convert_keys_to_snake(inner_dict) for inner_dict in data]
    elif isinstance(data, (dict, Box)):
        new_dict = {}
        for k in data.keys():
            v = data[k]
            new_key = camel_to_snake(k)
            new_dict[new_key] = convert_keys_to_snake(v) if isinstance(v, (dict, list)) else v
        return new_dict
    else:
        return data


def camel_to_snake(name: str):
    """Converts Python camelCase to Zscaler's lower snake_case."""
    # Edge-cases where camelCase is breaking
    edge_cases = {
        "routableIP": "routable_ip",
        "isNameL10nTag": "is_name_l10n_tag",
        "nameL10nTag": "name_l10n_tag",
        "surrogateIP": "surrogate_ip",
        "surrogateIPEnforcedForKnownBrowsers": "surrogate_ip_enforced_for_known_browsers",
        "startIPAddress": "start_ip_address",
        "endIPAddress": "end_ip_address",
        "isIncompleteDRConfig": "is_incomplete_dr_config",
    }
    return edge_cases.get(name, re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower())


def snake_to_camel(name: str):
    """Converts Python Snake Case to Zscaler's lower camelCase."""
    if "_" not in name:
        return name
    # Edge-cases where camelCase is breaking
    edge_cases = {
        "routable_ip": "routableIP",
        "is_name_l10n_tag": "isNameL10nTag",
        "name_l10n_tag": "nameL10nTag",
        "surrogate_ip": "surrogateIP",
        "surrogate_ip_enforced_for_known_browsers": "surrogateIPEnforcedForKnownBrowsers",
        "is_incomplete_dr_config": "isIncompleteDRConfig",
        "email_ids": "emailIds",
        "page_size": "pageSize",
    }
    return edge_cases.get(name, name[0].lower() + name.title()[1:].replace("_", ""))


def recursive_snake_to_camel(data):
    """Recursively convert dictionary keys from snake_case to camelCase."""
    if isinstance(data, dict):
        return {snake_to_camel(key): recursive_snake_to_camel(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [recursive_snake_to_camel(item) for item in data]
    else:
        return data


def chunker(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


# Recursive function to convert all keys and nested keys from snake case
# to camel case.


def convert_keys(data):
    if isinstance(data, (list, BoxList)):
        return [convert_keys(inner_dict) for inner_dict in data]
    elif isinstance(data, (dict, Box)):
        new_dict = {}
        for k in data.keys():
            v = data[k]
            new_key = snake_to_camel(k)
            new_dict[new_key] = convert_keys(v) if isinstance(v, (dict, list)) else v
        return new_dict
    else:
        return data


def keys_exists(element: dict, *keys):
    """
    Check if *keys (nested) exists in `element` (dict).
    """
    if not isinstance(element, dict):
        raise AttributeError("keys_exists() expects dict as first argument.")
    if not keys:
        raise AttributeError("keys_exists() expects at least two arguments, one given.")

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True


# Takes a tuple if id_groups, kwargs and the payload dict; reformat for API call
def add_id_groups(id_groups: list, kwargs: dict, payload: dict):
    for entry in id_groups:
        if kwargs.get(entry[0]):
            payload[entry[1]] = [{"id": param_id} for param_id in kwargs.pop(entry[0])]
    return


def transform_common_id_fields(id_groups: list, kwargs: dict, payload: dict):
    for entry in id_groups:
        if kwargs.get(entry[0]):
            # Ensure each ID is treated as an integer before adding it to the payload
            payload[entry[1]] = [{"id": int(param_id)} for param_id in kwargs.pop(entry[0])]
    return


def transform_clientless_apps(clientless_app_ids):
    transformed_apps = []
    for app in clientless_app_ids:
        # Transform each attribute in app as needed by your API
        transformed_apps.append(
            {
                "name": app["name"],
                "applicationProtocol": app["application_protocol"],
                "applicationPort": app["application_port"],
                "certificateId": app["certificate_id"],
                "trustUntrustedCert": app["trust_untrusted_cert"],
                "enabled": app["enabled"],
                "domain": app["domain"],
            }
        )
    return transformed_apps


def format_clientless_apps(clientless_apps):
    # Implement this function to format clientless_apps as needed for the update request
    # This is just a placeholder example
    formatted_apps = []
    for app in clientless_apps:
        formatted_app = {
            "id": app["id"],  # use the correct key
            # Add other necessary attributes and format them as needed
        }
        formatted_apps.append(formatted_app)
    return formatted_apps


def obfuscate_api_key(seed: list):
    now = int(time.time() * 1000)
    n = str(now)[-6:]
    r = str(int(n) >> 1).zfill(6)
    key = "".join(seed[int(str(n)[i])] for i in range(len(str(n))))
    for j in range(len(r)):
        key += seed[int(r[j]) + 2]

    return {"timestamp": now, "key": key}


def format_json_response(
    response: Response,
    box_attrs: Optional[Dict] = None,
    conv_json: bool = True,
    conv_box: bool = True,
):
    """
    A simple utility to handle formatting the response object into either a
    Box object or a Python native object from the JSON response.  The function
    will prefer box over python native if both flags are set to true.  If none
    of the flags are true, or if the content-type header reports as something
    other than "applicagion/json", then the response object is instead
    returned.

    Args:
        response:
            The response object that will be checked against.
        box_attrs:
            The optional box attributed to pass as part of instantiation.
        conv_json:
            A flag handling if we should run the JSON conversion to python
            native datatypes.
        conv_box:
            A flaghandling if we should convert the data to a Box object.

    Returns:
        box.Box:
            If the conv_box flag is True, and the response is a single object,
            then the response is a Box obj.
        box.BoxList:
            If the conv_box flag is True, and the response is a list of
            objects, then the response is a BoxList obj.
        dict:
            If the conv_json flag is True and the  conv_box is False, and the
            response is a single object, then the response is a dict obj.
        list:
            If the conv_json flag is True and conv_box is False, and the
            response is a list of objects, then the response is a list obj.
        requests.Response:
            If neither flag is True, or if the response isn't JSON data, then
            a response object is returned (pass-through).
    """
    if response.status_code > 299:
        return response
    content_type = response.headers.get("content-type", "application/json")
    if (conv_json or conv_box) and "application/json" in content_type.lower() and len(response.text) > 0:  # noqa: E124
        if conv_box:
            data = convert_keys_to_snake(response.json())
            if isinstance(data, list):
                return BoxList(data, **box_attrs)
            elif isinstance(data, dict):
                return Box(data, **box_attrs)
        elif conv_json:
            return convert_keys_to_snake(response.json())
    return response


def pick_version_profile(kwargs: list, payload: list):
    # Used in ZPA endpoints.
    # This function is used to convert the name of the version profile to
    # the version profile id. This means our users don't need to look up the
    # version profile id mapping themselves.

    version_profile = kwargs.pop("version_profile", None)
    if version_profile:
        payload["overrideVersionProfile"] = True
        if version_profile == "default":
            payload["versionProfileId"] = 0
        elif version_profile == "previous_default":
            payload["versionProfileId"] = 1
        elif version_profile == "new_release":
            payload["versionProfileId"] = 2


class Iterator(APIIterator):
    """Iterator class."""

    page_size = 100

    def __init__(self, api, path: str = "", **kw):
        """Initialize Iterator class."""
        super().__init__(api, **kw)

        self.path = path
        self.max_items = kw.pop("max_items", 0)
        self.max_pages = kw.pop("max_pages", 0)
        self.payload = {}
        if kw:
            self.payload = {snake_to_camel(key): value for key, value in kw.items()}

    def _get_page(self) -> None:
        """Iterator function to get the page."""
        resp = self._api.get(
            self.path,
            params={**self.payload, "page": self.num_pages + 1},
        )
        try:
            # If we are using ZPA then the API will return records under the
            # 'list' key.
            self.page = resp.get("list") or []
        except AttributeError:
            # If the list key doesn't exist then we're likely using ZIA so just
            # return the full response.
            self.page = resp
        finally:
            # If we use the default retry-after logic in Restfly then we are
            # going to keep seeing 429 messages in stdout. ZIA and ZPA have a
            # standard 1 sec rate limit on the API endpoints with pagination so
            # we are going to include it here.
            time.sleep(1)


def remove_cloud_suffix(str_name: str) -> str:
    """
    Removes appended cloud name (e.g. "(zscalerthree.net)") from the string.

    Args:
        str_name (str): The string from which to remove the cloud name.

    Returns:
        str: The string without the cloud name.
    """
    reg = re.compile(r"(.*)\s+\([a-zA-Z0-9\-_\.]*\)\s*$")
    res = reg.sub(r"\1", str_name)
    return res.strip()


def should_retry(status_code):
    """Determine if a given status code should be retried."""
    return status_code in RETRYABLE_STATUS_CODES


def retry_with_backoff(method_type="GET", retries=5, backoff_in_seconds=0.5):
    """
    Decorator to retry a function in case of an unsuccessful response.

    Parameters:
    - method_type (str): The HTTP method. Defaults to "GET".
    - retries (int): Number of retries before giving up. Defaults to 5.
    - backoff_in_seconds (float): Initial wait time (in seconds) before retry. Defaults to 0.5.

    Returns:
    - function: Decorated function with retry and backoff logic.
    """

    if method_type != "GET":
        retries = min(retries, 3)  # more conservative retry count for non-GET

    def decorator(f):
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                resp = f(*args, **kwargs)

                # Check if it's a successful status code, 400, or if it shouldn't be retried
                if 299 >= resp.status_code >= 200 or resp.status_code == 400 or not should_retry(resp.status_code):
                    return resp

                if x == retries:
                    try:
                        error_msg = resp.json()
                    except Exception as e:
                        error_msg = str(e)
                    raise Exception(f"Reached max retries. Response: {error_msg}")
                else:
                    sleep = backoff_in_seconds * 2**x + random.uniform(0, 1)
                    logger.info("Args: %s, retrying after %d seconds...", str(args), sleep)
                    time.sleep(sleep)
                    x += 1

        return wrapper

    return decorator


def is_token_expired(token_string):
    # If token string is None or empty, consider it expired
    if not token_string:
        logger.warning("Token string is None or empty. Requesting a new token.")
        return True

    try:
        # Split the token into its parts
        parts = token_string.split(".")
        if len(parts) != 3:
            return True

        # Decode the payload
        payload_bytes = base64.urlsafe_b64decode(parts[1] + "==")  # Padding might be needed
        payload = jsonp.loads(payload_bytes)

        # Check expiration time
        if "exp" in payload:
            # Deduct 10 seconds to account for any possible latency or clock skew
            expiration_time = payload["exp"] - 10
            if time.time() > expiration_time:
                return True

        return False

    except Exception as e:
        logger.error(f"Error checking token expiration: {str(e)}")
        return True


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def is_valid_ssh_key(private_key: str) -> bool:
    """
    Validate SSH private key format.
    """
    # Basic pattern matching to check for RSA/ECDSA (OpenSSH/PEM) key headers
    ssh_key_patterns = [
        r"-----BEGIN OPENSSH PRIVATE KEY-----",
        r"-----BEGIN RSA PRIVATE KEY-----",
        r"-----BEGIN EC PRIVATE KEY-----",
    ]
    return any(re.search(pattern, private_key) for pattern in ssh_key_patterns)


def validate_and_convert_times(start_time_str, end_time_str, time_zone_str):
    """
    Validates and converts provided time strings to epoch.
    Validates the time zone against IANA Time Zone database.
    Ensures start time is not more than 1 hour in the past and within 1 year range of end time.

    Args:
        start_time_str (str): Start time in RFC1123Z or RFC1123 format.
        end_time_str (str): End time in RFC1123Z or RFC1123 format.
        time_zone_str (str): IANA Time Zone database string.

    Returns:
        tuple: Converted start and end times in epoch format.

    Raises:
        ValueError: If any validation fails.
    """
    # Validate time zone
    if time_zone_str not in pytz.all_timezones:
        raise ValueError(f"Invalid time zone: {time_zone_str}")

    # Convert times
    try:
        start_time = parser.parse(start_time_str)
        end_time = parser.parse(end_time_str)
    except ValueError as e:
        raise ValueError(f"Time parsing error: {e}")

    # Handle timezone conversion
    tz = pytz.timezone(time_zone_str)
    if start_time.tzinfo is not None:
        start_time = start_time.astimezone(tz)
    else:
        start_time = tz.localize(start_time)

    if end_time.tzinfo is not None:
        end_time = end_time.astimezone(tz)
    else:
        end_time = tz.localize(end_time)

    # Ensure start time is not more than 1 hour in the past
    now_in_tz = datetime.datetime.now(tz)
    if start_time < (now_in_tz - datetime.timedelta(hours=1)):
        raise ValueError("Start time cannot be more than 1 hour in the past.")

    # Ensure start time is within a one year range of end time
    if end_time > (start_time + datetime.timedelta(days=365)):
        raise ValueError("Start time and end time range cannot exceed 1 year.")

    # Convert to epoch
    start_epoch = int(start_time.timestamp())
    end_epoch = int(end_time.timestamp())

    return start_epoch, end_epoch


def dump_request(logger, url: str, method: str, json, params, headers, request_uuid: str, body=True):
    request_headers_filtered = {key: value for key, value in headers.items() if key != "Authorization"}
    # Log the request details before sending the request
    request_data = {
        "url": url,
        "method": method,
        "params": jsonp.dumps(params),
        "uuid": str(request_uuid),
        "request_headers": jsonp.dumps(request_headers_filtered),
    }
    log_lines = []
    request_body = ""
    if body:
        request_body = jsonp.dumps(json)
    log_lines.append(f"\n---[ ZSCALER SDK REQUEST | ID:{request_uuid} ]-------------------------------")
    log_lines.append(f"{method} {url}")
    for key, value in headers.items():
        log_lines.append(f"{key}: {value}")
    if body and request_body != "" and request_body != "null":
        log_lines.append(f"\n{request_body}")
    log_lines.append("--------------------------------------------------------------------")
    logger.info("\n".join(log_lines))


def dump_response(
    logger,
    url: str,
    method: str,
    resp,
    params,
    request_uuid: str,
    start_time,
    from_cache: bool = None,
):
    # Calculate the duration in seconds
    end_time = time.time()
    duration_seconds = end_time - start_time
    # Convert the duration to milliseconds
    duration_ms = duration_seconds * 1000
    # Convert the headers to a regular dictionary
    response_headers_dict = dict(resp.headers)
    full_url = url
    if params:
        full_url += "?" + urlencode(params)
    log_lines = []
    response_body = ""
    if resp.text:
        response_body = resp.text

    if from_cache:
        log_lines.append(
            f"\n---[ ZSCALER SDK RESPONSE | ID:{request_uuid} | " f"FROM CACHE | DURATION:{duration_ms}ms ]" + "-" * 31
        )
    else:
        log_lines.append(f"\n---[ ZSCALER SDK RESPONSE | ID:{request_uuid} | " f"DURATION:{duration_ms}ms ]" + "-" * 46)
    log_lines.append(f"{method} {full_url}")
    for key, value in response_headers_dict.items():
        log_lines.append(f"{key}: {value}")
    if response_body and response_body != "" and response_body != "null":
        log_lines.append(f"\n{response_body}")
    log_lines.append("-" * 68)
    logger.info("\n".join(log_lines))
