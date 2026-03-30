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

from typing import Dict, List, Optional, Any
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.tag_group import TagGroup, TagGroupTag
from zscaler.zpa.tag_namespace import _post_search_all_pages
from zscaler.utils import format_url
from zscaler.types import APIResult


class TagGroupAPI(APIClient):
    """A client object for the Tag Group resource."""

    def __init__(self, request_executor, config: Dict[str, Any]) -> None:
        super().__init__()
        self._request_executor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._tag_group_endpoint = f"{self._zpa_base_endpoint}/tagGroup"
        self._tag_group_search_endpoint = f"{self._zpa_base_endpoint}/tagGroup/search"

    def list_tag_groups(self, query_params: Optional[dict] = None) -> APIResult[List[TagGroup]]:
        """
        Get all tag groups.

        Args:
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (list of TagGroup, Response, error).

        Examples:
            >>> groups, _, err = client.zpa.tag_group.list_tag_groups()
            >>> if err:
            ...     print(err)
            >>> for g in groups:
            ...     print(g.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        search_body = {"sortBy": {"sortName": "name", "sortOrder": "ASC"}}

        try:
            return _post_search_all_pages(
                self._request_executor,
                self._tag_group_search_endpoint,
                TagGroup,
                search_body,
                req_params,
                self.form_response_body,
            )
        except Exception as error:
            return (None, None, error)

    def get_tag_group(self, tag_group_id: str, query_params: Optional[dict] = None) -> APIResult[TagGroup]:
        """
        Get a tag group by ID.

        Args:
            tag_group_id (str): The unique identifier of the tag group.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (TagGroup, Response, error).

        Examples:
            >>> group, _, err = client.zpa.tag_group.get_tag_group("123456")
            >>> if err:
            ...     print(err)
            >>> print(group.as_dict())
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._tag_group_endpoint}/{tag_group_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        req, err = self._request_executor.create_request("GET", api_url, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, TagGroup)
        if err:
            return (None, resp, err)

        try:
            result = TagGroup(self.form_response_body(resp.get_body()))
        except Exception as e:
            return (None, resp, e)
        return (result, resp, None)

    def get_tag_group_by_name(self, tag_group_name: str, query_params: Optional[dict] = None) -> APIResult[TagGroup]:
        """
        Get a tag group by name (case-insensitive).

        Args:
            tag_group_name (str): The name of the tag group.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (TagGroup, Response, error).

        Examples:
            >>> group, _, err = client.zpa.tag_group.get_tag_group_by_name("MyGroup")
            >>> if err:
            ...     print(err)
            >>> print(group.as_dict())
        """
        groups, resp, err = self.list_tag_groups(query_params)
        if err:
            return (None, resp, err)
        name_lower = tag_group_name.lower()
        for g in groups or []:
            if g.name and g.name.lower() == name_lower:
                return (g, resp, None)
        return (None, resp, ValueError(f"no tag group named '{tag_group_name}' was found"))

    def create_tag_group(self, tag_group: TagGroup, query_params: Optional[dict] = None) -> APIResult[TagGroup]:
        """
        Create a tag group.

        Args:
            tag_group (TagGroup): The tag group object to create.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (TagGroup, Response, error).

        Examples:
            >>> group = TagGroup({"name": "MyGroup", "tags": []})
            >>> created, _, err = client.zpa.tag_group.create_tag_group(group)
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        body = tag_group.request_format()
        if body.get("tags") is None:
            body["tags"] = []

        req, err = self._request_executor.create_request("POST", self._tag_group_endpoint, body=body, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, TagGroup)
        if err:
            return (None, resp, err)

        try:
            result = TagGroup(self.form_response_body(resp.get_body()))
        except Exception as e:
            return (None, resp, e)
        return (result, resp, None)

    def update_tag_group(
        self,
        tag_group_id: str,
        tag_group: TagGroup,
        query_params: Optional[dict] = None,
    ) -> APIResult[TagGroup]:
        """
        Update a tag group.

        Args:
            tag_group_id (str): The unique identifier of the tag group.
            tag_group (TagGroup): The tag group object with updated fields.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (TagGroup, Response, error).

        Examples:
            >>> group.name = "UpdatedName"
            >>> updated, resp, err = client.zpa.tag_group.update_tag_group("123", group)
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._tag_group_endpoint}/{tag_group_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        body = tag_group.request_format()
        if body.get("tags") is None:
            body["tags"] = []

        req, err = self._request_executor.create_request("PUT", api_url, body=body, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, TagGroup)
        if err:
            return (None, resp, err)

        if resp is None or not resp.get_body():
            return (TagGroup({"id": tag_group_id}), resp, None)

        try:
            result = TagGroup(self.form_response_body(resp.get_body()))
        except Exception as error:
            return (None, resp, error)
        return (result, resp, None)

    def delete_tag_group(self, tag_group_id: str, query_params: Optional[dict] = None) -> APIResult[None]:
        """
        Delete a tag group.

        Args:
            tag_group_id (str): The unique identifier of the tag group.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (None, Response, error).

        Examples:
            >>> _, _, err = client.zpa.tag_group.delete_tag_group("123")
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._tag_group_endpoint}/{tag_group_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        req, err = self._request_executor.create_request("DELETE", api_url, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req)
        return (None, resp, err)
