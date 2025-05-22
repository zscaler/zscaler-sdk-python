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


class CommonIDName(ZscalerObject):
    """
    A class for CommonIDName objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the CommonIDName model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None

        else:
            self.id = None
            self.name = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CommonNameReason(ZscalerObject):
    """
    A class for CommonNameReason objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the CommonNameReason model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.name = config["name"] if "name" in config else None
            self.reason = config["reason"] if "reason" in config else None
        else:
            self.id = None
            self.reason = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "reason": self.reason,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ExtranetDTO(ZscalerObject):
    """
    A class for ExtranetDTO objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the ExtranetDTO model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.zia_er_name = config["ziaErName"] if "ziaErName" in config else None
            self.zia_er_id = config["ziaErId"] if "ziaErId" in config else None

            self.location_dto = ZscalerCollection.form_list(
                config["locationDTO"] if "locationDTO" in config else [], CommonIDName
            )

            self.location_group_dto = ZscalerCollection.form_list(
                config["locationGroupDTO"] if "locationGroupDTO" in config else [], LocationGroupDTO
            )

        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.zia_er_name = None
            self.zia_er_id = None
            self.location_dto = []

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "modifiedTime": self.modified_time,
            "creationTime": self.creation_time,
            "modifiedBy": self.modified_by,
            "ziaErName": self.zia_er_name,
            "ziaErId": self.zia_er_id,
            "locationDTO": self.location_dto,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class LocationGroupDTO(ZscalerObject):
    """
    A class for LocationGroupDTO objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the LocationGroupDTO model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None

            self.zia_locations = ZscalerCollection.form_list(
                config["ziaLocations"] if "ziaLocations" in config else [], CommonIDName
            )

        else:
            self.id = None
            self.name = None
            self.zia_locations = []

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "ziaLocations": self.zia_locations,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class InspectionControlException(ZscalerObject):
    """
    A class for InspectionControlException objects.
    """

    def __init__(self, config=None):
        """
        Initialize the InspectionControlException model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.domains = ZscalerCollection.form_list(config["domains"] if "domains" in config else [], Domains)

            self.paths = ZscalerCollection.form_list(config["paths"] if "paths" in config else [], Paths)

            self.variables = ZscalerCollection.form_list(config["variables"] if "variables" in config else [], Variables)

            self.version = config["version"] if "version" in config else None

        else:
            self.domains = None
            self.paths = None
            self.variables = None
            self.version = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "domains": self.domains,
            "paths": self.paths,
            "variables": self.variables,
            "version": self.version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Domains(ZscalerObject):
    """
    A class for Domains objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Domains model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.match_type = config["matchType"] if "matchType" in config else None
            self.var_value = config["varValue"] if "varValue" in config else None
        else:
            self.match_type = None
            self.var_value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "matchType": self.match_type,
            "varValue": self.var_value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Paths(ZscalerObject):
    """
    A class for Paths objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Paths model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.match_type = config["matchType"] if "matchType" in config else None
            self.var_value = config["varValue"] if "varValue" in config else None
        else:
            self.match_type = None
            self.var_value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "matchType": self.match_type,
            "varValue": self.var_value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Variables(ZscalerObject):
    """
    A class for Variables objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Variables model based on API response.

        Args:
            config (dict): A dictionary representing the Rule Labels configuration.
        """
        super().__init__(config)

        if config:
            self.match_type = config["matchType"] if "matchType" in config else None
            self.var_value = config["varValue"] if "varValue" in config else None
        else:
            self.match_type = None
            self.var_value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "matchType": self.match_type,
            "varValue": self.var_value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PrivilegedCapabilitiesResource(ZscalerObject):
    """
    A class for PrivilegedCapabilitiesResource objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the CommonIDName model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.capabilities = ZscalerCollection.form_list(config["capabilities"] if "capabilities" in config else [], str)

        else:
            self.capabilities = None
            self.microtenant_id = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "microtenantId": self.microtenant_id,
            "capabilities": self.capabilities,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
