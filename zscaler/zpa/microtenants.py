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

from . import ZPAClient


class MicrotenantsAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_microtenants(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured microtenants.

        Returns:
            :obj:`BoxList`: A list of all configured microtenants.

        Examples:
            >>> for microtenant in zpa.microtenants.list_microtenants():
            ...    pprint(microtenant)

        """
        if "pageSize" in kwargs:
            kwargs.pop("pageSize")
        list, _ = self.rest.get_paginated_data(path="/microtenants", **kwargs)
        return list

    def get_microtenant(self, microtenant_id: str) -> Box:
        """
        Returns information on the specified microtenant.

        Args:
            microtenant_id (str):
                The unique identifier for the microtenant.

        Returns:
            :obj:`Box`: The resource record for the microtenant.

        Examples:
            >>> pprint(zpa.microtenants.get_microtenant('216199618143364393'))

        """
        response = self.rest.get("/microtenants/%s" % (microtenant_id))

        # If the response is not a Box (indicating an error), return None or handle the error
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                raise Exception(f"Failed to retrieve microtenant: {status_code} - {response.text}")

        # Otherwise, return the formatted Box object
        return response

    def get_microtenant_summary(self) -> Box:
        """
        Returns the name and ID of the configured Microtenant

        Args:

        Returns:
            :obj:`Box`: The resource record for the microtenant.

        Examples:
            >>> pprint(zpa.microtenants.get_microtenant_summary())

        """
        return self.rest.get("microtenants/summary")

    def get_microtenant_by_name(self, name: str, **kwargs) -> Box:
        """
        Returns information on the microtenant with the specified name.

        Args:
            name (str): The name of the microtenant.

        Returns:
            :obj:`Box` or None: The resource record for the microtenant if found, otherwise None.

        Examples:
            >>> microtenant = zpa.microtenants.get_microtenant_by_name('example_name')
            >>> if microtenant:
            ...     pprint(microtenant)
            ... else:
            ...     print("Microtenant not found")
        """
        microtenants = self.list_microtenants(**kwargs)
        for microtenant in microtenants:
            if microtenant.get("name") == name:
                return microtenant
        return None

    def add_microtenant(self, name: str, criteria_attribute: str, criteria_attribute_values: list, **kwargs) -> Box:
        """
        Add a new microtenant.

        Args:
            name (str): The name of the microtenant.
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): A description for the microtenant.
            enabled (bool): Whether the Microtenant is enabled or not. Defaults to True.
            privileged_approvals_enabled (bool): Whether the Microtenant is enabled or not. Defaults to True.
            criteria_attribute (str): The criteria attribute for the Microtenant. The supported value is AuthDomain.
            criteria_attribute_values (list): The value for the criteria attribute.
                This is the valid authentication domains configured for a customer (e.g., ExampleAuthDomain.com).

        Returns:
            :obj:`Box`: The resource record for the newly created microtenant, including the user block.

        Examples:
            Create a server with the minimum required parameters:

            >>> zpa.microtenants.add_microtenant(
            ...   name='Microtenant_A',
            ...   description='New Microtenant',
            ...   enabled=True,
            ...   privileged_approvals_enabled=True,
            ...   criteria_attribute_values=['acme.com'],
            ...   criteria_attribute='AuthDomain',
            ... )

        """
        payload = {"name": name, "criteriaAttribute": criteria_attribute, "criteriaAttributeValues": criteria_attribute_values}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value
        response = self.rest.post("microtenants", json=payload)
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_microtenant(self, microtenant_id: str, **kwargs) -> Box:
        """
        Updates the specified microtenant.

        Args:
            microtenant_id (str):
                The unique identifier for the microtenant being updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            name (str): The name of the microtenant.
            description (str): A description for the microtenant.
            enabled (bool): Whether the Microtenant is enabled or not. Defaults to True.
            privileged_approvals_enabled (bool): Whether the Microtenant is enabled or not. Defaults to True.
            criteria_attribute (str): The criteria attribute for the Microtenant. The supported value is AuthDomain.
            criteria_attribute_values (list): The value for the criteria attribute.
                This is the valid authentication domains configured for a customer (e.g., ExampleAuthDomain.com).

        Returns:
            :obj:`Box`: The resource record for the updated microtenant.

        Examples:
            Update the name of a microtenant:

            >>> zpa.servers.update_server(
            ...   '99999',
            ...   name='Update_Microtenant_A')

            Disable the privileged_approvals_enabled:

            >>> zpa.microtenants.update_microtenant(
            ...   microtenant_id='216199618143368569',
            ...   name='Microtenant_A',
            ...   description='Microtenant_A',
            ...   enabled=True,
            ...   privileged_approvals_enabled=False,
            ...   criteria_attribute_values=['acme.com'],
            ...   criteria_attribute='AuthDomain',
            ... )

        """
        # Retrieve existing microtenant data
        existing_microtenant_response = self.get_microtenant(microtenant_id)

        # Handle Response object (in case of error)
        if isinstance(existing_microtenant_response, Response):
            if existing_microtenant_response.status_code != 200:
                raise Exception(f"Failed to retrieve microtenant: {existing_microtenant_response.status_code}")
            # If there's content, parse the response as JSON
            if existing_microtenant_response.text.strip():
                existing_microtenant = existing_microtenant_response.json()
            else:
                existing_microtenant = {}  # Treat as empty, no error
        else:
            existing_microtenant = existing_microtenant_response

        # Prepare the payload
        payload = {snake_to_camel(k): v for k, v in existing_microtenant.items()}

        # Add optional parameters from kwargs
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Send the PUT request to update the microtenant
        resp = self.rest.put(f"microtenants/{microtenant_id}", json=payload)

        # Handle 204 No Content as success
        if resp.status_code == 204:
            print(f"Update successful for microtenant {microtenant_id} (204 No Content).")
            return self.get_microtenant(microtenant_id)

        # Handle 200 OK as success
        if resp.status_code == 200:
            print(f"Update successful for microtenant {microtenant_id} (200 OK).")
            return self.get_microtenant(microtenant_id)

        # Raise exception for any other status code
        raise Exception(f"Failed to update microtenant: {resp.status_code}, {resp.text}")

    def delete_microtenant(self, microtenant_id: str) -> int:
        """
        Delete the specified microtenant.

        Args:
            microtenant_id (str): The unique identifier for the Microtenant to be deleted.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.microtenant.delete_microtenant('99999')

        """
        return self.rest.delete(f"microtenants/{microtenant_id}").status_code
