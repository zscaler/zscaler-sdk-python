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

from typing import Optional, List, Dict, Any, Union

from zscaler.utils import snake_to_camel
from zscaler.zcon.client import ZCONClient
from requests import Response


class LocationTemplateDetails:
    def __init__(
        self,
        template_prefix: Optional[str] = None,
        xff_forward_enabled: bool = False,
        auth_required: bool = False,
        caution_enabled: bool = False,
        aup_enabled: bool = False,
        aup_timeout_in_days: Optional[int] = None,
        ofw_enabled: bool = False,
        ips_control: bool = False,
        enforce_bandwidth_control: bool = False,
        up_bandwidth: Optional[int] = None,
        dn_bandwidth: Optional[int] = None,
        display_time_unit: Optional[str] = None,
        idle_time_in_minutes: Optional[int] = None,
        surrogate_ip_enforced_for_known_browsers: bool = False,
        surrogate_refresh_time_unit: Optional[str] = None,
        surrogate_refresh_time_in_minutes: Optional[int] = None,
        surrogate_ip: bool = False,
        **kwargs,
    ):
        self.template_prefix = template_prefix
        self.xff_forward_enabled = xff_forward_enabled
        self.auth_required = auth_required
        self.caution_enabled = caution_enabled
        self.aup_enabled = aup_enabled
        self.aup_timeout_in_days = aup_timeout_in_days
        self.ofw_enabled = ofw_enabled
        self.ips_control = ips_control
        self.enforce_bandwidth_control = enforce_bandwidth_control
        self.up_bandwidth = up_bandwidth
        self.dn_bandwidth = dn_bandwidth
        self.display_time_unit = display_time_unit
        self.idle_time_in_minutes = idle_time_in_minutes
        self.surrogate_ip_enforced_for_known_browsers = surrogate_ip_enforced_for_known_browsers
        self.surrogate_refresh_time_unit = surrogate_refresh_time_unit
        self.surrogate_refresh_time_in_minutes = surrogate_refresh_time_in_minutes
        self.surrogate_ip = surrogate_ip

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class LocationTemplate:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        location_template_details: Optional[LocationTemplateDetails] = None,
        editable: bool = False,
        last_mod_time: Optional[int] = None,
        last_mod_uid: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.location_template_details = location_template_details
        self.editable = editable
        self.last_mod_time = last_mod_time
        self.last_mod_uid = last_mod_uid

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "location_template_details":
                    payload[snake_to_camel(key)] = self.location_template_details.to_api_payload()
                else:
                    payload[snake_to_camel(key)] = value
        return payload


class LocationTemplateService:
    location_template_endpoint = "/locationTemplate"

    def __init__(self, client: ZCONClient):
        self.client = client

    def _check_response(self, response: Response) -> Union[None, dict]:
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                raise Exception(f"Request failed with status code: {status_code}")
        return response

    def get(self, loc_template_id: int) -> Optional[LocationTemplate]:
        response = self.client.get(f"{self.location_template_endpoint}/{loc_template_id}")
        data = self._check_response(response)
        return LocationTemplate(**data)

    def get_by_name(self, template_name: str) -> Optional[LocationTemplate]:
        response = self.client.get(self.location_template_endpoint)
        data = self._check_response(response)
        templates = [LocationTemplate(**tpl) for tpl in data]
        for template in templates:
            if template.name.lower() == template_name.lower():
                return template
        raise ValueError(f"No location template found with name: {template_name}")

    def create(self, location_template: LocationTemplate) -> Optional[LocationTemplate]:
        payload = location_template.to_api_payload()
        response = self.client.post(self.location_template_endpoint, json=payload)
        data = self._check_response(response)
        return LocationTemplate(**data)

    def update(self, loc_template_id: int, location_template: LocationTemplate) -> Optional[LocationTemplate]:
        payload = location_template.to_api_payload()
        response = self.client.put(f"{self.location_template_endpoint}/{loc_template_id}", json=payload)
        data = self._check_response(response)
        return LocationTemplate(**data)

    def delete(self, loc_template_id: int) -> None:
        response = self.client.delete(f"{self.location_template_endpoint}/{loc_template_id}")
        self._check_response(response)

    def get_all(self) -> List[LocationTemplate]:
        response, _ = self.client.get_paginated_data(path=self.location_template_endpoint)
        data = self._check_response(response)
        templates = [LocationTemplate(**tpl) for tpl in data]
        return templates
