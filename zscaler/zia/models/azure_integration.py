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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject
from zscaler.zia.models import common as common


class AzureVirtualHubConfiguration(ZscalerObject):
    """
    A class representing a AzureVirtualHubConfiguration object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.status = config["status"] if "status" in config else None
            self.details = config["details"] if "details" in config else None
            self.virtual_hubs = ZscalerCollection.form_list(
                config["virtualHubs"] if "virtualHubs" in config else [], AzureVirtualHubConfigurationVirtualHubs
            )
            self.last_sync_time = config["lastSyncTime"] if "lastSyncTime" in config else None
            self.hub_count = config["hubCount"] if "hubCount" in config else None
            self.last_refresh_time = config["lastRefreshTime"] if "lastRefreshTime" in config else None
        else:
            self.status = None
            self.details = None
            self.virtual_hubs = []
            self.last_sync_time = None
            self.hub_count = None
            self.last_refresh_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
            "details": self.details,
            "virtualHubs": [item.request_format() for item in (self.virtual_hubs or [])],
            "lastSyncTime": self.last_sync_time,
            "hubCount": self.hub_count,
            "lastRefreshTime": self.last_refresh_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AzureVirtualHub(ZscalerObject):
    """
    A class representing a AzureVirtualHub object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.resource_group_name = config["resourceGroupName"] if "resourceGroupName" in config else None
            self.virtual_wan = config["virtualWan"] if "virtualWan" in config else None
            self.azure_region = config["azureRegion"] if "azureRegion" in config else None
            self.vpn_gateway = config["vpnGateway"] if "vpnGateway" in config else None
            self.azure_hub_name = config["azureHubName"] if "azureHubName" in config else None
            self.hub_status = config["hubStatus"] if "hubStatus" in config else None
            self.azure_vpn_sites = ZscalerCollection.form_list(
                config["azureVpnSites"] if "azureVpnSites" in config else [], AzureVirtualHubAzureVpnSites
            )
            if "zsLocation" in config:
                if isinstance(config["zsLocation"], common.CommonBlocks):
                    self.zs_location = config["zsLocation"]
                elif config["zsLocation"] is not None:
                    self.zs_location = common.CommonBlocks(config["zsLocation"])
                else:
                    self.zs_location = None
            else:
                self.zs_location = None
            self.zs_ip_address = config["zsIpAddress"] if "zsIpAddress" in config else None
            self.tunnel_configuration_status = (
                config["tunnelConfigurationStatus"] if "tunnelConfigurationStatus" in config else None
            )
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
        else:
            self.id = None
            self.resource_group_name = None
            self.virtual_wan = None
            self.azure_region = None
            self.vpn_gateway = None
            self.azure_hub_name = None
            self.hub_status = None
            self.azure_vpn_sites = []
            self.zs_location = None
            self.zs_ip_address = None
            self.tunnel_configuration_status = None
            self.last_modified_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "resourceGroupName": self.resource_group_name,
            "virtualWan": self.virtual_wan,
            "azureRegion": self.azure_region,
            "vpnGateway": self.vpn_gateway,
            "azureHubName": self.azure_hub_name,
            "hubStatus": self.hub_status,
            "azureVpnSites": [item.request_format() for item in (self.azure_vpn_sites or [])],
            "zsLocation": self.zs_location,
            "zsIpAddress": self.zs_ip_address,
            "tunnelConfigurationStatus": self.tunnel_configuration_status,
            "lastModifiedTime": self.last_modified_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AzureVirtualHubConfigurationVirtualHubs(ZscalerObject):
    """
    A class representing a AzureVirtualHubConfigurationVirtualHubs object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.resource_group_name = config["resourceGroupName"] if "resourceGroupName" in config else None
            self.virtual_wan = config["virtualWan"] if "virtualWan" in config else None
            self.azure_region = config["azureRegion"] if "azureRegion" in config else None
            self.vpn_gateway = config["vpnGateway"] if "vpnGateway" in config else None
            self.azure_hub_name = config["azureHubName"] if "azureHubName" in config else None
            self.hub_status = config["hubStatus"] if "hubStatus" in config else None
            self.azure_vpn_sites = ZscalerCollection.form_list(
                config["azureVpnSites"] if "azureVpnSites" in config else [],
                AzureVirtualHubConfigurationVirtualHubsAzureVpnSites,
            )
            if "zsLocation" in config:
                if isinstance(config["zsLocation"], common.CommonBlocks):
                    self.zs_location = config["zsLocation"]
                elif config["zsLocation"] is not None:
                    self.zs_location = common.CommonBlocks(config["zsLocation"])
                else:
                    self.zs_location = None
            else:
                self.zs_location = None
            self.zs_ip_address = config["zsIpAddress"] if "zsIpAddress" in config else None
            self.tunnel_configuration_status = (
                config["tunnelConfigurationStatus"] if "tunnelConfigurationStatus" in config else None
            )
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
        else:
            self.id = None
            self.resource_group_name = None
            self.virtual_wan = None
            self.azure_region = None
            self.vpn_gateway = None
            self.azure_hub_name = None
            self.hub_status = None
            self.azure_vpn_sites = []
            self.zs_location = None
            self.zs_ip_address = None
            self.tunnel_configuration_status = None
            self.last_modified_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "resourceGroupName": self.resource_group_name,
            "virtualWan": self.virtual_wan,
            "azureRegion": self.azure_region,
            "vpnGateway": self.vpn_gateway,
            "azureHubName": self.azure_hub_name,
            "hubStatus": self.hub_status,
            "azureVpnSites": [item.request_format() for item in (self.azure_vpn_sites or [])],
            "zsLocation": self.zs_location,
            "zsIpAddress": self.zs_ip_address,
            "tunnelConfigurationStatus": self.tunnel_configuration_status,
            "lastModifiedTime": self.last_modified_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AzureVirtualHubAzureVpnSites(ZscalerObject):
    """
    A class representing a AzureVirtualHubAzureVpnSites object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.connection_status = config["connectionStatus"] if "connectionStatus" in config else None
        else:
            self.id = None
            self.name = None
            self.ip_address = None
            self.connection_status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "ipAddress": self.ip_address,
            "connectionStatus": self.connection_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AzureVirtualHubConfigurationVirtualHubsAzureVpnSites(ZscalerObject):
    """
    A class representing a AzureVirtualHubConfigurationVirtualHubsAzureVpnSites object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.connection_status = config["connectionStatus"] if "connectionStatus" in config else None
        else:
            self.id = None
            self.name = None
            self.ip_address = None
            self.connection_status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "ipAddress": self.ip_address,
            "connectionStatus": self.connection_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
