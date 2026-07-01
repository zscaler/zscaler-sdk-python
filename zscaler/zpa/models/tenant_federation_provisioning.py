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


class TenantFederationApprovalRequest(ZscalerObject):
    """
    A class representing a TenantFederationApprovalRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.partner_notes = config["partnerNotes"] if "partnerNotes" in config else None
            self.token = config["token"] if "token" in config else None
        else:
            self.partner_notes = None
            self.token = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "partnerNotes": self.partner_notes,
            "token": self.token,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TenantFederationToken(ZscalerObject):
    """
    A class representing a TenantFederationToken object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.token = config["token"] if "token" in config else None
            self.token_expiration_epoch_seconds = (
                config["tokenExpirationEpochSeconds"] if "tokenExpirationEpochSeconds" in config else None
            )
        else:
            self.id = None
            self.token = None
            self.token_expiration_epoch_seconds = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "token": self.token,
            "tokenExpirationEpochSeconds": self.token_expiration_epoch_seconds,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TenantFederationTokenRequest(ZscalerObject):
    """
    A class representing a TenantFederationTokenRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.expiry_time_in_seconds = config["expiryTimeInSeconds"] if "expiryTimeInSeconds" in config else None
            self.notes = config["notes"] if "notes" in config else None
        else:
            self.expiry_time_in_seconds = None
            self.notes = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "expiryTimeInSeconds": self.expiry_time_in_seconds,
            "notes": self.notes,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TenantFederationProvisioning(ZscalerObject):
    """
    A class representing a TenantFederationProvisioning object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            if "partnerInfo" in config:
                if isinstance(config["partnerInfo"], PartnerInfo):
                    self.partner_info = config["partnerInfo"]
                elif config["partnerInfo"] is not None:
                    self.partner_info = PartnerInfo(config["partnerInfo"])
                else:
                    self.partner_info = None
            else:
                self.partner_info = None
            self.partner_notes = config["partnerNotes"] if "partnerNotes" in config else None
            self.success = config["success"] if "success" in config else False
            self.token_expiration_epoch_seconds = (
                config["tokenExpirationEpochSeconds"] if "tokenExpirationEpochSeconds" in config else None
            )
        else:
            self.partner_info = None
            self.partner_notes = None
            self.success = False
            self.token_expiration_epoch_seconds = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "partnerInfo": self.partner_info,
            "partnerNotes": self.partner_notes,
            "success": self.success,
            "tokenExpirationEpochSeconds": self.token_expiration_epoch_seconds,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TenantFederationTokenVerifyRequest(ZscalerObject):
    """
    A class representing a TenantFederationTokenVerifyRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.token = config["token"] if "token" in config else None
        else:
            self.token = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "token": self.token,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class TenantFederationNotesUpdate(ZscalerObject):
    """
    A class representing a TenantFederationNotesUpdate object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.notes = config["notes"] if "notes" in config else None
        else:
            self.notes = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "notes": self.notes,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PartnerInfo(ZscalerObject):
    """
    A class representing a PartnerInfo object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.approval_status = config["approvalStatus"] if "approvalStatus" in config else None
            self.federation_status = config["federationStatus"] if "federationStatus" in config else None
            self.partner_gid = config["partnerGid"] if "partnerGid" in config else None
            self.partner_name = config["partnerName"] if "partnerName" in config else None
            self.partner_scope_name = config["partnerScopeName"] if "partnerScopeName" in config else None
        else:
            self.approval_status = None
            self.federation_status = None
            self.partner_gid = None
            self.partner_name = None
            self.partner_scope_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "approvalStatus": self.approval_status,
            "federationStatus": self.federation_status,
            "partnerGid": self.partner_gid,
            "partnerName": self.partner_name,
            "partnerScopeName": self.partner_scope_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
