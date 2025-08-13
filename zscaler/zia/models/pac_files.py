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


class PacFiles(ZscalerObject):
    """
    A class for Pac File objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Pac Files model based on API response.

        Args:
            config (dict): A dictionary representing the Pac Files configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.domain = config["domain"] if "domain" in config else None
            self.pac_url = config["pacUrl"] if "pacUrl" in config else None
            self.pac_content = config["pacContent"] if "pacContent" in config else None
            self.editable = config["editable"] if "editable" in config else None
            self.pac_sub_url = config["pacSubURL"] if "pacSubURL" in config else None
            self.pac_url_obfuscated = config["pacUrlObfuscated"] if "pacUrlObfuscated" in config else None
            self.pac_verification_status = config["pacVerificationStatus"] if "pacVerificationStatus" in config else None
            self.pac_version_status = config["pacVersionStatus"] if "pacVersionStatus" in config else None
            self.pac_version = config["pacVersion"] if "pacVersion" in config else None
            self.pac_commit_message = config["pacCommitMessage"] if "pacCommitMessage" in config else None
            self.total_hits = config["totalHits"] if "totalHits" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.create_time = config["createTime"] if "createTime" in config else None

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
            # Initialize with default None or 0 values
            self.id = None
            self.name = None
            self.description = None
            self.domain = None
            self.pac_url = None
            self.pac_content = None
            self.editable = None
            self.pac_sub_url = None
            self.pac_url_obfuscated = None
            self.pac_verification_status = None
            self.pac_version_status = None
            self.pac_version = None
            self.pac_commit_message = None
            self.total_hits = None
            self.last_modified_time = None
            self.last_modified_by = None
            self.create_time = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "domain": self.domain,
            "pacUrl": self.pac_url,
            "pacContent": self.pac_content,
            "editable": self.editable,
            "pacSubURL": self.pac_sub_url,
            "pacUrlObfuscated": self.pac_url_obfuscated,
            "pacVerificationStatus": self.pac_verification_status,
            "pacVersionStatus": self.pac_version_status,
            "pacVersion": self.pac_version,
            "pacCommitMessage": self.pac_commit_message,
            "totalHits": self.total_hits,
            "lastModifiedTime": self.last_modified_time,
            "lastModifiedBy": self.last_modified_by,
            "createTime": self.create_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PacFileValidationResponse(ZscalerObject):
    """
    A class for Pac File Validation Response objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Pac File Validation Response model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.success = config["success"] \
                if "success" in config else None
            self.message = config["message"] \
                if "message" in config else None
            self.severity = config["severity"] \
                if "severity" in config else None
            self.warning_count = config["warningCount"] \
                if "warningCount" in config else None
            self.error_count = config["errorCount"] \
                if "errorCount" in config else None

            self.messages = ZscalerCollection.form_list(
                config["messages"] if "messages" in config else [], Messages
            )
        else:
            self.success = None
            self.message = None
            self.severity = None
            self.messages = []
            self.warning_count = None
            self.error_count = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "success": self.success,
            "message": self.message,
            "severity": self.severity,
            "messages": self.messages,
            "warningCount": self.warning_count,
            "errorCount": self.error_count
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Messages(ZscalerObject):
    """
    A class for Messages objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Messages model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.severity = config["severity"] \
                if "severity" in config else None
            self.end_line = config["endLine"] \
                if "endLine" in config else None
            self.end_column = config["endColumn"] \
                if "endColumn" in config else None
            self.line = config["line"] \
                if "line" in config else None
            self.column = config["column"] \
                if "column" in config else None
            self.message = config["message"] \
                if "message" in config else None
            self.fatal = config["fatal"] \
                if "fatal" in config else None
        else:
            self.severity = None
            self.end_line = None
            self.end_column = None
            self.line = None
            self.column = None
            self.message = None
            self.fatal = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "severity": self.severity,
            "endLine": self.end_line,
            "endColumn": self.end_column,
            "line": self.line,
            "column": self.column,
            "message": self.message,
            "fatal": self.fatal
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
