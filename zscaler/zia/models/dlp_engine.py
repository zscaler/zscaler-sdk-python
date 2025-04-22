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


class DLPEngine(ZscalerObject):
    """
    A class representing a DLP Engine object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.predefined_engine_name = config["predefinedEngineName"] if "predefinedEngineName" in config else None
            self.description = config["description"] if "description" in config else None
            self.engine_expression = config["engineExpression"] if "engineExpression" in config else None
            self.custom_dlp_engine = config["customDlpEngine"] if "customDlpEngine" in config else False

        else:
            self.id = None
            self.name = None
            self.predefined_engine_name = None
            self.description = None
            self.engine_expression = None
            self.custom_dlp_engine = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "predefinedEngineName": self.predefined_engine_name,
            "description": self.description,
            "engineExpression": self.engine_expression,
            "customDlpEngine": self.custom_dlp_engine,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DLPVAlidateExpression(ZscalerObject):
    """
    A class representing the response from validating a DLP Pattern.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.status = config["status"] if "status" in config else None
            self.err_msg = config["errMsg"] if "errMsg" in config else None
            self.err_parameter = config["errParameter"] if "errParameter" in config else None
            self.err_suggestion = config["errSuggestion"] if "errSuggestion" in config else None
        else:
            self.status = None
            self.err_msg = None
            self.err_parameter = None
            self.err_suggestion = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
            "errMsg": self.err_msg,
            "errParameter": self.err_parameter,
            "errSuggestion": self.err_suggestion,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
