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


class PrivilegedRemoteAccessCredential(ZscalerObject):
    """
    A class representing the Privileged Remote Access Credential.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.description = config["description"] if "description" in config else None
            self.user_domain = config["userDomain"] if "userDomain" in config else None
            self.user_name = config["userName"] if "userName" in config else None
            self.credential_type = config["credentialType"] if "credentialType" in config else None
            self.last_credential_reset_time = (
                config["lastCredentialResetTime"] if "lastCredentialResetTime" in config else None
            )
            self.microtenant_id = config["microtenantId"] if "microtenantId" in config else None
            self.microtenant_name = config["microtenantName"] if "microtenantName" in config else None
        else:
            self.id = None
            self.name = None
            self.description = None
            self.user_domain = None
            self.user_name = None
            self.credential_type = None
            self.last_credential_reset_time = None
            self.microtenant_id = None
            self.microtenant_name = None

    def request_format(self):
        """
        Formats the credential data into a dictionary suitable for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "userDomain": self.user_domain,
            "userName": self.user_name,
            "credentialType": self.credential_type,
            "lastCredentialResetTime": self.last_credential_reset_time,
            "microtenantId": self.microtenant_id,
            "microtenantName": self.microtenant_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
