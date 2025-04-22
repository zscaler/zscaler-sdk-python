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


class ResourceReference(ZscalerObject):
    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.external_id = config["externalId"] if "externalId" in config else None
            self.extensions = config if isinstance(config, dict) else {}

        else:
            # Defaults when config is None
            self.id = None
            self.name = None
            self.external_id = None
            self.extensions = None

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {"id": self.id, "name": self.name, "externalId": self.external_id, "extensions": self.extensions}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Extensions(ZscalerObject):
    """
    A generic class to wrap dynamic extension data.
    """

    def __init__(self, config=None):
        super().__init__(config)
        # Simply store the dictionary as is
        if config and isinstance(config, dict):
            self.data = config
        else:
            self.data = {}

    def request_format(self):
        """
        Return the extension data as a dictionary.
        """
        return self.data

    def as_dict(self):
        """
        Return a dictionary representation of the extension data.
        """
        return self.data


class CommonBlocks(ZscalerObject):
    """
    A class for CommonBlocks objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the CommonBlocks model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.external_id = config["externalId"] if "externalId" in config else False
            self.extensions = config if isinstance(config, dict) else {}

        else:
            self.id = None
            self.name = None
            self.external_id = None
            self.extensions = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "externalId": self.external_id,
            "extensions": self.extensions,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


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


class CommonIDNameTag(ZscalerObject):
    """
    A class for CommonIDNameTag objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the CommonIDNameTag model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.is_name_l10n_tag = config["isNameL10nTag"] if "isNameL10nTag" in config else False
        else:
            self.id = None
            self.name = None
            self.is_name_l10n_tag = False

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {"id": self.id, "name": self.name, "isNameL10nTag": self.is_name_l10n_tag}
        parent_req_format.update(current_obj_format)
        return parent_req_format
