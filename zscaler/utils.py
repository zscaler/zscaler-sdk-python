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

import argparse
import base64
import datetime
import functools
import json as jsonp
import logging
import random
import re
import time
from typing import Dict, Optional
from urllib.parse import urlencode
from datetime import datetime as dt
from functools import wraps
import pytz
from box import Box, BoxList
from dateutil import parser
from requests import Response

# from restfly import APIIterator

from zscaler.constants import RETRYABLE_STATUS_CODES, DATETIME_FORMAT, EPOCH_DAY, EPOCH_MONTH, EPOCH_YEAR

logger = logging.getLogger(__name__)

# 1) Single global reformat_params
reformat_params = [
    ("app_services", "appServices"),
    ("app_service_groups", "appServiceGroups"),
    ("devices", "devices"),
    ("device_groups", "deviceGroups"),
    ("departments", "departments"),
    ("ec_groups", "ecGroups"),
    ("auditor", "auditor"),
    ("dlp_engines", "dlpEngines"),
    ("excluded_departments", "excludedDepartments"),
    ("excluded_groups", "excludedGroups"),
    ("excluded_users", "excludedUsers"),
    ("dest_ip_groups", "destIpGroups"),
    ("dest_ipv6_groups", "destIpv6Groups"),
    ("groups", "groups"),
    ("users", "users"),
    ("labels", "labels"),
    ("notification_template", "notificationTemplate"),
    ("locations", "locations"),
    ("location_groups", "locationGroups"),
    ("nw_application_groups", "nwApplicationGroups"),
    ("nw_service_groups", "nwServiceGroups"),
    ("nw_services", "nwServices"),
    ("source_ip_groups", "source_ip_groups"),
    ("source_ip_groups", "sourceIpGroups"),
    ("src_ip_groups", "srcIpGroups"),
    ("src_ipv6_groups", "srcIpv6Groups"),
    ("proxy_gateway", "proxyGateway"),
    ("time_windows", "timeWindows"),
    ("tenancy_profile_ids", "tenancyProfileIds"),
    ("sharing_domain_profiles", "sharingDomainProfiles"),
    ("form_sharing_domain_profiles", "formSharingDomainProfiles"),
    ("url_categories", "urlCategories"),
    ("zpa_app_segments", "zpaAppSegments"),
    ("zpa_application_segments", "zpaApplicationSegments"),
    ("zpa_application_segment_groups", "zpaApplicationSegmentGroups"),
    ("workload_groups", "workloadGroups"),
    ("service_ids", "services"),
    ("bandwidth_class_ids", "bandwidthClasses"),
    ("virtual_zen_node_ids", "virtualZenNodes"),
    ("smart_isolation_user_ids", "smartIsolationUsers"),
    ("smart_isolation_group_ids", "smartIsolationGroups"),
    ("cloud_app_tenant_ids", "cloudAppTenants"),
    ("object_type_ids", "objectTypes"),
    ("bucket_ids", "buckets"),
    ("included_domain_profile_ids", "includedDomainProfiles"),
    ("excluded_domain_profile_ids", "excludedDomainProfiles"),
    ("criteria_domain_profile_ids", "criteriaDomainProfiles"),
    ("email_recipient_profile_ids", "emailRecipientProfiles"),
    ("entity_group_ids", "entityGroups"),
]


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
        "ec_vms": "ecVMs",
        "is_incomplete_dr_config": "isIncompleteDRConfig",
        "ipv6_enabled": "ipV6Enabled",
        "valid_ssl_certificate": "validSSLCertificate",
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


def convert_keys(data, direction="to_camel"):
    converter = camel_to_snake if direction == "to_snake" else snake_to_camel

    if isinstance(data, (list, BoxList)):
        return [convert_keys(inner_dict, direction=direction) for inner_dict in data]
    elif isinstance(data, (dict, Box)):
        new_dict = {}
        for k in data.keys():
            v = data[k]
            new_key = converter(k)
            new_dict[new_key] = convert_keys(v, direction=direction) if isinstance(v, (dict, list)) else v
        return new_dict
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

