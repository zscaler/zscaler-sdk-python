# flake8: noqa
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


class AccountDetails(ZscalerObject):
    """
    A class for AccountDetails nested object.
    """

    def __init__(self, config=None):
        """
        Initialize the AccountDetails model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.aws_account_id = config.get("awsAccountId")
            self.aws_role_name = config.get("awsRoleName")
            self.cloud_watch_group_arn = config.get("cloudWatchGroupArn")
            self.event_bus_name = config.get("eventBusName")
            self.external_id = config.get("externalId")
            self.log_info_type = config.get("logInfoType")
            self.trouble_shooting_logging = config.get("troubleShootingLogging")
            self.trusted_account_id = config.get("trustedAccountId")
            self.trusted_role = config.get("trustedRole")
        else:
            self.aws_account_id = None
            self.aws_role_name = None
            self.cloud_watch_group_arn = None
            self.event_bus_name = None
            self.external_id = None
            self.log_info_type = None
            self.trouble_shooting_logging = None
            self.trusted_account_id = None
            self.trusted_role = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "awsAccountId": self.aws_account_id,
            "awsRoleName": self.aws_role_name,
            "cloudWatchGroupArn": self.cloud_watch_group_arn,
            "eventBusName": self.event_bus_name,
            "externalId": self.external_id,
            "logInfoType": self.log_info_type,
            "troubleShootingLogging": self.trouble_shooting_logging,
            "trustedAccountId": self.trusted_account_id,
            "trustedRole": self.trusted_role,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PublicCloudInfo(ZscalerObject):
    """
    A class for PublicCloudInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PublicCloudInfo model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None

            self.account_groups = ZscalerCollection.form_list(
                config["accountGroups"] if "accountGroups" in config else [], common.CommonIDNameExternalID
            )

            self.cloud_type = config["cloudType"] \
                if "cloudType" in config else None
            self.external_id = config["externalId"] \
                if "externalId" in config else None
            self.last_mod_time = config["lastModTime"] \
                if "lastModTime" in config else None
            self.last_sync_time = config["lastSyncTime"] \
                if "lastSyncTime" in config else None
            self.permission_status = config["permissionStatus"] \
                if "permissionStatus" in config else None
                
            self.region_status = ZscalerCollection.form_list(
                config["regionStatus"] if "regionStatus" in config else [], common.CommonPublicCloudInfo
            )

            self.supported_regions = ZscalerCollection.form_list(
                config["supportedRegions"] if "supportedRegions" in config else [], common.CommonPublicCloudInfo
            )

            if "lastModUser" in config:
                if isinstance(config["lastModUser"], common.CommonIDNameExternalID):
                    self.last_mod_user = config["lastModUser"]
                elif config["lastModUser"] is not None:
                    self.last_mod_user = common.CommonIDNameExternalID(config["lastModUser"])
                else:
                    self.last_mod_user = None
            else:
                self.last_mod_user = None

            if "accountDetails" in config:
                if isinstance(config["accountDetails"], AccountDetails):
                    self.account_details = config["accountDetails"]
                elif config["accountDetails"] is not None:
                    self.account_details = AccountDetails(config["accountDetails"])
                else:
                    self.account_details = None
            else:
                self.account_details = None

        else:
            self.id = None
            self.name = None
            self.account_details = None
            self.account_groups = []
            self.cloud_type = None
            self.external_id = None
            self.last_mod_time = None
            self.last_mod_user = None
            self.last_sync_time = None
            self.permission_status = None
            self.region_status = []
            self.supported_regions = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "accountDetails": self.account_details,
            "accountGroups": self.account_groups,
            "cloudType": self.cloud_type,
            "externalId": self.external_id,
            "lastModTime": self.last_mod_time,
            "lastModUser": self.last_mod_user,
            "lastSyncTime": self.last_sync_time,
            "permissionStatus": self.permission_status,
            "regionStatus": self.region_status,
            "supportedRegions": self.supported_regions
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
