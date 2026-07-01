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


class OneIdentity(ZscalerObject):
    """
    A class representing a OneIdentity object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            if "iamIdpIdToIamIdMapping" in config:
                if isinstance(config["iamIdpIdToIamIdMapping"], IamIdpIdToIamIdMapping):
                    self.iam_idp_id_to_iam_id_mapping = config["iamIdpIdToIamIdMapping"]
                elif config["iamIdpIdToIamIdMapping"] is not None:
                    self.iam_idp_id_to_iam_id_mapping = IamIdpIdToIamIdMapping(config["iamIdpIdToIamIdMapping"])
                else:
                    self.iam_idp_id_to_iam_id_mapping = None
            else:
                self.iam_idp_id_to_iam_id_mapping = None
            self.id = config["id"] if "id" in config else None
            self.sequence = config["sequence"] if "sequence" in config else None
        else:
            self.iam_idp_id_to_iam_id_mapping = None
            self.id = None
            self.sequence = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iamIdpIdToIamIdMapping": self.iam_idp_id_to_iam_id_mapping,
            "id": self.id,
            "sequence": self.sequence,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class IamIdpIdToIamIdMapping(ZscalerObject):
    """
    A class representing a IamIdpIdToIamIdMapping object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.delivery_tag = config["deliveryTag"] if "deliveryTag" in config else None
            self.mappings = ZscalerCollection.form_list(config["mappings"] if "mappings" in config else [], Mapping)
            self.org_id = config["orgId"] if "orgId" in config else None
            self.sync_version = config["syncVersion"] if "syncVersion" in config else None
        else:
            self.delivery_tag = None
            self.mappings = []
            self.org_id = None
            self.sync_version = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "deliveryTag": self.delivery_tag,
            "mappings": [item.request_format() for item in (self.mappings or [])],
            "orgId": self.org_id,
            "syncVersion": self.sync_version,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Mapping(ZscalerObject):
    """
    A class representing a Mapping object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.iam_idp_id = config["iamIdpId"] if "iamIdpId" in config else None
            self.idp_id = config["idpId"] if "idpId" in config else None
            self.idp_name = config["idpName"] if "idpName" in config else None
        else:
            self.iam_idp_id = None
            self.idp_id = None
            self.idp_name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "iamIdpId": self.iam_idp_id,
            "idpId": self.idp_id,
            "idpName": self.idp_name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
