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

from typing import Dict, Any, Optional, Union

from requests import Response

from zscaler.utils import snake_to_camel
from zscaler.zcon.client import ZCONClient


class ECAdminActivation:
    def __init__(
        self,
        org_edit_status: Optional[str] = None,
        org_last_activate_status: Optional[str] = None,
        admin_status_map: Optional[Dict[str, Any]] = None,
        admin_activate_status: Optional[str] = None,
    ):
        self.org_edit_status = org_edit_status
        self.org_last_activate_status = org_last_activate_status
        self.admin_status_map = admin_status_map
        self.admin_activate_status = admin_activate_status

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class ActivationService:
    ec_admin_activate_status_endpoint = "/ecAdminActivateStatus"
    ec_admin_activate_endpoint = "/ecAdminActivateStatus/activate"
    ec_admin_force_activate_endpoint = "/ecAdminActivateStatus/forcedActivate"

    def __init__(self, client: ZCONClient):
        self.client = client

    def _check_response(self, response: Response) -> Union[None, dict]:
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                raise Exception(f"Request failed with status code: {status_code}")
        return response

    def get_activation_status(self) -> Optional[ECAdminActivation]:
        """
        Returns the activation status for a configuration change.

        Returns:
            :obj:`str`
                Configuration status.

        Examples:
            >>> status = zcon.activation.get_activation_status()

        """
        response = self.client.get(self.ec_admin_activate_status_endpoint)
        data = self._check_response(response)
        return ECAdminActivation(**data)

    def update_activation_status(self, activation: ECAdminActivation) -> Optional[ECAdminActivation]:
        """
        Activates configuration changes.

        Returns:
            :obj:`str`
                Activates configuration changes.

        Examples:
            >>> activate = zcon.activation.update_activation_status()

        """
        payload = activation.to_api_payload()
        response = self.client.put(self.ec_admin_activate_endpoint, json=payload)
        data = self._check_response(response)
        return ECAdminActivation(**data)

    def force_activation_status(self, activation: ECAdminActivation) -> Optional[ECAdminActivation]:
        """
        Force activates configuration changes.

        Returns:
            :obj:`str`
                Force activates.

        Examples:
            >>> activate = zcon.activation.force_activation_status()

        """
        payload = activation.to_api_payload()
        response = self.client.put(self.ec_admin_force_activate_endpoint, json=payload)
        data = self._check_response(response)
        return ECAdminActivation(**data)
