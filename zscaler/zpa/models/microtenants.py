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
    def __init__(self, config=None):
        """
        Initialize the MicrotenantSearch model based on API response.

        Args:
            config (dict): A dictionary representing the microtenant search configuration.
        """
        super().__init__(config)

        self.filter_by = []
        if config and "filterBy" in config:
            for item in config["filterBy"]:
                filter_obj = {
                    "commaSepValues": item["commaSepValues"]\
                        if "commaSepValues" in item else None,
                    "filterName": item["filterName"]\
                        if "filterName" in item else None,
                    "operator": item["operator"]\
                        if "operator" in item else None,
                    "values": item["values"]\
                        if "values" in item else None
                }
                self.filter_by.append(filter_obj)

        self.page_by = {
            "page": config["pageBy"]["page"]\
                if config and "pageBy" in config and "page" in config["pageBy"] else None,
            "pageSize": config["pageBy"]["pageSize"]\
                if config and "pageBy" in config and "pageSize" in config["pageBy"] else None,
            "validPage": config["pageBy"]["validPage"]\
                if config and "validPage" in config["pageBy"] else 0,
            "validPageSize": config["pageBy"]["validPageSize"]\
                if config and "validPageSize" in config["pageBy"] else 0
        } if config and "pageBy" in config else None

        self.sort_by = {
            "sortName": config["sortBy"]["sortName"]\
                if config and "sortBy" in config and "sortName" in config["sortBy"] else None,
            "sortOrder": config["sortBy"]["sortOrder"]\
                if config and "sortBy" in config and "sortOrder" in config["sortBy"] else None
        } if config and "sortBy" in config else None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {}

        if self.filter_by:
            current_obj_format["filterBy"] = [
                {
                    "commaSepValues": item["commaSepValues"],
                    "filterName": item["filterName"],
                    "operator": item["operator"],
                    "values": item["values"]
                } for item in self.filter_by if item
            ]

        if self.page_by:
            current_obj_format["pageBy"] = {
                "page": self.page_by["page"],
                "pageSize": self.page_by["pageSize"],
                "validPage": self.page_by["validPage"],
                "validPageSize": self.page_by["validPageSize"]
            }

        if self.sort_by:
            current_obj_format["sortBy"] = {
                "sortName": self.sort_by["sortName"],
                "sortOrder": self.sort_by["sortOrder"]
            }

        parent_req_format.update(current_obj_format)
        return parent_req_format
