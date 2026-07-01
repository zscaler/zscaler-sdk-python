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
from zscaler.zpa.models import app_connector_groups as app_connector_groups
from zscaler.zpa.models import private_cloud_group as private_cloud_group
from zscaler.zpa.models import service_edge_groups as service_edge_groups


class PrivateCloud(ZscalerObject):
    """
    A class representing a PrivateCloud object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.description = config["description"] if "description" in config else None
            self.enabled = config["enabled"] if "enabled" in config else False
            self.fire_drill_enabled = config["fireDrillEnabled"] if "fireDrillEnabled" in config else False
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.re_enroll_period = config["reEnrollPeriod"] if "reEnrollPeriod" in config else None
            self.read_only = config["readOnly"] if "readOnly" in config else False
            self.remote_lss = config["remoteLss"] if "remoteLss" in config else False
            self.restriction_type = config["restrictionType"] if "restrictionType" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
            self.site_controller_group_ids = ZscalerCollection.form_list(
                config["siteControllerGroupIds"] if "siteControllerGroupIds" in config else [],
                private_cloud_group.PrivateCloudGroup,
            )
            self.private_broker_group_ids = ZscalerCollection.form_list(
                config["privateBrokerGroupIds"] if "privateBrokerGroupIds" in config else [],
                service_edge_groups.ServiceEdgeGroup,
            )
            self.siem_ids = ZscalerCollection.form_list(
                config["siemIds"] if "siemIds" in config else [], app_connector_groups.AppConnectorGroup
            )
            self.assistant_groups_ids = ZscalerCollection.form_list(
                config["assistantGroupsIds"] if "assistantGroupsIds" in config else [], app_connector_groups.AppConnectorGroup
            )
            self.sitec_preferred = config["sitecPreferred"] if "sitecPreferred" in config else False
            if "zpnFireDrillSite" in config:
                if isinstance(config["zpnFireDrillSite"], ZpnFiredrillSite):
                    self.zpn_fire_drill_site = config["zpnFireDrillSite"]
                elif config["zpnFireDrillSite"] is not None:
                    self.zpn_fire_drill_site = ZpnFiredrillSite(config["zpnFireDrillSite"])
                else:
                    self.zpn_fire_drill_site = None
            else:
                self.zpn_fire_drill_site = None
            self.zscaler_managed = config["zscalerManaged"] if "zscalerManaged" in config else False
        else:
            self.assistant_groups_ids = []
            self.creation_time = None
            self.description = None
            self.enabled = False
            self.fire_drill_enabled = False
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.private_broker_group_ids = []
            self.re_enroll_period = None
            self.read_only = False
            self.remote_lss = False
            self.restriction_type = None
            self.microtenant_id = None
            self.microtenant_name = None
            self.siem_ids = []
            self.site_controller_group_ids = []
            self.sitec_preferred = False
            self.zpn_fire_drill_site = None
            self.zscaler_managed = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "assistantGroupsIds": [item.request_format() for item in (self.assistant_groups_ids or [])],
            "creationTime": self.creation_time,
            "description": self.description,
            "enabled": self.enabled,
            "fireDrillEnabled": self.fire_drill_enabled,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "privateBrokerGroupIds": [item.request_format() for item in (self.private_broker_group_ids or [])],
            "reEnrollPeriod": self.re_enroll_period,
            "readOnly": self.read_only,
            "remoteLss": self.remote_lss,
            "restrictionType": self.restriction_type,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "siemIds": [item.request_format() for item in (self.siem_ids or [])],
            "siteControllerGroupIds": [item.request_format() for item in (self.site_controller_group_ids or [])],
            "sitecPreferred": self.sitec_preferred,
            "zpnFireDrillSite": self.zpn_fire_drill_site,
            "zscalerManaged": self.zscaler_managed,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ZpnFiredrillSite(ZscalerObject):
    """
    A class representing a ZpnFiredrillSite object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.fire_drill_interval = config["fireDrillInterval"] if "fireDrillInterval" in config else None
            self.fire_drill_interval_time_unit = (
                config["fireDrillIntervalTimeUnit"] if "fireDrillIntervalTimeUnit" in config else None
            )
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
        else:
            self.creation_time = None
            self.fire_drill_interval = None
            self.fire_drill_interval_time_unit = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.microtenant_id = None
            self.microtenant_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "creationTime": self.creation_time,
            "fireDrillInterval": self.fire_drill_interval,
            "fireDrillIntervalTimeUnit": self.fire_drill_interval_time_unit,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
