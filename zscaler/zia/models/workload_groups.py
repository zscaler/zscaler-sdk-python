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
from zscaler.zia.models import common as common


class WorkloadGroups(ZscalerObject):
    """
    A class for WorkloadGroup objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.expression = config["expression"] if "expression" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None

            if "expressionJson" in config:
                if isinstance(config["expressionJson"], ExpressionJson):
                    self.expression_json = config["expressionJson"]
                elif config["expressionJson"] is not None:
                    self.expression_json = ExpressionJson(config["expressionJson"])
                else:
                    self.expression_json = None
            else:
                self.expression_json = None

            if "lastModifiedBy" in config:
                if isinstance(config["lastModifiedBy"], common.CommonBlocks):
                    self.last_modified_by = config["lastModifiedBy"]
                elif config["lastModifiedBy"] is not None:
                    self.last_modified_by = common.CommonBlocks(config["lastModifiedBy"])
                else:
                    self.last_modified_by = None
            else:
                self.last_modified_by = None
        else:
            self.id = None
            self.name = None
            self.description = None
            self.expression = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.expression_json = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "expression": self.expression,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "expressionJson": self.expression_json
        }


class ExpressionJson(ZscalerObject):
    """
    A class for ExpressionJson objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.tag_type = config["tagType"] if "tagType" in config else None
            self.operator = config["operator"] if "operator" in config else None

            self.expression_containers = ZscalerCollection.form_list(
                config["expressionContainers"] if "expressionContainers" in config else [], ExpressionContainers
            )

        else:
            self.tag_type = None
            self.operator = None
            self.tag_container = None
            self.expression_containers = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "tagType": self.tag_type,
            "operator": self.operator,
            "expressionContainers": self.expression_containers
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ExpressionContainers(ZscalerObject):
    """
    A class for ExpressionContainers objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.tag_type = config["tagType"] if "tagType" in config else None
            self.operator = config["operator"] if "operator" in config else None

            if "tagContainer" in config:
                if isinstance(config["tagContainer"], TagContainer):
                    self.tag_container = config["tagContainer"]
                elif config["tagContainer"] is not None:
                    self.tag_container = TagContainer(config["tagContainer"])
                else:
                    self.tag_container = None
            else:
                self.tag_container = None

        else:
            self.tag_type = None
            self.operator = None
            self.tag_container = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "tagType": self.tag_type,
            "operator": self.operator,
            "tagContainer": self.tag_container
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TagContainer(ZscalerObject):
    """
    A class for TagContainer objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.operator = config["operator"] if "operator" in config else None
            self.tags = ZscalerCollection.form_list(
                config["tags"] if "tags" in config else [], Tags
            )

        else:
            self.operator = None
            self.tags = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "operator": self.operator,
            "tags": self.tags,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Tags(ZscalerObject):
    """
    A class for Tags objects.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.key = config["key"] if "key" in config else None
            self.value = config["value"] if "value" in config else None

        else:
            self.key = None
            self.value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "key": self.key,
            "value": self.value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
