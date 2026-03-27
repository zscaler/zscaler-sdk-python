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

from zscaler.request_executor import RequestExecutor
from zscaler.zid.api_client import APIClientAPI
from zscaler.zid.user_entitlement import EntitlementAPI
from zscaler.zid.groups import GroupsAPI
from zscaler.zid.users import UsersAPI
from zscaler.zid.resource_servers import ResourceServersAPI


class ZIdService:
    """Zid service client, exposing Z Identity admin APIs."""

    def __init__(self, request_executor: RequestExecutor):
        # Ensure the service gets the request executor from the Client object
        self._request_executor = request_executor

    @property
    def api_client(self) -> APIClientAPI:
        """
        The interface object for the :ref:`Zid API Client interface <zid-api_client>`.

        """
        return APIClientAPI(self._request_executor)

    @property
    def groups(self) -> GroupsAPI:
        """
        The interface object for the :ref:`Zid Groups interface <zid-groups>`.

        """
        return GroupsAPI(self._request_executor)

    @property
    def users(self) -> UsersAPI:
        """
        The interface object for the :ref:`Zid Users interface <zid-users>`.

        """
        return UsersAPI(self._request_executor)

    @property
    def user_entitlement(self) -> EntitlementAPI:
        """
        The interface object for the :ref:`Zid Entitlement interface <zid-user_entitlement>`.

        """
        return EntitlementAPI(self._request_executor)

    @property
    def resource_servers(self) -> ResourceServersAPI:
        """
        The interface object for the :ref:`Zid Resource Servers interface <zid-resource_servers>`.

        """
        return ResourceServersAPI(self._request_executor)
