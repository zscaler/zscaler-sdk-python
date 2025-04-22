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
from zscaler.ztw.models import ecgroup as ecgroup


class ECGroupVM(ZscalerObject):
    """
    A class for Ecgroupvm objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Ecgroupvm model based on API response.

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

            self.ec_instances = ZscalerCollection.form_list(
                config["ecInstances"] if "ecInstances" in config else [], ecgroup.ECInstances
            )

            if "managementNw" in config:
                if isinstance(config["managementNw"], ecgroup.ManagementNW):
                    self.management_nw = config["managementNw"]
                elif config["managementNw"] is not None:
                    self.management_nw = ecgroup.ManagementNW(config["managementNw"])
                else:
                    self.management_nw = None
            else:
                self.management_nw = None

            if "dns" in config:
                if isinstance(config["dns"], ecgroup.DNS):
                    self.dns = config["dns"]
                elif config["dns"] is not None:
                    self.dns = ecgroup.DNS(config["dns"])
                else:
                    self.dns = None
            else:
                self.dns = None

        else:
            self.id = None
            self.name = None
            self.status = ZscalerCollection.form_list([], str)
            self.operational_status = None
            self.form_factor = None
            self.management_nw = None
            self.ec_instances = ZscalerCollection.form_list([], str)
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
            "managementNw": self.management_nw,
            "ecInstances": self.ec_instances,
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
