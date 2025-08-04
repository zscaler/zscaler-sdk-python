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
from zscaler.zidentity.models import common


class APIClients(ZscalerObject):
    """
    A class for API Clients objects.
    """

    def __init__(self, config=None):
        """
        Initialize the API Clients model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.results_total = config["results_total"] \
                if "results_total" in config else None
            self.page_offset = config["pageOffset"] \
                if "pageOffset" in config else None
            self.page_size = config["pageSize"] \
                if "pageSize" in config else None
            self.next_link = config["next_link"] \
                if "next_link" in config else None
            self.prev_link = config["prev_link"] \
                if "prev_link" in config else None

            self.records = ZscalerCollection.form_list(
                config["records"] if "records" in config else [], APIClientRecords
            )

        else:
            self.results_total = None
            self.page_offset = None
            self.page_size = None
            self.next_link = None
            self.prev_link = None
            self.records = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "results_total": self.results_total,
            "pageOffset": self.page_offset,
            "pageSize": self.page_size,
            "next_link": self.next_link,
            "prev_link": self.prev_link,
            "records": self.records
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class APIClientRecords(ZscalerObject):
    """
    A class for Apiclientsecrets objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Apiclientsecrets model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.name = config["name"] \
                if "name" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.status = config["status"] \
                if "status" in config else None
            self.access_token_life_time = config["accessTokenLifeTime"] \
                if "accessTokenLifeTime" in config else None
            self.client_authentication = config["clientAuthentication"] \
                if "clientAuthentication" in config else None
            self.id = config["id"] \
                if "id" in config else None

            self.client_resources = ZscalerCollection.form_list(
                config["clientResources"] if "clientResources" in config else [], ClientResources
            )
            if "clientAuthentication" in config:
                if isinstance(config["clientAuthentication"], ClientAuthentication):
                    self.client_authentication = config["clientAuthentication"]
                elif config["clientAuthentication"] is not None:
                    self.client_authentication = ClientAuthentication(config["clientAuthentication"])
                else:
                    self.client_authentication = None

            else:
                self.client_authentication = None
        else:
            self.name = None
            self.description = None
            self.status = None
            self.access_token_life_time = None
            self.client_authentication = None
            self.client_resources = []
            self.id = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "accessTokenLifeTime": self.access_token_life_time,
            "clientAuthentication": self.client_authentication,
            "clientResources": self.client_resources,
            "id": self.id
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ClientAuthentication(ZscalerObject):
    """
    A class for Client Authentication objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Client Authentication model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.client_jw_ks_url = config["clientJWKsUrl"] \
                if "clientJWKsUrl" in config else None

            self.auth_type = config["authType"] \
                if "authType" in config else None

            self.public_keys = ZscalerCollection.form_list(
                config["publicKeys"] if "publicKeys" in config else [], PublicKeys
            )

            self.client_certificates = ZscalerCollection.form_list(
                config["clientCertificates"] if "clientCertificates" in config else [], ClientCertificates
            )
        else:
            self.client_jw_ks_url = None
            self.auth_type = None
            self.public_keys = []
            self.client_certificates = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "clientJWKsUrl": self.client_jw_ks_url,
            "publicKeys": self.public_keys,
            "clientCertificates": self.client_certificates,
            "authType": self.auth_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ClientCertificates(ZscalerObject):
    """
    A class for Client Certificates objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Client Certificates model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.cert_content = config["certContent"] \
                if "certContent" in config else None
        else:
            self.cert_content = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "certContent": self.cert_content,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ClientResources(ZscalerObject):
    """
    A class for Client Resources objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Client Resources model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.default_api = config["defaultApi"] \
                if "defaultApi" in config else None

            self.selected_scopes = ZscalerCollection.form_list(
                config["selectedScopes"] if "selectedScopes" in config else [], common.CommonIDName
            )
        else:
            self.id = None
            self.name = None
            self.default_api = None
            self.selected_scopes = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "defaultApi": self.default_api,
            "selectedScopes": self.selected_scopes,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PublicKeys(ZscalerObject):
    """
    A class for Public Keys objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Public Keys model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.key_name = config["keyName"] \
                if "keyName" in config else None
            self.key_value = config["keyValue"] \
                if "keyValue" in config else None
        else:
            self.key_name = None
            self.key_value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "keyName": self.key_name,
            "keyValue": self.key_value,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class APIClientSecrets(ZscalerObject):
    """
    A class for Api Client Secrets objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Api Client Secrets model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.expires_at = config["expiresAt"] \
                if "expiresAt" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.created_at = config["createdAt"] \
                if "createdAt" in config else None
            self.value = config["value"] \
                if "value" in config else None
        else:
            self.expires_at = None
            self.id = None
            self.created_at = None
            self.value = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "expiresAt": self.expires_at,
            "id": self.id,
            "createdAt": self.created_at,
            "value": self.value
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
