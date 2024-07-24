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


class ProvisioningAPIKeys:
    def __init__(
        self,
        id: Optional[int] = None,
        key_value: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        enabled: bool = False,
        last_modified_time: Optional[int] = None,
        last_modified_by: Optional[Dict[str, Any]] = None,
        partner_url: Optional[str] = None,
        **kwargs,
    ):
        self.id = id
        self.key_value = key_value
        self.permissions = permissions
        self.enabled = enabled
        self.last_modified_time = last_modified_time
        self.last_modified_by = last_modified_by
        self.partner_url = partner_url

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class APIKeyProvisioningService:
    api_keys_endpoint = "/apiKeys"
    regenerate_api_keys_endpoint = "/regenerate"

    def __init__(self, client: ZCONClient):
        self.client = client

    def _check_response(self, response: Response) -> Union[None, dict]:
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                raise Exception(f"Request failed with status code: {status_code}")
        return response

    def get(self, api_key_id: int) -> Optional[ProvisioningAPIKeys]:
        response = self.client.get(f"{self.api_keys_endpoint}/{api_key_id}")
        data = self._check_response(response)
        return ProvisioningAPIKeys(**data)

    def get_partner_api_key(self, api_key_value: str, include_partner_key: bool) -> Optional[ProvisioningAPIKeys]:
        url = f"{self.api_keys_endpoint}?includePartnerKey={str(include_partner_key).lower()}"
        response = self.client.get(url)
        data = self._check_response(response)
        api_keys = [ProvisioningAPIKeys(**key) for key in data]
        for key in api_keys:
            if key.key_value == api_key_value:
                return key
        raise ValueError(f"No partner API key found with key value: {api_key_value}")

    def get_all(self) -> List[ProvisioningAPIKeys]:
        response, _ = self.client.get_paginated_data(path=self.api_keys_endpoint)
        data = self._check_response(response)
        return [ProvisioningAPIKeys(**key) for key in data]

    def create(
        self,
        api_key_value: Optional[ProvisioningAPIKeys] = None,
        include_partner_key: bool = False,
        key_id: Optional[int] = None,
    ) -> Optional[ProvisioningAPIKeys]:
        if api_key_value is None:
            api_key_value = ProvisioningAPIKeys()
        if key_id is not None:
            url = f"{self.api_keys_endpoint}/{key_id}{self.regenerate_api_keys_endpoint}?includePartnerKey={str(include_partner_key).lower()}"
        else:
            url = f"{self.api_keys_endpoint}?includePartnerKey={str(include_partner_key).lower()}"
        payload = api_key_value.to_api_payload()
        response = self.client.post(url, json=payload)
        data = self._check_response(response)
        return ProvisioningAPIKeys(**data)
