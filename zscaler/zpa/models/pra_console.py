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
from zscaler.zpa.models import application_segment_pra as application_segment_pra
from zscaler.zpa.models import pra_portal as pra_portal

class PrivilegedRemoteAccessConsole(ZscalerObject):
    """
    A class representing the Privileged Remote Access Console.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else True
            self.modified_time = config["modifiedTime"] \
                if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] \
                if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] \
                if "modifiedBy" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.microtenant_id = config["microtenantId"]\
                if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"]\
                if "microtenantName" in config else "Default"
                
            # Handling the nested PRA Application
            self.pra_application = application_segment_pra.ApplicationSegmentPRA(config["praApplication"]) \
                if "praApplication" in config else None

            # Handling the nested PRA Portals (list)
            self.pra_portals = ZscalerCollection.form_list(
                config["praPortals"], pra_portal.PrivilegedRemoteAccessPortal
            ) if "praPortals" in config else []
        else:
            self.id = None
            self.name = None
            self.enabled = True
            self.modified_time = None
            self.creation_time = None
            self.modified_by = None
            self.description = None
            self.pra_application = None
            self.microtenant_id = None
            self.microtenant_name = "Default"
            self.pra_portals = []

    def request_format(self):
        """
        Formats the PRA Console data into a dictionary suitable for API requests.
        """
        return {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
            "praApplication": self.pra_application.request_format() \
                if self.pra_application else None,
            "praPortals": [portal.request_format() for portal in self.pra_portals],
        }