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

from zscaler.zcc.admin_user import AdminUserAPI
from zscaler.zcc.company import CompanyInfoAPI
from zscaler.zcc.devices import DevicesAPI
from zscaler.zcc.entitlements import EntitlementAPI
from zscaler.zcc.fail_open_policy import FailOpenPolicyAPI
from zscaler.zcc.forwarding_profile import ForwardingProfileAPI
from zscaler.zcc.secrets import SecretsAPI
from zscaler.zcc.trusted_networks import TrustedNetworksAPI
from zscaler.zcc.web_policy import WebPolicyAPI
from zscaler.zcc.web_privacy import WebPrivacyAPI
from zscaler.zcc.web_app_service import WebAppServiceAPI


class ZCCService:
    """ZCC Service client, exposing various ZCC APIs."""

    def __init__(self, client):
        self._request_executor = client._request_executor

    @property
    def devices(self):
        """
        The interface object for the :ref:`ZCC devices interface <zcc-devices>`.

        """
        return DevicesAPI(self._request_executor)

    @property
    def secrets(self):
        """
        The interface object for the :ref:`ZCC secrets interface <zcc-secrets>`.

        """
        return SecretsAPI(self._request_executor)

    @property
    def admin_user(self):
        """
        The interface object for the :ref:`ZCC admin user interface <zcc-admin_user>`.

        """
        return AdminUserAPI(self._request_executor)

    @property
    def company(self):
        """
        The interface object for the :ref:`ZCC company info interface <zcc-company_info>`.

        """
        return CompanyInfoAPI(self._request_executor)

    @property
    def entitlements(self):
        """
        The interface object for the :ref:`ZCC entitlement for zdx and zpa interface <zcc-entitlements>`.

        """
        return EntitlementAPI(self._request_executor)

    @property
    def forwarding_profile(self):
        """
        The interface object for the :ref:`ZCC web forwarding profile interface <zcc-forwarding_profile>`.

        """
        return ForwardingProfileAPI(self._request_executor)

    @property
    def fail_open_policy(self):
        """
        The interface object for the :ref:`ZCC fail open policy interface <zcc-fail_open_policy>`.

        """
        return FailOpenPolicyAPI(self._request_executor)

    @property
    def web_policy(self):
        """
        The interface object for the :ref:`ZCC web policy interface <zcc-web_policy>`.

        """
        return WebPolicyAPI(self._request_executor)

    @property
    def web_app_service(self):
        """
        The interface object for the :ref:`ZCC web app service interface <zcc-web_app_service>`.

        """
        return WebAppServiceAPI(self._request_executor)

    @property
    def web_privacy(self):
        """
        The interface object for the :ref:`ZCC web privacy interface <zcc-web_privacy>`.

        """
        return WebPrivacyAPI(self._request_executor)

    @property
    def trusted_networks(self):
        """
        The interface object for the :ref:`ZCC trusted networks interface <zcc-trusted_networks>`.

        """
        return TrustedNetworksAPI(self._request_executor)
