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


class CommonIDNameExternalID(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.is_name_l10n_tag = config["isNameL10nTag"] if "isNameL10nTag" in config else None
            self.deleted = config["deleted"] if "deleted" in config else False
            self.external_id = config["externalId"] if "externalId" in config else None
            self.association_time = config["associationTime"] if "associationTime" in config else None

            self.extensions = config if isinstance(config, dict) else {}

        else:
            self.id = None
            self.name = None
            self.is_name_l10n_tag = False
            self.deleted = False
            self.external_id = None
            self.association_time = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "isNameL10nTag": self.is_name_l10n_tag,
            "deleted": self.deleted,
            "externalId": self.external_id,
            "associationTime": self.association_time,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
