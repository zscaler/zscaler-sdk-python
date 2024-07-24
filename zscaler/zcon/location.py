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

from typing import List, Optional, Dict, Any, Union

from zscaler.utils import snake_to_camel
from zscaler.zcon.client import ZCONClient
from typing import List, Optional
from requests import Response


class CloudMeta:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        self.id = id
        self.name = name

        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class VPCInfo:
    def __init__(
        self,
        cloud_provider: Optional[str] = None,
        cloud_meta: Optional[CloudMeta] = None,
        **kwargs,
    ):
        self.cloud_provider = cloud_provider
        self.cloud_meta = cloud_meta

        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "cloud_meta":
                    payload[snake_to_camel(key)] = self.cloud_meta.to_api_payload()
                else:
                    payload[snake_to_camel(key)] = value
        return payload


class VPNCredentials:
    def __init__(
        self,
        id: Optional[int] = None,
        type: Optional[str] = None,
        fqdn: Optional[str] = None,
        ip_address: str = None,
        pre_shared_key: Optional[str] = None,
        comments: Optional[str] = None,
        managed_by: Optional[List[Dict[str, Any]]] = None,
        **kwargs,
    ):
        self.id = id
        self.type = type
        self.fqdn = fqdn
        self.ip_address = ip_address
        self.pre_shared_key = pre_shared_key
        self.comments = comments
        self.managed_by = managed_by

        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class GeneralPurpose:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        is_name_l10n_tag: Optional[bool] = None,
        extensions: Optional[Dict[str, Any]] = None,
        deleted: Optional[bool] = None,
        external_id: Optional[str] = None,
        association_time: Optional[int] = None,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.is_name_l10n_tag = is_name_l10n_tag
        self.extensions = extensions
        self.deleted = deleted
        self.external_id = external_id
        self.association_time = association_time

        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class Location:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        parent_id: Optional[int] = None,
        up_bandwidth: Optional[int] = None,
        dn_bandwidth: Optional[int] = None,
        override_up_bandwidth: Optional[int] = None,
        override_dn_bandwidth: Optional[int] = None,
        shared_up_bandwidth: Optional[int] = None,
        shared_down_bandwidth: Optional[int] = None,
        unused_up_bandwidth: Optional[int] = None,
        country: Optional[str] = None,
        state: Optional[str] = None,
        language: Optional[str] = None,
        tz: Optional[str] = None,
        ip_addresses: Optional[List[str]] = None,
        ports: Optional[List[str]] = None,
        auth_required: bool = False,
        ssl_scan_enabled: bool = False,
        zapp_ssl_scan_enabled: bool = False,
        xff_forward_enabled: bool = False,
        other_sub_location: Optional[bool] = None,
        other6_sub_location: Optional[bool] = None,
        ec_location: bool = False,
        surrogate_ip: bool = False,
        idle_time_in_minutes: Optional[int] = None,
        display_time_unit: Optional[str] = None,
        surrogate_ip_enforced_for_known_browsers: bool = False,
        surrogate_refresh_time_in_minutes: Optional[int] = None,
        surrogate_refresh_time_unit: Optional[str] = None,
        ofw_enabled: bool = False,
        ips_control: bool = False,
        aup_enabled: bool = False,
        caution_enabled: bool = False,
        aup_block_internet_until_accepted: bool = False,
        aup_force_ssl_inspection: bool = False,
        aup_timeout_in_days: Optional[int] = None,
        profile: Optional[str] = None,
        description: Optional[str] = None,
        ipv6_enabled: bool = False,
        ipv6_dns64_prefix: Optional[str] = None,
        kerberos_auth: bool = False,
        digest_auth_enabled: bool = False,
        child_count: Optional[int] = None,
        match_in_child: bool = False,
        exclude_from_dynamic_groups: bool = False,
        exclude_from_manual_groups: bool = False,
        vpn_credentials: Optional[List[VPNCredentials]] = None,
        virtual_zens: Optional[List[GeneralPurpose]] = None,
        virtual_zen_clusters: Optional[List[GeneralPurpose]] = None,
        static_location_groups: Optional[List[GeneralPurpose]] = None,
        dynamic_location_groups: Optional[List[GeneralPurpose]] = None,
        public_cloud_account_id: Optional[List[GeneralPurpose]] = None,
        vpc_info: Optional[VPCInfo] = None,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.up_bandwidth = up_bandwidth
        self.dn_bandwidth = dn_bandwidth
        self.override_up_bandwidth = override_up_bandwidth
        self.override_dn_bandwidth = override_dn_bandwidth
        self.shared_up_bandwidth = shared_up_bandwidth
        self.shared_down_bandwidth = shared_down_bandwidth
        self.unused_up_bandwidth = unused_up_bandwidth
        self.country = country
        self.state = state
        self.language = language
        self.tz = tz
        self.ip_addresses = ip_addresses
        self.ports = ports
        self.auth_required = auth_required
        self.ssl_scan_enabled = ssl_scan_enabled
        self.zapp_ssl_scan_enabled = zapp_ssl_scan_enabled
        self.xff_forward_enabled = xff_forward_enabled
        self.other_sub_location = other_sub_location
        self.other6_sub_location = other6_sub_location
        self.ec_location = ec_location
        self.surrogate_ip = surrogate_ip
        self.idle_time_in_minutes = idle_time_in_minutes
        self.display_time_unit = display_time_unit
        self.surrogate_ip_enforced_for_known_browsers = surrogate_ip_enforced_for_known_browsers
        self.surrogate_refresh_time_in_minutes = surrogate_refresh_time_in_minutes
        self.surrogate_refresh_time_unit = surrogate_refresh_time_unit
        self.ofw_enabled = ofw_enabled
        self.ips_control = ips_control
        self.aup_enabled = aup_enabled
        self.caution_enabled = caution_enabled
        self.aup_block_internet_until_accepted = aup_block_internet_until_accepted
        self.aup_force_ssl_inspection = aup_force_ssl_inspection
        self.aup_timeout_in_days = aup_timeout_in_days
        self.profile = profile
        self.description = description
        self.ipv6_enabled = ipv6_enabled
        self.ipv6_dns64_prefix = ipv6_dns64_prefix
        self.kerberos_auth = kerberos_auth
        self.digest_auth_enabled = digest_auth_enabled
        self.child_count = child_count
        self.match_in_child = match_in_child
        self.exclude_from_dynamic_groups = exclude_from_dynamic_groups
        self.exclude_from_manual_groups = exclude_from_manual_groups
        self.vpn_credentials = vpn_credentials
        self.virtual_zens = virtual_zens
        self.virtual_zen_clusters = virtual_zen_clusters
        self.static_location_groups = static_location_groups
        self.dynamic_location_groups = dynamic_location_groups
        self.public_cloud_account_id = public_cloud_account_id
        self.vpc_info = vpc_info

        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "virtual_zens":
                    payload[snake_to_camel(key)] = [i.to_api_payload() for i in self.virtual_zens]
                elif key == "virtual_zen_clusters":
                    payload[snake_to_camel(key)] = [i.to_api_payload() for i in self.virtual_zen_clusters]
                elif key == "static_location_groups":
                    payload[snake_to_camel(key)] = [i.to_api_payload() for i in self.static_location_groups]
                elif key == "dynamic_location_groups":
                    payload[snake_to_camel(key)] = [i.to_api_payload() for i in self.dynamic_location_groups]
                elif key == "public_cloud_account_id":
                    payload[snake_to_camel(key)] = [i.to_api_payload() for i in self.public_cloud_account_id]
                else:
                    payload[snake_to_camel(key)] = value
        return payload


