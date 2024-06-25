# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from box import Box, BoxList
from requests import Response

from zscaler.utils import snake_to_camel
from zscaler.zpa.client import ZPAClient


def simplify_key_type(key_type):
    # Simplify the key type for our users
    if key_type == "connector":
        return "CONNECTOR_GRP"
    elif key_type == "service_edge":
        return "SERVICE_EDGE_GRP"
    else:
        raise ValueError("Unexpected key type.")


class ProvisioningKeyAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_provisioning_keys(self, key_type: str, **kwargs) -> BoxList:
        """
        Returns a list of all configured provisioning keys that match the specified ``key_type``.

        Args:
            key_type (str): The type of provisioning key, accepted values are:
                ``connector`` and ``service_edge``.
            **kwargs: Optional keyword args.

        Keyword Args:
            max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            pagesize (int, optional):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list containing the requested provisioning keys.

        Examples:
            List all App Connector provisioning keys.

            >>> for key in zpa.provisioning.list_provisioning_keys(key_type="connector"):
            ...    print(key)

            List all Service Edge provisioning keys.

            >>> for key in zpa.provisioning.list_provisioning_keys(key_type="service_edge"):
            ...    print(key)

        """
        list, _ = self.rest.get_paginated_data(
            path=f"/associationType/{simplify_key_type(key_type)}/provisioningKey",
            **kwargs,
        )
        return list

    def get_provisioning_key(self, key_id: str, key_type: str, **kwargs) -> Box:
        """
        Returns information on the specified provisioning key.

        Args:
            key_id (str): The unique id of the provisioning key.
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.
            **kwargs: Optional keyword arguments.

        Keyword Args:
            microtenant_id (str): The unique identifier for the microtenant.

        Returns:
            :obj:`Box`: The requested provisioning key resource record.

        Examples:
            Get the specified App Connector key.

            >>> provisioning_key = zpa.provisioning.get_provisioning_key("999999",
            ...    key_type="connector")

            Get the specified Service Edge key.

            >>> provisioning_key = zpa.provisioning.get_provisioning_key("888888",
            ...    key_type="service_edge")

            Get the specified App Connector key for a microtenant.

            >>> provisioning_key = zpa.provisioning.get_provisioning_key("999999",
            ...    key_type="connector", microtenant_id="12345")

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get(f"associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}", params=params)

    def add_provisioning_key(
        self,
        key_type: str,
        name: str,
        max_usage: str,
        enrollment_cert_id: str,
        component_id: str,
        **kwargs,
    ) -> Box:
        """
        Adds a new provisioning key to ZPA.

        Args:
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.
            name (str): The name of the provisioning key.
            max_usage (int): The maximum amount of times this key can be used.
            enrollment_cert_id (str):
                The unique id of the enrollment certificate that will be used for this provisioning key.
            component_id (str):
                The unique id of the component that this provisioning key will be linked to. For App Connectors, this
                will be the App Connector Group Id. For Service Edges, this will be the Service Edge Group Id.
            **kwargs: Optional keyword args.

        Keyword Args:
            enabled (bool): Enable the provisioning key. Defaults to ``True``.
            microtenant_id (str): The microtenant ID to be used for this request.

        Returns:
            :obj:`Box`: The newly created Provisioning Key resource record.

        Examples:
            Add a new App Connector Provisioning Key that can be used a maximum of 2 times.

            >>> key = zpa.provisioning.add_provisioning_key(key_type="connector",
            ...    name="Example App Connector Provisioning Key",
            ...    max_usage=2,
            ...    enrollment_cert_id="99999",
            ...    component_id="888888")

            Add a new Service Edge Provisioning Key in the disabled state that can be used once.

            >>> key = zpa.provisioning.add_provisioning_key(key_type="service_edge",
            ...    name="Example Service Edge Provisioning Key",
            ...    max_usage=1,
            ...    enrollment_cert_id="99999",
            ...    component_id="777777"
            ...    enabled=False)

        """
        payload = {
            "name": name,
            "maxUsage": max_usage,
            "enrollmentCertId": enrollment_cert_id,
            "zcomponentId": component_id,
        }

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(
            f"associationType/{simplify_key_type(key_type)}/provisioningKey", json=payload, params=params
        )
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_provisioning_key(self, key_id: str, key_type: str, **kwargs) -> Box:
        """
        Updates the specified provisioning key.

        Args:
            key_id (str): The unique id of the Provisioning Key being updated.
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the provisioning key.
            max_usage (int): The maximum amount of times this key can be used.
            enrollment_cert_id (str):
                The unique id of the enrollment certificate that will be used for this provisioning key.
            component_id (str):
                The unique id of the component that this provisioning key will be linked to. For App Connectors, this
                will be the App Connector Group Id. For Service Edges, this will be the Service Edge Group Id.
            microtenant_id (str): The microtenant ID to be used for this request.

        Returns:
            :obj:`Box`: The updated Provisioning Key resource record.

        Examples:
            Update the name of an App Connector provisioning key:

            >>> updated_key = zpa.provisioning.update_provisioning_key('999999',
            ...    key_type="connector",
            ...    name="Updated Name")

            Change the max usage of a Service Edge provisioning key:

            >>> updated_key = zpa.provisioning.update_provisioning_key('888888',
            ...    key_type="service_edge",
            ...    max_usage=10)

        """

        # Get the provided provisioning key record
        payload = {snake_to_camel(k): v for k, v in self.get_provisioning_key(key_id, key_type=key_type).items()}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        resp = self.rest.put(
            f"associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}", json=payload, params=params
        ).status_code

        if not isinstance(resp, Response):
            return self.get_provisioning_key(key_id, key_type=key_type)

    def delete_provisioning_key(self, key_id: str, key_type: str, **kwargs) -> int:
        """
        Deletes the specified provisioning key from ZPA.

        Args:
            key_id (str): The unique id of the provisioning key that will be deleted.
            key_type (str): The type of provisioning key, accepted values are:

                ``connector`` and ``service_edge``.
            **kwargs: Optional keyword args.

        Keyword Args:
            microtenant_id (str): The microtenant ID to be used for this request.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Delete an App Connector provisioning key:

            >>> zpa.provisioning.delete_provisioning_key(key_id="999999",
            ...    key_type="connector")

            Delete a Service Edge provisioning key:

            >>> zpa.provisioning.delete_provisioning_key(key_id="888888",
            ...    key_type="service_edge")

        """
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.delete(
            f"associationType/{simplify_key_type(key_type)}/provisioningKey/{key_id}", params=params
        ).status_code
