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


class Microtenant(ZscalerObject):
    def __init__(self, config=None):
        """
        Initialize the Microtenant model based on API response.

        Args:
            config (dict): A dictionary representing the microtenant configuration.
        """
        super().__init__(config)
        self.id = config["id"]\
            if config and "id" in config else None
        self.modified_time = config["modifiedTime"]\
            if config and "modifiedTime" in config else None
        self.creation_time = config["creationTime"]\
            if config and "creationTime" in config else None
        self.modified_by = config["modifiedBy"]\
            if config and "modifiedBy" in config else None
        self.name = config["name"]\
            if config and "name" in config else None
        self.description = config["description"]\
            if config and "description" in config else None
        self.enabled = config["enabled"]\
            if config and "enabled" in config else None
        self.operator = config["operator"]\
            if config and "operator" in config else None
        self.criteria_attribute = config["criteriaAttribute"]\
            if config and "criteriaAttribute" in config else None
        self.criteria_attribute_values = (
            config["criteriaAttributeValues"]\
                if config and "criteriaAttributeValues" in config else None
        )
        self.privileged_approvals_enabled = (
            config["privilegedApprovalsEnabled"]\
                if config and "privilegedApprovalsEnabled" in config else None
        )

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {}

        if self.id is not None:
            current_obj_format["id"] = self.id
        if self.modified_time is not None:
            current_obj_format["modifiedTime"] = self.modified_time
        if self.creation_time is not None:
            current_obj_format["creationTime"] = self.creation_time
        if self.modified_by is not None:
            current_obj_format["modifiedBy"] = self.modified_by
        if self.name is not None:
            current_obj_format["name"] = self.name
        if self.description is not None:
            current_obj_format["description"] = self.description
        if self.enabled is not None:
            current_obj_format["enabled"] = self.enabled
        if self.operator is not None:
            current_obj_format["operator"] = self.operator
        if self.criteria_attribute is not None:
            current_obj_format["criteriaAttribute"] = self.criteria_attribute
        if self.criteria_attribute_values is not None:
            current_obj_format["criteriaAttributeValues"] = self.criteria_attribute_values
        if self.privileged_approvals_enabled is not None:
            current_obj_format["privilegedApprovalsEnabled"] = self.privileged_approvals_enabled

        parent_req_format.update(current_obj_format)
        return parent_req_format


class MicrotenantSearch(ZscalerObject):
    """
    A class for MicrotenantSearch objects.
    """

    def __init__(self, config=None):
        """
        Initialize the MicrotenantSearch model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            
            filter_and_sort = config.get("filterAndSortDto", {})
            
            self.filter_by = ZscalerCollection.form_list(
                config["filterBy"] if "filterBy" in config else [], FilterBy
            )

            self.page_by = PageBy(filter_and_sort["pageBy"]) if "pageBy" in filter_and_sort else None
            self.sort_by = SortBy(filter_and_sort["sortBy"]) if "sortBy" in filter_and_sort else None           
            # if "pageBy" in config:
            #     if isinstance(config["pageBy"], PageBy):
            #         self.page_by = config["pageBy"]
            #     elif config["pageBy"] is not None:
            #         self.page_by = PageBy(config["pageBy"])
            #     else:
            #         self.page_by = None
            # else:
            #     self.page_by = None

            # if "sortBy" in config:
            #     if isinstance(config["sortBy"], SortBy):
            #         self.sort_by = config["pageBy"]
            #     elif config["sortBy"] is not None:
            #         self.sort_by = SortBy(config["sortBy"])
            #     else:
            #         self.sort_by = None
            # else:
            #     self.sort_by = None

        else:
            self.filter_by = []
            self.page_by = None
            self.sort_by = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "filterAndSortDto": {
                "filterBy": self.filter_by,
                "pageBy": self.page_by,
                "sortBy": self.sort_by
            }
        }
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
            self.comma_sep_values = config["commaSepValues"]\
                if "commaSepValues" in config else None
            self.filter_name = config["filterName"]\
                if "filterName" in config else None
            self.operator = config["operator"]\
                if "operator" in config else None
                
            self.values = ZscalerCollection.form_list(
                config["values"] if "values" in config else [], str
            )
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
            self.page = config["page"]\
                if "page" in config else None
            self.page_size = config["pageSize"]\
                if "pageSize" in config else None
            self.valid_page = config["validPage"]\
                if "validPage" in config else None
            self.valid_page_size = config["validPageSize"]\
                if "validPageSize" in config else None
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
            self.sort_name = config["sortName"]\
                if "sortName" in config else None
            self.sort_order = config["sortOrder"]\
                if "sortOrder" in config else None
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
