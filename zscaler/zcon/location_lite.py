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

from typing import List, Optional, Any, Dict, Union
from requests import Response
from zscaler.zcon.client import ZCONClient


class LocationLite:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        parent_id: Optional[int] = None,
        tz: Optional[str] = None,
        xff_forward_enabled: Optional[bool] = None,
        aup_enabled: Optional[bool] = None,
        caution_enabled: Optional[bool] = None,
        aup_block_internet_until_accepted: Optional[bool] = None,
        aup_force_ssl_inspection: Optional[bool] = None,
        surrogate_ip: Optional[bool] = None,
        surrogate_ip_enforced_for_known_browsers: Optional[bool] = None,
        other_sub_location: Optional[bool] = None,
        other6_sub_location: Optional[bool] = None,
        ofw_enabled: Optional[bool] = None,
        ips_control: Optional[bool] = None,
        zapp_ssl_scan_enabled: Optional[bool] = None,
        ipv6_enabled: Optional[bool] = None,
        ec_location: Optional[bool] = None,
        kerberos_auth: Optional[bool] = None,
        digest_auth_enabled: Optional[bool] = None,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.tz = tz
        self.xff_forward_enabled = xff_forward_enabled
        self.aup_enabled = aup_enabled
        self.caution_enabled = caution_enabled
        self.aup_block_internet_until_accepted = aup_block_internet_until_accepted
        self.aup_force_ssl_inspection = aup_force_ssl_inspection
        self.surrogate_ip = surrogate_ip
        self.surrogate_ip_enforced_for_known_browsers = surrogate_ip_enforced_for_known_browsers
        self.other_sub_location = other_sub_location
        self.other6_sub_location = other6_sub_location
        self.ofw_enabled = ofw_enabled
        self.ips_control = ips_control
        self.zapp_ssl_scan_enabled = zapp_ssl_scan_enabled
        self.ipv6_enabled = ipv6_enabled
        self.ec_location = ec_location
        self.kerberos_auth = kerberos_auth
        self.digest_auth_enabled = digest_auth_enabled

        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)


class LocationLiteService:
    locations_lite_endpoint = "/location/lite"

    def __init__(self, client: ZCONClient):
        self.client = client

    def _check_response(self, response: Response) -> Union[None, dict]:
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                raise Exception(f"Request failed with status code: {status_code}")
        return response

    def get(self, location_id: int) -> Optional[LocationLite]:
        all_loc = self.get_all()
        if all_loc:
            for loc in all_loc:
                if loc.id == location_id:
                    return loc
        return None

    def get_by_name(self, location_name: str) -> Optional[LocationLite]:
        response = self.client.get(f"{self.locations_lite_endpoint}?name={location_name}")
        data = self._check_response(response)
        if data:
            for loc in data:
                if loc["name"].lower() == location_name.lower():
                    return LocationLite(**loc)
        raise ValueError(f"No location found with name: {location_name}")

    def get_all(self) -> List[LocationLite]:
        response, _ = self.client.get_paginated_data(path=self.locations_lite_endpoint)
        data = self._check_response(response)
        if data:
            return [LocationLite(**loc) for loc in data]
        return []
