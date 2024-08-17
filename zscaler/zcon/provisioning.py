# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from box import Box, BoxList
from zscaler.utils import Iterator
from zscaler.zcon.client import ZCONClient


class ProvisioningAPI:
    def __init__(self, client: ZCONClient):
        self.rest = client

    def list_api_keys(self, **kwargs) -> BoxList:
        """
        List all existing API keys.

        Keyword Args:
            include_partner_keys (bool): Include / exclude partner keys in the response.

        Returns:
            :obj:`BoxList`: The list of API keys.

        Examples:
            List all API keys::

                for api_key in zcon.admin.list_api_keys():
                    print(api_key)
        """
        params = {}
        if "include_partner_keys" in kwargs:
            params["includePartnerKeys"] = kwargs["include_partner_keys"]

        return self.rest.get("apiKeys", params=params)

    def regenerate_api_key(self, api_key_id: str) -> Box:
        """
        Regenerate the specified API key.

        Args:
            api_key_id (str): The ID of the API key to regenerate.

        Returns:
            :obj:`Box`: The regenerated API key.

        Examples:
            Regenerate an API key::

                print(zcon.admin.regenerate_api_key("123456789"))

        """
        return self.rest.post(f"apiKeys/{api_key_id}/regenerate")

    def list_provisioning_url(self, **kwargs) -> BoxList:
        """
        List all provisioning URLs.

        Keyword Args:
            id (list): The ID of the provisioning URL to include.
            name (string): Name of Cloud & Branch Connector provisioning template.
            desc (string): Description of Cloud & Branch Connector provisioning template.
            prov_url (string): URL of Cloud & Branch Connector provisioning template.
            prov_url_type (string): URL type of Cloud & Branch Connector provisioning template.
            prov_url_data (list): Cloud & Branch Connector provisioning URL content.
            used_in_ec_groups (list): Indicates that the provisioning template is in use.
            status (string): Deployment status of Cloud & Branch Connector provisioning template.
            last_mod_uid (list): User ID of last time Cloud & Branch Connector provisioning template was modified.
            last_mod_time (int): Deployment status of Cloud & Branch Connector provisioning template.

        Returns:
            :obj:`BoxList`: The list of provisioning URLs.

        Examples:
            Print all provisioning URLs::

                roles = zcon.provisioning.list_provisioning_url()
                for role in roles:
                    print(role)
        """
        return BoxList(Iterator(self.rest, "provUrl", **kwargs))

    def get_provisioning_url(self, provision_id: str) -> Box:
        """
        Get details for a provisioning template by ID.

        Args:
            provision_id (str): ID of Cloud & Branch Connector provisioning template.

        Returns:
            :obj:`Box`: The provisiong template url details.

        Examples:
            Print the details of a provisioning template url:

                print(zcon.provisioning.get_provisioning_url("123456789")

        """
        return self.rest.get(f"provUrl/{provision_id}")

    def list_public_account_details(self) -> BoxList:
        """
        Returns a list of public cloud account information.

        Keyword Args:
            **account_id (string): Account or subscription ID of public cloud account.
            **platform_id (string): Public cloud platform (AWS or Azure).
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.

        Returns:
            :obj:`BoxList`: List of configured public account details.

        Examples:

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zcon.provisioning.list_public_account_details(page_size=200, max_pages=2):
            ...    print(location)

        """
        return self.rest.get("publicCloudAccountDetails")

    def get_public_account_details(self, account_id: str) -> Box:
        """
        Returns information for the public (Cloud Connector) cloud account information for the specified ID.

        Args:
            **account_id (str, optional): Account or subscription ID of public cloud account.
            **platform_id (string): Public cloud platform (AWS or Azure).

        Returns:
            :obj:`Box`: The requested public account record.

        Examples:
            >>> location = zcon.provisioning.get_public_account_details('97456691')

        """
        return self.rest.get(f"publicCloudAccountDetails/{account_id}")

    def list_public_account_details_lite(self) -> BoxList:
        """
        Returns a subset of public (Cloud Connector) cloud account information.

        Keyword Args:
            **account_id (str, optional):
                Account or subscription ID of public cloud account.
            **platform_id (string):
                Public cloud platform (AWS or Azure).
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.

        Returns:
            :obj:`BoxList`: A lite list of public account details.

        Examples:
            List accounts with default settings:

            >>> for account in zcon.provisioning.list_public_account_details_lite():
            ...    print(account)

            List accounts, limiting to a maximum of 10 items:

            >>> for account in zcon.provisioning.list_public_account_details_lite(max_items=10):
            ...    print(account)

            List accounts, returning 200 items per page for a maximum of 2 pages:

            >>> for account in zcon.provisioning.list_public_account_details_lite(page_size=200, max_pages=2):
            ...    print(account)

        """
        return self.rest.get("publicCloudAccountDetails/lite")

    def list_public_account_status(self) -> BoxList:
        """
        Returns a List of public (Cloud Connector) cloud account status information (enabled/disabled).

        Returns:
            :obj:`BoxList`: List of configured public account status.

        Examples:
            List public account status:
            >>> status = zcon.provisioning.list_public_account_status()
            ...    print(status)
        """
        response = self.rest.get("publicCloudAccountIdStatus")
        return response

    def update_public_account_status(self) -> Box:
        """
        Update an existing public account status.

        Keyword Args:
            account_id_enabled (bool): Indicates whether public cloud account is enabled.
            sub_id_enabled (bool): Indicates whether public cloud subscription is enabled.

        Returns:
            :obj:`Box`: The updated public account status details.

        Examples:
            Update the public account status::

                print(zcon.provisioning.update_public_account_status(account_id_enabled=True, sub_id_enabled=False))
        """
        return self.rest.put("publicCloudAccountIdStatus")
