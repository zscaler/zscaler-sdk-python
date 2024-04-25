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

from zscaler.utils import Iterator, convert_keys, snake_to_camel
from zscaler.zia import ZIAClient


class RuleLabelsAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_labels(self, **kwargs) -> BoxList:
        """
        Returns the list of ZIA Rule Labels.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.

        Returns:
            :obj:`BoxList`: The list of Rule Labels configured in ZIA.

        Examples:
            List Rule Labels using default settings:

            >>> for label in zia.labels.list_labels():
            ...   print(label)

            List labels, limiting to a maximum of 10 items:

            >>> for label in zia.labels.list_labels(max_items=10):
            ...    print(label)

            List labels, returning 200 items per page for a maximum of 2 pages:

            >>> for label in zia.labels.list_labels(page_size=200, max_pages=2):
            ...    print(label)

        """
        return BoxList(Iterator(self.rest, "ruleLabels", **kwargs))

    def get_label(self, label_id: str) -> Box:
        """
        Returns the label details for a given Rule Label.

        Args:
            label_id (str): The unique identifier for the Rule Label.

        Returns:
            :obj:`Box`: The Rule Label resource record.

        Examples:
            >>> label = zia.labels.get_label('99999')

        """
        response = self.rest.get("/ruleLabels/%s" % (label_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def add_label(self, name: str, **kwargs) -> Box:
        """
        Creates a new ZIA Rule Label.

        Args:
            name (str):
                The name of the Rule Label.

        Keyword Args:
            description (str):
                Additional information about the Rule Label.

        Returns:
            :obj:`Box`: The newly added Rule Label resource record.

        Examples:
            Add a label with default parameters:

            >>> label = zia.labels.add_label("My New Label")

            Add a label with description:

            >>> label = zia.labels.add_label("My Second Label":
            ...    description="My second label description")

        """
        payload = {"name": name}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("ruleLabels", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_label(self, label_id: str, **kwargs):
        """
        Updates information for the specified ZIA Rule Label.

        Args:
            label_id (str): The unique id for the Rule Label that will be updated.

        Keyword Args:
            name (str): The name of the Rule Label.
            description (str): Additional information for the Rule Label.

        Returns:
            :obj:`Box`: The updated Rule Label resource record.

        Examples:
            Update the name of a Rule Label:

            >>> label = zia.labels.update_label(99999,
            ...    name="Updated Label Name")

            Update the name and description of a Rule Label:

            >>> label = zia.labels.update_label(99999,
            ...    name="Updated Label Name",
            ...    description="Updated Label Description")

        """
        # Get the label data from ZIA
        payload = convert_keys(self.get_label(label_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"ruleLabels/{label_id}", json=payload)

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_label(label_id)

    def delete_label(self, label_id):
        """
        Deletes the specified Rule Label.

        Args:
            label_id (str): The unique identifier of the Rule Label that will be deleted.

        Returns:
            :obj:`int`: The response code for the request.

        Examples
            >>> user = zia.labels.delete_label('99999')

        """
        return self.rest.delete(f"ruleLabels/{label_id}").status_code