def transform_common_id_fields(id_groups: list, source_dict: dict, target_dict: dict):
    """
    For each (key, payload_key) in 'id_groups':
      - If 'key' in source_dict, pop it out,
      - convert that list/dict to the final "id" structure,
      - store in target_dict[payload_key].
    """
    for key, payload_key in id_groups:
        if key in source_dict:
            value = source_dict.pop(key)
            if isinstance(value, list):
                # 1) Convert list-of-str-or-int => [{ "id":... }, ...]
                final_list = []
                for item in value:
                    if isinstance(item, (str, int)):
                        final_list.append({"id": int(item)})
                    elif isinstance(item, dict) and "id" in item:
                        # Possibly user gave { "id": 123, ... }
                        item["id"] = int(item["id"])
                        final_list.append(item)
                    else:
                        final_list.append(item)
                target_dict[payload_key] = final_list
            elif isinstance(value, dict) and "id" in value:
                # single dict with ID
                value["id"] = int(value["id"])
                target_dict[payload_key] = value
    return


def transform_clientless_apps(clientless_app_ids):
    transformed_apps = []
    for app in clientless_app_ids:
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

def calculate_epoch(hours: int):
    current_time = int(time.time())
    past_time = int(current_time - (hours * 3600))
    return current_time, past_time


import functools


