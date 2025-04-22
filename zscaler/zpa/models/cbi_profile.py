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
    A class representing a Cloud Browser Isolation Profile object.
    """

    def __init__(self, config=None):
        """
        Initialize the CBIProfile model based on API response.

        Args:
            config (dict): A dictionary representing the cloud browser isolation profile.
        """
        super().__init__(config)
        self.id = config["id"] if config and "id" in config else None
        self.name = config["name"] if config and "name" in config else None
        self.description = config["description"] if config and "description" in config else None
        self.is_default = config["isDefault"] if config and "isDefault" in config else False
        self.banner_id = config["bannerId"] if config and "bannerId" in config else None

        # Lists for certificates and region IDs
        self.certificate_ids = ZscalerCollection.form_list(
            config["certificateIds"] if config and "certificateIds" in config else [], str
        )
        self.region_ids = ZscalerCollection.form_list(config["regionIds"] if config and "regionIds" in config else [], str)

        # Handling the banner as an object (for PUT requests)
        self.banner = {
            "id": config["banner"]["id"] if config and "banner" in config and "id" in config["banner"] else None,
            "name": config["banner"]["name"] if config and "banner" in config and "name" in config["banner"] else None,
        }

        # Certificates as objects
        self.certificates = []
        if config and "certificates" in config:
            for cert in config["certificates"]:
                if "id" in cert and "name" in cert:
                    self.certificates.append({"id": cert["id"], "name": cert["name"]})

        # Regions as objects
        self.regions = []
        if config and "regions" in config:
            for region in config["regions"]:
                if "id" in region and "name" in region:
                    self.regions.append({"id": region["id"], "name": region["name"]})

        # Security controls
        security_controls = config["securityControls"] if config and "securityControls" in config else {}
        self.security_controls = {
            "documentViewer": security_controls["documentViewer"] if "documentViewer" in security_controls else False,
            "allowPrinting": security_controls["allowPrinting"] if "allowPrinting" in security_controls else True,
            "watermark": {
                "enabled": (
                    security_controls["watermark"]["enabled"]
                    if "watermark" in security_controls and "enabled" in security_controls["watermark"]
                    else False
                ),
                "showUserId": (
                    security_controls["watermark"]["showUserId"]
                    if "watermark" in security_controls and "showUserId" in security_controls["watermark"]
                    else False
                ),
                "showTimestamp": (
                    security_controls["watermark"]["showTimestamp"]
                    if "watermark" in security_controls and "showTimestamp" in security_controls["watermark"]
                    else False
                ),
                "showMessage": (
                    security_controls["watermark"]["showMessage"]
                    if "watermark" in security_controls and "showMessage" in security_controls["watermark"]
                    else False
                ),
                "message": (
                    security_controls["watermark"]["message"]
                    if "watermark" in security_controls and "message" in security_controls["watermark"]
                    else None
                ),
            },
            "flattenedPdf": security_controls["flattenedPdf"] if "flattenedPdf" in security_controls else False,
            "uploadDownload": security_controls["uploadDownload"] if "uploadDownload" in security_controls else "all",
            "restrictKeystrokes": (
                security_controls["restrictKeystrokes"] if "restrictKeystrokes" in security_controls else False
            ),
            "copyPaste": security_controls["copyPaste"] if "copyPaste" in security_controls else "all",
            "localRender": security_controls["localRender"] if "localRender" in security_controls else True,
            "deepLink": {
                "enabled": (
                    security_controls["deepLink"]["enabled"]
                    if "deepLink" in security_controls and "enabled" in security_controls["deepLink"]
                    else False
                ),
                "applications": ZscalerCollection.form_list(
                    (
                        security_controls["deepLink"]["applications"]
                        if "deepLink" in security_controls and "applications" in security_controls["deepLink"]
                        else []
                    ),
                    str,
                ),
            },
        }

        # User experience attributes
        user_experience = config["userExperience"] if config and "userExperience" in config else {}
        self.user_experience = {
            "sessionPersistence": user_experience["sessionPersistence"] if "sessionPersistence" in user_experience else False,
            "browserInBrowser": user_experience["browserInBrowser"] if "browserInBrowser" in user_experience else True,
            "persistIsolationBar": (
                user_experience["persistIsolationBar"] if "persistIsolationBar" in user_experience else False
            ),
            "translate": user_experience["translate"] if "translate" in user_experience else False,
            "forwardToZia": {
                "enabled": (
                    user_experience["forwardToZia"]["enabled"]
                    if "forwardToZia" in user_experience and "enabled" in user_experience["forwardToZia"]
                    else False
                ),
                "organizationId": (
                    user_experience["forwardToZia"]["organizationId"]
                    if "forwardToZia" in user_experience and "organizationId" in user_experience["forwardToZia"]
                    else None
                ),
                "cloudName": (
                    user_experience["forwardToZia"]["cloudName"]
                    if "forwardToZia" in user_experience and "cloudName" in user_experience["forwardToZia"]
                    else None
                ),
                "pacFileUrl": (
                    user_experience["forwardToZia"]["pacFileUrl"]
                    if "forwardToZia" in user_experience and "pacFileUrl" in user_experience["forwardToZia"]
                    else None
                ),
            },
        }

        # Debug mode
        debug_mode = config["debugMode"] if config and "debugMode" in config else {}
        self.debug_mode = {
            "allowed": debug_mode["allowed"] if "allowed" in debug_mode else False,
            "filePassword": debug_mode["filePassword"] if "filePassword" in debug_mode else None,
        }

    def request_format(self):
        """
        Prepare the object in a format suitable for sending as a request payload.

        Returns:
            dict: A dictionary representing the CBI profile for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "isDefault": self.is_default,
            "bannerId": self.banner_id,
            "certificateIds": self.certificate_ids,
            "regionIds": self.region_ids,
            "banner": self.banner,  # Use banner as an object
            "certificates": self.certificates,  # List of certificate objects
            "regions": self.regions,  # List of region objects
            "securityControls": {
                "documentViewer": self.security_controls["documentViewer"],
                "allowPrinting": self.security_controls["allowPrinting"],
                "watermark": {
                    "enabled": self.security_controls["watermark"]["enabled"],
                    "showUserId": self.security_controls["watermark"]["showUserId"],
                    "showTimestamp": self.security_controls["watermark"]["showTimestamp"],
                    "showMessage": self.security_controls["watermark"]["showMessage"],
                    "message": self.security_controls["watermark"]["message"],
                },
                "deepLink": {
                    "enabled": self.security_controls["deepLink"]["enabled"],
                    "applications": self.security_controls["deepLink"]["applications"],
                },
                "flattenedPdf": self.security_controls["flattenedPdf"],
                "uploadDownload": self.security_controls["uploadDownload"],
                "restrictKeystrokes": self.security_controls["restrictKeystrokes"],
                "copyPaste": self.security_controls["copyPaste"],
                "localRender": self.security_controls["localRender"],
            },
            "userExperience": {
                "sessionPersistence": self.user_experience["sessionPersistence"],
                "browserInBrowser": self.user_experience["browserInBrowser"],
                "persistIsolationBar": self.user_experience["persistIsolationBar"],
                "translate": self.user_experience["translate"],
                "forwardToZia": {
                    "enabled": self.user_experience["forwardToZia"]["enabled"],
                    "organizationId": self.user_experience["forwardToZia"]["organizationId"],
                    "cloudName": self.user_experience["forwardToZia"]["cloudName"],
                    "pacFileUrl": self.user_experience["forwardToZia"]["pacFileUrl"],
                },
            },
            "debugMode": {"allowed": self.debug_mode["allowed"], "filePassword": self.debug_mode["filePassword"]},
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
