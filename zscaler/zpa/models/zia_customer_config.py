# flake8: noqa
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
from zscaler.zia.models import common


class ZIACustomerConfig(ZscalerObject):
    """
    A class for ZIA Customer Config objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ZIA Customer Config model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.zia_cloud_domain = config["ziaCloudDomain"] \
                if "ziaCloudDomain" in config else None
            self.zia_cloud_service_api_key = config["ziaCloudServiceApiKey"] \
                if "ziaCloudServiceApiKey" in config else None
            self.zia_password = config["ziaPassword"] \
                if "ziaPassword" in config else None
            self.zia_sandbox_api_token = config["ziaSandboxApiToken"] \
                if "ziaSandboxApiToken" in config else None
            self.zia_username = config["ziaUsername"] \
                if "ziaUsername" in config else None
        else:
            self.zia_cloud_domain = None
            self.zia_cloud_service_api_key = None
            self.zia_password = None
            self.zia_sandbox_api_token = None
            self.zia_username = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ziaCloudDomain": self.zia_cloud_domain,
            "ziaCloudServiceApiKey": self.zia_cloud_service_api_key,
            "ziaPassword": self.zia_password,
            "ziaSandboxApiToken": self.zia_sandbox_api_token,
            "ziaUsername": self.zia_username
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SessionTerminationOnReauth(ZscalerObject):
    """
    A class for Session Termination On Reauth objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Session Termination On Reauth model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.session_termination_on_reauth = config["sessionTerminationOnReauth"] \
                if "sessionTerminationOnReauth" in config else None
            self.allow_disable_session_termination_on_reauth = config["allowDisableSessionTerminationOnReauth"] \
                if "allowDisableSessionTerminationOnReauth" in config else None

        else:
            self.session_termination_on_reauth = None
            self.allow_disable_session_termination_on_reauth = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "sessionTerminationOnReauth": self.session_termination_on_reauth,
            "allowDisableSessionTerminationOnReauth": self.allow_disable_session_termination_on_reauth,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
