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

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection
from zscaler.ztw.models import common as common


class ECGroup(ZscalerObject):
    """
    A class for Ecgroup objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Ecgroup model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.desc = config["desc"] if "desc" in config else None
            self.deploy_type = config["deployType"] if "deployType" in config else None
            self.status = ZscalerCollection.form_list(config["status"] if "status" in config else [], str)
            self.platform = config["platform"] if "platform" in config else None
            self.aws_availability_zone = config["awsAvailabilityZone"] if "awsAvailabilityZone" in config else None
            self.azure_availability_zone = config["azureAvailabilityZone"] if "azureAvailabilityZone" in config else None
            self.max_ec_count = config["maxEcCount"] if "maxEcCount" in config else None
            self.tunnel_mode = config["tunnelMode"] if "tunnelMode" in config else None

            self.ec_vms = ZscalerCollection.form_list(config["ecVMs"] if "ecVMs" in config else [], ECVMS)

            if "location" in config:
                if isinstance(config["location"], common.CommonIDNameExternalID):
                    self.location = config["location"]
                elif config["location"] is not None:
                    self.location = common.CommonIDNameExternalID(config["location"])
                else:
                    self.location = None
            else:
                self.location = None

            if "provTemplate" in config:
                if isinstance(config["provTemplate"], common.CommonIDNameExternalID):
                    self.prov_template = config["provTemplate"]
                elif config["provTemplate"] is not None:
                    self.prov_template = common.CommonIDNameExternalID(config["provTemplate"])
                else:
                    self.prov_template = None
            else:
                self.prov_template = None

        else:
            self.id = None
            self.name = None
            self.desc = None
            self.deploy_type = None
            self.status = ZscalerCollection.form_list([], str)
            self.platform = None
            self.aws_availability_zone = None
            self.azure_availability_zone = None
            self.location = None
            self.max_ec_count = None
            self.prov_template = None
            self.tunnel_mode = None
            self.ec_v_ms = ZscalerCollection.form_list([], str)

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "deployType": self.deploy_type,
            "status": self.status,
            "platform": self.platform,
            "awsAvailabilityZone": self.aws_availability_zone,
            "azureAvailabilityZone": self.azure_availability_zone,
            "location": self.location,
            "maxEcCount": self.max_ec_count,
            "provTemplate": self.prov_template,
            "tunnelMode": self.tunnel_mode,
            "ecVMs": self.ec_v_ms,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ECVMS(ZscalerObject):
    """
    A class for ECVMS objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ECVMS model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.status = ZscalerCollection.form_list(config["status"] if "status" in config else [], str)
            self.operational_status = config["operationalStatus"] if "operationalStatus" in config else None
            self.form_factor = config["formFactor"] if "formFactor" in config else None

            if "managementNw" in config:
                if isinstance(config["managementNw"], ManagementNW):
                    self.management_nw = config["managementNw"]
                elif config["managementNw"] is not None:
                    self.management_nw = ManagementNW(config["managementNw"])
                else:
                    self.management_nw = None
            else:
                self.management_nw = None

            self.ec_instances = ZscalerCollection.form_list(
                config["ecInstances"] if "ecInstances" in config else [], EcInstance
            )

            self.city_geo_id = config["cityGeoId"] if "cityGeoId" in config else None
            self.nat_ip = config["natIp"] if "natIp" in config else None
            self.zia_gateway = config["ziaGateway"] if "ziaGateway" in config else None
            self.zpa_broker = config["zpaBroker"] if "zpaBroker" in config else None
            self.build_version = config["buildVersion"] if "buildVersion" in config else None
            self.last_upgrade_time = config["lastUpgradeTime"] if "lastUpgradeTime" in config else None
            self.upgrade_status = config["upgradeStatus"] if "upgradeStatus" in config else None
            self.upgrade_start_time = config["upgradeStartTime"] if "upgradeStartTime" in config else None
            self.upgrade_end_time = config["upgradeEndTime"] if "upgradeEndTime" in config else None
            self.upgrade_day_of_week = config["upgradeDayOfWeek"] if "upgradeDayOfWeek" in config else None

        else:
            self.id = None
            self.name = None
            self.status = ZscalerCollection.form_list([], str)
            self.operational_status = None
            self.form_factor = None
            self.management_nw = None
            self.ec_instances = ZscalerCollection.form_list([], EcInstance)
            self.city_geo_id = None
            self.nat_ip = None
            self.zia_gateway = None
            self.zpa_broker = None
            self.build_version = None
            self.last_upgrade_time = None
            self.upgrade_status = None
            self.upgrade_start_time = None
            self.upgrade_end_time = None
            self.upgrade_day_of_week = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "operationalStatus": self.operational_status,
            "formFactor": self.form_factor,
            "managementNw": self.management_nw.request_format() if self.management_nw else None,
            "ecInstances": [instance.request_format() for instance in self.ec_instances],
            "cityGeoId": self.city_geo_id,
            "natIp": self.nat_ip,
            "ziaGateway": self.zia_gateway,
            "zpaBroker": self.zpa_broker,
            "buildVersion": self.build_version,
            "lastUpgradeTime": self.last_upgrade_time,
            "upgradeStatus": self.upgrade_status,
            "upgradeStartTime": self.upgrade_start_time,
            "upgradeEndTime": self.upgrade_end_time,
            "upgradeDayOfWeek": self.upgrade_day_of_week,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class EcInstance(ZscalerObject):
    """
    A class for ECInstance objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ECInstance model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.instance_type = config["instanceType"] if "instanceType" in config else None
            self.service_ips = config["serviceIps"] if "serviceIps" in config else None
        else:
            self.id = None
            self.instance_type = None
            self.service_ips = None


class ManagementNW(ZscalerObject):
    """
    A class for ManagementNW objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ManagementNW model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.ip_start = config["ipStart"] if "ipStart" in config else None
            self.ip_end = config["ipEnd"] if "ipEnd" in config else None
            self.netmask = config["netmask"] if "netmask" in config else None
            self.default_gateway = config["defaultGateway"] if "defaultGateway" in config else None
            self.nw_type = config["nwType"] if "nwType" in config else None

            if "dns" in config:
                if isinstance(config["dns"], DNS):
                    self.dns = config["dns"]
                elif config["dns"] is not None:
                    self.dns = DNS(config["dns"])
                else:
                    self.dns = None
            else:
                self.dns = None
        else:
            self.id = None
            self.ip_start = None
            self.ip_end = None
            self.netmask = None
            self.default_gateway = None
            self.management_nw = None
            self.nw_type = None
            self.dns = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "ipStart": self.ip_start,
            "ipEnd": self.ip_end,
            "netmask": self.netmask,
            "defaultGateway": self.default_gateway,
            "nwType": self.nw_type,
            "dns": self.dns,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DNS(ZscalerObject):
    """
    A class for DNS objects.
    """

    def __init__(self, config=None):
        """
        Initialize the DNS model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.dns_type = config["dnsType"] if "dnsType" in config else None
            self.ips = ZscalerCollection.form_list(config["ips"] if "ips" in config else [], str)

        else:
            self.id = None
            self.ips = None
            self.dns_type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "ips": self.ips,
            "dnsType": self.dns_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ECInstances(ZscalerObject):
    """
    A class for ECInstances objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ECInstances model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.instance_type = config["instanceType"] if "instanceType" in config else None
            self.out_gwip = config["outGwIp"] if "outGwIp" in config else None
            self.nat_ip = config["natIp"] if "natIp" in config else None
            self.dns_ip = config["dnsIp"] if "dnsIp" in config else None
            self.nw_type = config["nwType"] if "nwType" in config else None

            if "serviceIps" in config:
                if isinstance(config["serviceIps"], ServiceIPs):
                    self.service_ips = config["serviceIps"]
                elif config["serviceIps"] is not None:
                    self.service_ips = ServiceIPs(config["serviceIps"])
                else:
                    self.service_ips = None
            else:
                self.service_ips = None

            if "lbIpAddr" in config:
                if isinstance(config["lbIpAddr"], LBIPAddr):
                    self.lb_ip_addr = config["lbIpAddr"]
                elif config["lbIpAddr"] is not None:
                    self.lb_ip_addr = LBIPAddr(config["lbIpAddr"])
                else:
                    self.lb_ip_addr = None
            else:
                self.lb_ip_addr = None

        else:
            self.id = None
            self.instance_type = None
            self.out_gwip = None
            self.nat_ip = None
            self.dns_ip = None
            self.nw_type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "instanceType": self.instance_type,
            "outGwIp": self.out_gwip,
            "natIp": self.nat_ip,
            "dnsIp": self.dns_ip,
            "nwType": self.nw_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ServiceIPs(ZscalerObject):
    """
    A class for ServiceIPs objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ServiceIPs model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.ip_start = config["ipStart"] if "ipStart" in config else None
            self.ip_end = config["ipEnd"] if "ipEnd" in config else None

        else:
            self.ip_start = None
            self.ip_end = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ipStart": self.ip_start,
            "ipEnd": self.ip_end,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LBIPAddr(ZscalerObject):
    """
    A class for LBIPAddr objects.
    """

    def __init__(self, config=None):
        """
        Initialize the LBIPAddr model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.ip_start = config["ipStart"] if "ipStart" in config else None
            self.ip_end = config["ipEnd"] if "ipEnd" in config else None

        else:
            self.ip_start = None
            self.ip_end = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ipStart": self.ip_start,
            "ipEnd": self.ip_end,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
