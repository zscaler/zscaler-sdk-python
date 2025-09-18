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
from zscaler.zpa.models import application_segment as application_segment


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
            self.enabled = config["enabled"] if "enabled" in config else None
        else:
            self.id = None
            self.name = None
            self.enabled = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
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


class CommonFilterSearch(ZscalerObject):
    """
    A class for CommonFilterSearch objects.
    """

    def __init__(self, config=None):
        """
        Initialize the CommonFilterSearch model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:

            filter_and_sort = config.get("filterAndSortDto", {})

            self.filter_by = ZscalerCollection.form_list(config["filterBy"] if "filterBy" in config else [], FilterBy)

            self.page_by = PageBy(filter_and_sort["pageBy"]) if "pageBy" in filter_and_sort else None
            self.sort_by = SortBy(filter_and_sort["sortBy"]) if "sortBy" in filter_and_sort else None

        else:
            self.filter_by = []
            self.page_by = None
            self.sort_by = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"filterAndSortDto": {"filterBy": self.filter_by, "pageBy": self.page_by, "sortBy": self.sort_by}}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class FilterBy(ZscalerObject):
    """
    A class for FilterBy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the FilterBy model based on API response.

        Args:
            config (dict): A dictionary representing the FilterBy configuration.
        """
        super().__init__(config)

        if config:
            self.comma_sep_values = config["commaSepValues"] if "commaSepValues" in config else None
            self.filter_name = config["filterName"] if "filterName" in config else None
            self.operator = config["operator"] if "operator" in config else None

            self.values = ZscalerCollection.form_list(config["values"] if "values" in config else [], str)
        else:
            self.comma_sep_values = None
            self.filter_name = None
            self.operator = None
            self.values = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "commaSepValues": self.comma_sep_values,
            "filterName": self.filter_name,
            "operator": self.operator,
            "values": self.values,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PageBy(ZscalerObject):
    """
    A class for PageBy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PageBy model based on API response.

        Args:
            config (dict): A dictionary representing the PageBy configuration.
        """
        super().__init__(config)

        if config:
            self.page = config["page"] if "page" in config else None
            self.page_size = config["pageSize"] if "pageSize" in config else None
            self.valid_page = config["validPage"] if "validPage" in config else None
            self.valid_page_size = config["validPageSize"] if "validPageSize" in config else None
        else:
            self.page = None
            self.page_size = None
            self.valid_page = None
            self.valid_page_size = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "page": self.page,
            "pageSize": self.page_size,
            "validPage": self.valid_page,
            "validPageSize": self.valid_page_size,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SortBy(ZscalerObject):
    """
    A class for SortBy objects.
    """

    def __init__(self, config=None):
        """
        Initialize the SortBy model based on API response.

        Args:
            config (dict): A dictionary representing the SortBy configuration.
        """
        super().__init__(config)

        if config:
            self.sort_name = config["sortName"] if "sortName" in config else None
            self.sort_order = config["sortOrder"] if "sortOrder" in config else None
        else:
            self.sort_name = None
            self.sort_order = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "sortName": self.sort_name,
            "sortOrder": self.sort_order,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DesktopPolicyMappingsDTO(ZscalerObject):
    """
    A class for DesktopPolicyMappingsDTO objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the DesktopPolicyMappingsDTO model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.image_id = config["imageId"] if "imageId" in config else None
            self.image_name = config["imageName"] if "imageName" in config else None
            self.app_segments = ZscalerCollection.form_list(
                config["appSegments"] if "appSegments" in config else [], application_segment.ApplicationSegments
            )
        else:
            self.id = None
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.image_id = None
            self.image_name = None
            self.app_segments = []

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
            "imageId": self.image_id,
            "imageName": self.image_name,
            "appSegments": [segment.as_dict() for segment in self.app_segments],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
