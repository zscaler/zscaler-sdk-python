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


class CBIProfile(ZscalerObject):
    """
    A class for CBIProfile objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the CBIProfile model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.banner_id = config["bannerId"] \
                if "bannerId" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.cbi_url = config["cbiUrl"] \
                if "cbiUrl" in config else None
            self.is_default = config["isDefault"] \
                if "isDefault" in config else None

            self.region_ids = ZscalerCollection.form_list(config["regionIds"] if "regionIds" in config else [], str)

            self.certificate_ids = ZscalerCollection.form_list(
                config["certificateIds"] if "certificateIds" in config else [],
                str
            )

            self.certificates = ZscalerCollection.form_list(
                config["certificates"] if "certificates" in config else [],
                Certificates
            )

            self.regions = ZscalerCollection.form_list(config["regions"] if "regions" in config else [], Regions)

            if "banner" in config:
                if isinstance(config["banner"], Banner):
                    self.banner = config["banner"]
                elif config["banner"] is not None:
                    self.banner = Banner(config["banner"])
                else:
                    self.banner = None
            else:
                self.banner = None

            if "debugMode" in config:
                if isinstance(config["debugMode"], DebugMode):
                    self.debug_mode = config["debugMode"]
                elif config["debugMode"] is not None:
                    self.debug_mode = DebugMode(config["debugMode"])
                else:
                    self.debug_mode = None
            else:
                self.debug_mode = None

            if "userExperience" in config:
                if isinstance(config["userExperience"], UserExperience):
                    self.user_experience = config["userExperience"]
                elif config["userExperience"] is not None:
                    self.user_experience = UserExperience(config["userExperience"])
                else:
                    self.user_experience = None
            else:
                self.user_experience = None

            if "securityControls" in config:
                if isinstance(config["securityControls"], SecurityControls):
                    self.security_controls = config["securityControls"]
                elif config["securityControls"] is not None:
                    self.security_controls = SecurityControls(config["securityControls"])
                else:
                    self.security_controls = None
            else:
                self.security_controls = None
        else:
            self.id = None
            self.banner_id = None
            self.banner = None
            self.name = None
            self.description = None
            self.certificates = None
            self.regions = None
            self.debug_mode = None
            self.user_experience = None
            self.security_controls = None
            self.cbi_url = None
            self.is_default = None
            self.region_ids = []
            self.certificate_ids = []

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "bannerId": self.banner_id,
            "banner": self.banner,
            "cbiUrl": self.cbi_url,
            "certificates": self.certificates,
            "regions": self.regions,
            "isDefault": self.is_default,
            "certificateIds": self.certificate_ids,
            "regionIds": self.region_ids,
            "debugMode": self.debug_mode,
            "userExperience": self.user_experience,
            "securityControls": self.security_controls,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DebugMode(ZscalerObject):
    """
    A class for DebugMode objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the DebugMode model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.allowed = config["allowed"] \
                if "allowed" in config else None
            self.file_password = config["filePassword"] \
                if "filePassword" in config else None

        else:
            self.allowed = None
            self.file_password = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "allowed": self.allowed,
            "filePassword": self.file_password,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class UserExperience(ZscalerObject):
    """
    A class for UserExperience objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the UserExperience model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.browser_in_browser = config["browserInBrowser"] \
                if "browserInBrowser" in config else None
            self.session_persistence = config["sessionPersistence"] \
                if "sessionPersistence" in config else None
            self.persist_isolation_bar = config["persistIsolationBar"] \
                if "persistIsolationBar" in config else None
            self.translate = config["translate"] \
                if "translate" in config else None
            self.zgpu = config["zgpu"] \
                if "zgpu" in config else None

            if "forwardToZia" in config:
                if isinstance(config["forwardToZia"], ForwardToZia):
                    self.forward_to_zia = config["forwardToZia"]
                elif config["forwardToZia"] is not None:
                    self.forward_to_zia = ForwardToZia(config["forwardToZia"])
                else:
                    self.forward_to_zia = None
            else:
                self.forward_to_zia = None
        else:
            self.browser_in_browser = None
            self.session_persistence = None
            self.persist_isolation_bar = None
            self.translate = None
            self.forward_to_zia = None
            self.zgpu = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "browserInBrowser": self.browser_in_browser,
            "sessionPersistence": self.session_persistence,
            "persistIsolationBar": self.persist_isolation_bar,
            "translate": self.translate,
            "zgpu": self.zgpu,
            "forwardToZia": self.forward_to_zia,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ForwardToZia(ZscalerObject):
    """
    A class for ForwardToZia objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the ForwardToZia model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.cloud_name = config["cloudName"] \
                if "cloudName" in config else None
            self.pac_file_url = config["pacFileUrl"] \
                if "pacFileUrl" in config else None
            self.organization_id = config["organizationId"] \
                if "organizationId" in config else None

        else:
            self.enabled = None
            self.cloud_name = None
            self.pac_file_url = None
            self.organization_id = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "enabled": self.enabled,
            "cloudName": self.cloud_name,
            "pacFileUrl": self.pac_file_url,
            "organizationId": self.organization_id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SecurityControls(ZscalerObject):
    """
    A class for SecurityControls objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the SecurityControls model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.copy_paste = config["copyPaste"] \
                if "copyPaste" in config else None
            self.upload_download = config["uploadDownload"] \
                if "uploadDownload" in config else None
            self.document_viewer = config["documentViewer"] \
                if "documentViewer" in config else None
            self.local_render = config["localRender"] \
                if "localRender" in config else None
            self.allow_printing = config["allowPrinting"] \
                if "allowPrinting" in config else None
            self.restrict_keystrokes = config["restrictKeystrokes"] \
                if "restrictKeystrokes" in config else None
            self.camera_and_mic = config["cameraAndMic"] \
                if "cameraAndMic" in config else None
            self.flattened_pdf = config["flattenedPdf"] \
                if "flattenedPdf" in config else None

            if "deepLink" in config:
                if isinstance(config["deepLink"], DeepLink):
                    self.deep_link = config["deepLink"]
                elif config["deepLink"] is not None:
                    self.deep_link = DeepLink(config["deepLink"])
                else:
                    self.deep_link = None
            else:
                self.deep_link = None

            if "watermark" in config:
                if isinstance(config["watermark"], Watermark):
                    self.watermark = config["watermark"]
                elif config["watermark"] is not None:
                    self.watermark = Watermark(config["watermark"])
                else:
                    self.watermark = None
            else:
                self.watermark = None

        else:
            self.copy_paste = None
            self.upload_download = None
            self.document_viewer = None
            self.local_render = None
            self.allow_printing = None
            self.restrict_keystrokes = None
            self.camera_and_mic = None
            self.deep_link = None
            self.watermark = None
            self.flattened_pdf = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "copyPaste": self.copy_paste,
            "uploadDownload": self.upload_download,
            "documentViewer": self.document_viewer,
            "localRender": self.local_render,
            "allowPrinting": self.allow_printing,
            "restrictKeystrokes": self.restrict_keystrokes,
            "cameraAndMic": self.camera_and_mic,
            "flattenedPdf": self.flattened_pdf,
            "deepLink": self.deep_link,
            "watermark": self.watermark,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class DeepLink(ZscalerObject):
    """
    A class for DeepLink objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the DeepLink model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.applications = ZscalerCollection.form_list(
                config["applications"] if "applications" in config else [],
                str
            )

        else:
            self.enabled = None
            self.applications = []

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "enabled": self.enabled,
            "applications": self.applications,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Watermark(ZscalerObject):
    """
    A class for Watermark objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the Watermark model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.show_user_id = config["showUserId"] \
                if "showUserId" in config else None
            self.show_timestamp = config["showTimestamp"] \
                if "showTimestamp" in config else None
            self.show_message = config["showMessage"] \
                if "showMessage" in config else None
            self.message = config["message"] \
                if "message" in config else None

        else:
            self.enabled = None
            self.show_user_id = None
            self.show_timestamp = None
            self.show_message = None
            self.message = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "enabled": self.enabled,
            "showUserId": self.show_user_id,
            "showTimestamp": self.show_timestamp,
            "showMessage": self.show_message,
            "message": self.message,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Certificates(ZscalerObject):
    """
    A class for Certificates objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the Certificates model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.enabled = config["enabled"] \
                if "enabled" in config else None
            self.is_default = config["isDefault"] \
                if "isDefault" in config else None

        else:
            self.id = None
            self.name = None
            self.enabled = None
            self.is_default = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "enabled": self.enabled,
            "isDefault": self.is_default,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Regions(ZscalerObject):
    """
    A class for Regions objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the Regions model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] \
                if "id" in config else None
            self.name = config["name"] \
                if "name" in config else None

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


class Banner(ZscalerObject):
    """
    A class for Banner objects.
    Handles common block attributes shared across multiple resources
    """

    def __init__(self, config=None):
        """
        Initialize the Banner model based on API response.

        Args:
            config (dict): A dictionary representing the response.
        """
        super().__init__(config)
        if config:
            self.id = config["id"] \
                if "id" in config else None

        else:
            self.id = None

    def request_format(self):
        """
        Returns the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
