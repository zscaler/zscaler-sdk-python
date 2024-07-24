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

from typing import List, Dict, Any, Optional, Union
from zscaler.utils import snake_to_camel
from zscaler.zcon.client import ZCONClient
from requests import Response
import logging


class DNS:
    def __init__(
        self,
        id: Optional[int] = None,
        ips: Optional[List[str]] = None,
        dns_type: Optional[str] = None,
        **kwargs,
    ):
        self.id = id
        self.ips = ips
        self.dns_type = dns_type
        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                payload[snake_to_camel(key)] = value
        return payload


class ManagementNw:
    def __init__(
        self,
        id: Optional[int] = None,
        ip_start: Optional[str] = None,
        ip_end: Optional[str] = None,
        netmask: Optional[str] = None,
        default_gateway: Optional[str] = None,
        nw_type: Optional[str] = None,
        dns: Optional[DNS] = None,
        **kwargs,
    ):
        self.id = id
        self.ip_start = ip_start
        self.ip_end = ip_end
        self.netmask = netmask
        self.default_gateway = default_gateway
        self.nw_type = nw_type
        self.dns = dns
        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "dns":
                    payload[snake_to_camel(key)] = self.dns.to_api_payload()
                else:
                    payload[snake_to_camel(key)] = value
        return payload


class ECInstances:
    def __init__(
        self,
        service_nw: Optional[ManagementNw] = None,
        virtual_nw: Optional[ManagementNw] = None,
        ec_instance_type: Optional[str] = None,
        out_gw_ip: Optional[str] = None,
        nat_ip: Optional[str] = None,
        dns_ip: Optional[str] = None,
        **kwargs,
    ):
        self.service_nw = service_nw
        self.virtual_nw = virtual_nw
        self.ec_instance_type = ec_instance_type
        self.out_gw_ip = out_gw_ip
        self.nat_ip = nat_ip
        self.dns_ip = dns_ip
        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "service_nw":
                    payload[snake_to_camel(key)] = self.service_nw.to_api_payload()
                elif key == "virtual_nw":
                    payload[snake_to_camel(key)] = self.virtual_nw.to_api_payload()
                else:
                    payload[snake_to_camel(key)] = value
        return payload


class GeneralPurpose:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        is_name_l10n_tag: Optional[bool] = None,
        extensions: Optional[dict] = None,
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


class ECVMs:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        form_factor: Optional[str] = None,
        city_geo_id: Optional[int] = None,
        nat_ip: Optional[str] = None,
        zia_gateway: Optional[str] = None,
        zpa_broker: Optional[str] = None,
        build_version: Optional[str] = None,
        last_upgrade_time: Optional[int] = None,
        upgrade_status: Optional[int] = None,
        upgrade_start_time: Optional[int] = None,
        upgrade_end_time: Optional[int] = None,
        management_nw: Optional[ManagementNw] = None,
        ec_instances: Optional[List[ECInstances]] = None,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.form_factor = form_factor
        self.city_geo_id = city_geo_id
        self.nat_ip = nat_ip
        self.zia_gateway = zia_gateway
        self.zpa_broker = zpa_broker
        self.build_version = build_version
        self.last_upgrade_time = last_upgrade_time
        self.upgrade_status = upgrade_status
        self.upgrade_start_time = upgrade_start_time
        self.upgrade_end_time = upgrade_end_time
        self.management_nw = management_nw
        self.ec_instances = ec_instances
        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "management_nw":
                    payload[snake_to_camel(key)] = self.management_nw.to_api_payload()
                elif key == "ec_instances":
                    payload[snake_to_camel(key)] = [i.to_api_payload() for i in self.ec_instances]
                else:
                    payload[snake_to_camel(key)] = value
        return payload


class EcGroup:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        deploy_type: Optional[str] = None,
        status: Optional[List[str]] = None,
        platform: Optional[str] = None,
        aws_availability_zone: Optional[str] = None,
        azure_availability_zone: Optional[str] = None,
        max_ec_count: Optional[int] = None,
        tunnel_mode: Optional[str] = None,
        location: Optional[GeneralPurpose] = None,
        prov_template: Optional[GeneralPurpose] = None,
        ec_vms: Optional[List[ECVMs]] = None,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.deploy_type = deploy_type
        self.status = status
        self.platform = platform
        self.aws_availability_zone = aws_availability_zone
        self.azure_availability_zone = azure_availability_zone
        self.max_ec_count = max_ec_count
        self.tunnel_mode = tunnel_mode
        self.location = location
        self.prov_template = prov_template
        self.ec_vms = ec_vms
        # Store any additional keyword arguments as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_api_payload(self):
        payload = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "location":
                    payload[snake_to_camel(key)] = self.location.to_api_payload()
                elif key == "prov_template":
                    payload[snake_to_camel(key)] = self.prov_template.to_api_payload()
                elif key == "ec_vms":
                    payload[snake_to_camel(key)] = [i.to_api_payload() for i in self.ec_vms]
                else:
                    payload[snake_to_camel(key)] = value
        return payload


class EcGroupService:
    ecgroup_endpoint = "/ecgroup"
    ecgroup_lite_endpoint = "/ecgroup/lite"

    def __init__(self, client: ZCONClient):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def _check_response(self, response: Response) -> Union[None, dict]:
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                raise Exception(f"Request failed with status code: {status_code}")
        return response

    def get(self, ecgroup_id: int) -> Optional[EcGroup]:
        response = self.client.get(f"{self.ecgroup_endpoint}/{ecgroup_id}")
        data = self._check_response(response)
        return EcGroup(**data)

    def get_by_name(self, ecgroup_name: str) -> Optional[EcGroup]:
        response = self.client.get(self.ecgroup_endpoint)
        data = self._check_response(response)
        ecgroups = [EcGroup(**ecgroup) for ecgroup in data]
        for ecgroup in ecgroups:
            if ecgroup.name.lower() == ecgroup_name.lower():
                return ecgroup
        raise Exception(f"No EC Group found with name: {ecgroup_name}")

    def delete(self, ecgroup_id: int) -> None:
        response = self.client.delete(f"{self.ecgroup_endpoint}/{ecgroup_id}")
        self._check_response(response)

    def get_all(self) -> List[EcGroup]:
        response = self.client.get(self.ecgroup_endpoint)
        data = self._check_response(response)
        return [EcGroup(**ecgroup) for ecgroup in data]

    def get_ecgroup_lite(self, ecgroup_id: int) -> Optional[EcGroup]:
        response = self.client.get(f"{self.ecgroup_lite_endpoint}")
        data = self._check_response(response)
        ecgroups = [EcGroup(**ecgroup) for ecgroup in data]
        for ecgroup in ecgroups:
            if ecgroup.id == ecgroup_id:
                return ecgroup
        raise Exception(f"No EC Group Lite found with ID: {ecgroup_id}")

    def get_ecgroup_lite_by_name(self, ecgroup_name: str) -> Optional[EcGroup]:
        response = self.client.get(f"{self.ecgroup_lite_endpoint}?name={ecgroup_name}")
        data = self._check_response(response)
        ecgroups = [EcGroup(**ecgroup) for ecgroup in data]
        for ecgroup in ecgroups:
            if ecgroup.name.lower() == ecgroup_name.lower():
                return ecgroup
        raise Exception(f"No EC Group Lite found with name: {ecgroup_name}")