def zdx_params(func):
    """
    Decorator to add custom parameter functionality for ZDX API calls.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.

    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Get the existing query_params dict (or create one)
        query_params = kwargs.get("query_params", {})

        # First, process shorthand parameters passed directly as keyword args.
        for key, target in [
            ("since", ("from", "to")),
            ("search", "q"),
            ("location_id", "loc"),
            ("department_id", "dept"),
            ("geo_id", "geo"),
            ("exclude_dept", "exclude_dept"),  # New: array[integer]
            ("exclude_loc", "exclude_loc"),  # New: array[integer]
            ("exclude_geo", "exclude_geo"),  # New: array[str]
            ("score_bucket", "score_bucket"),  # New: str (poor, okay, good)
            ("limit", "limit"),  # New: int
            ("offset", "offset"),  # New: str (API-defined pagination)
        ]:
            if key in kwargs:
                value = kwargs.pop(key)
                if key == "since":
                    current_time, past_time = calculate_epoch(value)
                    if "from" not in query_params:
                        query_params["from"] = past_time
                    if "to" not in query_params:
                        query_params["to"] = current_time
                else:
                    if target not in query_params:
                        query_params[target] = value

        # Then, process shorthand parameters if provided within query_params itself.
        if "since" in query_params:
            value = query_params.pop("since")
            current_time, past_time = calculate_epoch(value)
            if "to" not in query_params:
                query_params["to"] = current_time
            if "from" not in query_params:
                query_params["from"] = past_time

        if "search" in query_params and "q" not in query_params:
            query_params["q"] = query_params.pop("search")
        if "location_id" in query_params and "loc" not in query_params:
            query_params["loc"] = query_params.pop("location_id")
        if "department_id" in query_params and "dept" not in query_params:
            query_params["dept"] = query_params.pop("department_id")
        if "geo_id" in query_params and "geo" not in query_params:
            query_params["geo"] = query_params.pop("geo_id")

        # Handle new parameters: Exclusions and score_bucket
        if "exclude_dept" in query_params and isinstance(query_params["exclude_dept"], list):
            query_params["exclude_dept"] = [int(i) for i in query_params["exclude_dept"]]

        if "exclude_loc" in query_params and isinstance(query_params["exclude_loc"], list):
            query_params["exclude_loc"] = [int(i) for i in query_params["exclude_loc"]]

        if "exclude_geo" in query_params and isinstance(query_params["exclude_geo"], list):
            query_params["exclude_geo"] = [str(i) for i in query_params["exclude_geo"]]

        if "score_bucket" in query_params and query_params["score_bucket"] not in ["poor", "okay", "good"]:
            raise ValueError("Invalid value for score_bucket. Supported values: 'poor', 'okay', 'good'.")

        if "limit" in query_params:
            try:
                query_params["limit"] = int(query_params["limit"])
            except ValueError:
                raise ValueError("limit must be an integer.")

        if "offset" in query_params:
            query_params["offset"] = str(query_params["offset"])

        # Update kwargs with the modified query_params dictionary
        kwargs["query_params"] = query_params

        return func(self, *args, **kwargs)

    return wrapper


class CommonFilters:
    def __init__(self, **kwargs):
        valid_params = {
            "from_time": None,
            "to": None,
            "score_bucket": None,
            "app_id": None,
            "loc": None,
            "exclude_loc": None,
            "dept": None,
            "exclude_dept": None,
            "geo": None,
            "exclude_geo": None,
            "offset": None,
            "limit": None,
        }

        for key, value in kwargs.items():
            if key in valid_params:
                setattr(self, key, value)

    def to_dict(self):
        return {
            k: v
            for k, v in {
                "from": getattr(self, "from_time", None),
                "to": getattr(self, "to", None),
                "score_bucket": getattr(self, "score_bucket", None),
                "app_id": getattr(self, "app_id", None),
                "loc": getattr(self, "loc", None),
                "exclude_loc": getattr(self, "exclude_loc", None),
                "dept": getattr(self, "dept", None),
                "exclude_dept": getattr(self, "exclude_dept", None),
                "geo": getattr(self, "geo", None),
                "exclude_geo": getattr(self, "exclude_geo", None),
                "offset": getattr(self, "offset", None),
                "limit": getattr(self, "limit", None),
            }.items()
            if v is not None
        }


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
        raise ValueError(f"Invalid time zone. Please visit the following site for reference: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones:{time_zone_str}")

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


def convert_dc_exclusion_times(start_time_str, end_time_str, time_zone_str):
    """
    Converts and validates DC exclusion times based on API rules:
    - start_time must be >= 5 min in the future and within 30 days
    - end_time must be >= 2 hours after start_time and within 15 days
    """
    start_epoch, end_epoch = validate_and_convert_times(start_time_str, end_time_str, time_zone_str)

    now = int(datetime.datetime.now(pytz.timezone(time_zone_str)).timestamp())

    if start_epoch < now + 300:
        raise ValueError("Start time must be at least 5 minutes in the future.")
    if start_epoch > now + (30 * 86400):
        raise ValueError("Start time must be within 30 days from now.")

    if end_epoch < start_epoch + 7200:
        raise ValueError("End time must be at least 2 hours after start time.")
    if end_epoch > start_epoch + (15 * 86400):
        raise ValueError("End time must be within 15 days from start time.")

    return start_epoch, end_epoch


def convert_date_time_to_seconds(date_time):
    """
    Takes in a date time string and returns the number of seconds
    since the epoch (Unix timestamp).

    Args:
        date_time (str): Date time string in the datetime format

    Returns:
        float: Number of seconds since the epoch
    """
    dt_obj = dt.strptime(date_time, DATETIME_FORMAT)
    return float((dt_obj - dt(EPOCH_YEAR, EPOCH_MONTH, EPOCH_DAY)).total_seconds())


def format_url(base_string):
    """
    Turns multiline strings in generated clients into
    simple one-line string

    Args:
        base_string (str): multiline URL

    Returns:
        str: single line URL
    """
    return "".join([line.strip() for line in base_string.splitlines()])

# def zcc_param_mapper(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         query_params = kwargs.get("query_params", {}) or {}
#         body = kwargs.copy()
#         mapped_params = {}

#         # -------------------------------
#         # Detect source of raw inputs
#         # -------------------------------
#         raw_os = (
#             query_params.get("os_type") or
#             query_params.get("os_types") or
#             body.get("os_type") or
#             body.get("os_types")
#         )

#         if raw_os:
#             raw_os = [raw_os] if isinstance(raw_os, str) else raw_os
#             mapped = [
#                 str(zcc_param_map["os"].get(os.lower()))
#                 for os in raw_os
#                 if zcc_param_map["os"].get(os.lower())
#             ]
#             if not mapped:
#                 raise ValueError("Invalid `os_type` or `os_types` provided.")
#             mapped_params["osTypes"] = ",".join(mapped)

#         raw_reg = (
#             query_params.get("registration_type") or
#             query_params.get("registration_types") or
#             body.get("registration_type") or
#             body.get("registration_types")
#         )

#         if raw_reg:
#             raw_reg = [raw_reg] if isinstance(raw_reg, str) else raw_reg
#             mapped = [
#                 str(zcc_param_map["reg_type"].get(rt.lower()))
#                 for rt in raw_reg
#                 if zcc_param_map["reg_type"].get(rt.lower())
#             ]
#             if not mapped:
#                 raise ValueError("Invalid `registration_type(s)` provided.")
#             mapped_params["registrationTypes"] = ",".join(mapped)

#         # Clean aliases
#         for key in [
#             "os_type", "os_types",
#             "registration_type", "registration_types",
#         ]:
#             query_params.pop(key, None)
#             kwargs.pop(key, None)

#         # Distribute to the appropriate location
#         if "query_params" in kwargs:
#             query_params.update(mapped_params)
#             kwargs["query_params"] = query_params
#         else:
#             kwargs.update(mapped_params)

#         return func(self, *args, **kwargs)

#     return wrapper

def zcc_param_mapper(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        query_params = kwargs.get("query_params", {}) or {}
        body = kwargs.copy()
        mapped_params = {}

        # -------------------------------
        # Detect source of raw inputs
        # -------------------------------
        raw_os = (
            query_params.get("os_type") or
            query_params.get("os_types") or
            body.get("os_type") or
            body.get("os_types")
        )

        if raw_os:
            raw_os = [raw_os] if isinstance(raw_os, str) else raw_os
            mapped = [
                str(zcc_param_map["os"].get(os.lower()))
                for os in raw_os
                if zcc_param_map["os"].get(os.lower())
            ]
            if not mapped:
                raise ValueError("Invalid `os_type` or `os_types` provided.")
            # Use singular key if original was singular, plural if original was plural
            if "os_type" in query_params or "os_type" in body:
                mapped_params["osType"] = ",".join(mapped)
            else:
                mapped_params["osTypes"] = ",".join(mapped)

        raw_reg = (
            query_params.get("registration_type") or
            query_params.get("registration_types") or
            body.get("registration_type") or
            body.get("registration_types")
        )

        if raw_reg:
            raw_reg = [raw_reg] if isinstance(raw_reg, str) else raw_reg
            mapped = [
                str(zcc_param_map["reg_type"].get(rt.lower()))
                for rt in raw_reg
                if zcc_param_map["reg_type"].get(rt.lower())
            ]
            if not mapped:
                raise ValueError("Invalid `registration_type(s)` provided.")
            # Use singular key if original was singular, plural if original was plural
            if "registration_type" in query_params or "registration_type" in body:
                mapped_params["registrationType"] = ",".join(mapped)
            else:
                mapped_params["registrationTypes"] = ",".join(mapped)

        # Clean aliases
        for key in [
            "os_type", "os_types",
            "registration_type", "registration_types",
        ]:
            query_params.pop(key, None)
            kwargs.pop(key, None)

        # Distribute to the appropriate location
        if "query_params" in kwargs:
            query_params.update(mapped_params)
            kwargs["query_params"] = query_params
        else:
            kwargs.update(mapped_params)

        return func(self, *args, **kwargs)

    return wrapper

zcc_param_map = {
    "os": {
        "ios": 1,
        "android": 2,
        "windows": 3,
        "macos": 4,
        "linux": 5,
    },
    "reg_type": {
        "all": 0,
        "registered": 1,
        "removal_pending": 3,
        "unregistered": 4,
        "removed": 5,
        "quarantined": 6,
    },
}

class RateLimitExceededError(Exception):
    def __init__(self, retry_at: datetime):
        super().__init__(
            f"/downloadDevices daily limit reached. Try again at {retry_at.isoformat()}."
        )
        self.retry_at = retry_at


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