class LocationService:
    locations_endpoint = "/location"

    def __init__(self, client: ZCONClient):
        self.client = client

    def _check_response(self, response: Response) -> Union[None, dict]:
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                raise Exception(f"Request failed with status code: {status_code}")
        return response

    def get(self, location_id: int) -> Optional[Location]:
        response = self.client.get(f"{self.locations_endpoint}/{location_id}")
        data = self._check_response(response)
        return Location(**data)

    def get_by_name(self, location_name: str) -> Optional[Location]:
        response = self.client.get(self.locations_endpoint)
        data = self._check_response(response)
        locations = [Location(**loc) for loc in data]
        for location in locations:
            if location.name.lower() == location_name.lower():
                return location
        raise ValueError(f"No location found with name: {location_name}")

    def create(self, location: Location) -> Optional[Location]:
        payload = location.to_api_payload()
        response = self.client.post(self.locations_endpoint, json=payload)
        data = self._check_response(response)
        return Location(**data)

    def update(self, location_id: int, location: Location) -> Optional[Location]:
        payload = location.to_api_payload()
        response = self.client.put(f"{self.locations_endpoint}/{location_id}", json=payload)
        data = self._check_response(response)
        return Location(**data)

    def delete(self, location_id: int) -> None:
        response = self.client.delete(f"{self.locations_endpoint}/{location_id}")
        self._check_response(response)

    def get_all(self) -> List[Location]:
        response, _ = self.client.get_paginated_data(path=self.locations_endpoint)
        data = self._check_response(response)
        locations = [Location(**loc) for loc in data]
        return locations
