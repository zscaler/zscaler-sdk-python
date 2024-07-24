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


class PublicCloudAccountDetails:
    def __init__(
        self,
        id: Optional[int] = None,
        account_id: Optional[str] = None,
        platform_id: Optional[str] = None,
        **kwargs,
    ):
        self.id = id
        self.account_id = account_id
        self.platform_id = platform_id

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class PublicCloudAccountIDStatus:
    def __init__(
        self,
        account_id_enabled: bool = False,
        sub_id_enabled: bool = False,
        project_id_enabled: bool = False,
        **kwargs,
    ):
        self.account_id_enabled = account_id_enabled
        self.sub_id_enabled = sub_id_enabled
        self.project_id_enabled = project_id_enabled

        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class PublicCloudAccountService:
    public_cloud_endpoint = "/publicCloudAccountDetails"
    public_cloud_endpoint_lite = "/publicCloudAccountDetails/lite"
    public_cloud_account_status = "/publicCloudAccountIdStatus"

    def __init__(self, client: ZCONClient):
        self.client = client

    def _check_response(self, response: Response) -> Union[None, dict]:
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                raise Exception(f"Request failed with status code: {status_code}")
        return response

    def get(self, account_id: int) -> Optional[PublicCloudAccountDetails]:
        response = self.client.get(f"{self.public_cloud_endpoint}/{account_id}")
        data = self._check_response(response)
        return PublicCloudAccountDetails(**data)

    def get_lite(self) -> List[PublicCloudAccountDetails]:
        response = self.client.get(self.public_cloud_endpoint_lite)
        data = self._check_response(response)
        return [PublicCloudAccountDetails(**account) for account in data]

    def get_account_status(self) -> Optional[PublicCloudAccountIDStatus]:
        response = self.client.get(self.public_cloud_account_status)
        data = self._check_response(response)
        return PublicCloudAccountIDStatus(**data)

    def get_all(self) -> List[PublicCloudAccountDetails]:
        response, _ = self.client.get_paginated_data(path=self.public_cloud_endpoint)
        data = self._check_response(response)
        return [PublicCloudAccountDetails(**account) for account in data]
