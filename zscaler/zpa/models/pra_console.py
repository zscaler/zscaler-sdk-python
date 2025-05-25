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
from zscaler.zpa.models import pra_portal as pra_portal


class PrivilegedRemoteAccessConsole(ZscalerObject):
    """
    A class representing the Privileged Remote Access Console.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.enabled = config["enabled"] if "enabled" in config else True
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.description = config["description"] if "description" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else "Default"

            if "praApplication" in config:
                if isinstance(config["praApplication"], PRAApplication):
                    self.pra_application = config["praApplication"]
                elif config["praApplication"] is not None:
                    self.pra_application = PRAApplication(config["praApplication"])
                else:
                    self.pra_application = None
            else:
                self.pra_application = None

            self.pra_portals = (
                ZscalerCollection.form_list(config["praPortals"], pra_portal.PrivilegedRemoteAccessPortal)
                if "praPortals" in config
                else []
            )

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
            self.microtenant_name = None
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
            "praApplication": self.pra_application,
            "praPortals": [portal.request_format() for portal in self.pra_portals],
        }


class PRAApplication(ZscalerObject):
    """
    A class for PRAApplication objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PRAApplication model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.app_id = config["appId"] if "appId" in config else None
            self.application_port = config["applicationPort"] if "applicationPort" in config else None
            self.application_protocol = config["applicationProtocol"] if "applicationProtocol" in config else None
            self.connection_security = config["connectionSecurity"] if "connectionSecurity" in config else None
            self.creation_time = config["creationTime"] if "creationTime" in config else None
            self.description = config["description"] if "description" in config else None
            self.domain = config["domain"] if "domain" in config else None
            self.enabled = config["enabled"] if "enabled" in config else None
            self.hidden = config["hidden"] if "hidden" in config else None
            self.id = config["id"] if "id" in config else None
            self.modified_by = config["modifiedBy"] if "modifiedBy" in config else None
            self.modified_time = config["modifiedTime"] if "modifiedTime" in config else None
            self.name = config["name"] if "name" in config else None
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
        else:
            self.app_id = None
            self.application_port = None
            self.application_protocol = None
            self.connection_security = None
            self.creation_time = None
            self.description = None
            self.domain = None
            self.enabled = None
            self.hidden = None
            self.id = None
            self.modified_by = None
            self.modified_time = None
            self.name = None
            self.microtenant_id = None
            self.microtenant_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "appId": self.app_id,
            "applicationPort": self.application_port,
            "applicationProtocol": self.application_protocol,
            "connectionSecurity": self.connection_security,
            "creationTime": self.creation_time,
            "description": self.description,
            "domain": self.domain,
            "enabled": self.enabled,
            "hidden": self.hidden,
            "id": self.id,
            "modifiedBy": self.modified_by,
            "modifiedTime": self.modified_time,
            "name": self.name,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
