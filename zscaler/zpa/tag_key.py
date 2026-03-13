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
from zscaler.zpa.models.tag_key import TagKey, TagValue, BulkUpdateStatusRequest
from zscaler.zpa.tag_namespace import _post_search_all_pages
from zscaler.utils import format_url
from zscaler.types import APIResult


class TagKeyAPI(APIClient):
    """A client object for the Tag Key resource (scoped to a namespace)."""

    def __init__(self, request_executor: RequestExecutor, config: Dict[str, Any]) -> None:
        super().__init__()
        self._request_executor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def _namespace_path(self, namespace_id: str) -> str:
        return f"{self._zpa_base_endpoint}/namespace/{namespace_id}"

    def list_tag_keys(
        self,
        namespace_id: str,
        query_params: Optional[dict] = None,
    ) -> APIResult[List[TagKey]]:
        """
        Get all tag keys in a namespace.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (list of TagKey, Response, error).

        Examples:
            >>> keys, _, err = client.zpa.tag_key.list_tag_keys("namespace-123")
            >>> if err:
            ...     print(err)
            >>> for k in keys:
            ...     print(k.as_dict())
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        search_url = f"{self._namespace_path(namespace_id)}/tagKey/search"
        search_body = {"sortBy": {"sortName": "name", "sortOrder": "ASC"}}

        try:
            return _post_search_all_pages(
                self._request_executor,
                search_url,
                TagKey,
                search_body,
                req_params,
                self.form_response_body,
            )
        except Exception as error:
            return (None, None, error)

    def get_tag_key(
        self,
        namespace_id: str,
        tag_key_id: str,
        query_params: Optional[dict] = None,
    ) -> APIResult[TagKey]:
        """
        Get a tag key by ID.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            tag_key_id (str): The unique identifier of the tag key.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (TagKey, Response, error).

        Examples:
            >>> key, _, err = client.zpa.tag_key.get_tag_key("ns-123", "key-456")
            >>> if err:
            ...     print(err)
            >>> print(key.as_dict())
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._namespace_path(namespace_id)}/tagKey/{tag_key_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        req, err = self._request_executor.create_request("GET", api_url, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, TagKey)
        if err:
            return (None, resp, err)

        try:
            result = TagKey(self.form_response_body(resp.get_body()))
        except Exception as e:
            return (None, resp, e)
        return (result, resp, None)

    def get_tag_key_by_name(
        self,
        namespace_id: str,
        tag_key_name: str,
        query_params: Optional[dict] = None,
    ) -> APIResult[TagKey]:
        """
        Get a tag key by name (case-insensitive).

        Args:
            namespace_id (str): The unique identifier of the namespace.
            tag_key_name (str): The name of the tag key.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (TagKey, Response, error).

        Examples:
            >>> key, _, err = client.zpa.tag_key.get_tag_key_by_name("ns-123", "environment")
            >>> if err:
            ...     print(err)
            >>> print(key.as_dict())
        """
        keys, resp, err = self.list_tag_keys(namespace_id, query_params)
        if err:
            return (None, resp, err)
        name_lower = tag_key_name.lower()
        for k in keys or []:
            if k.name and k.name.lower() == name_lower:
                return (k, resp, None)
        return (None, resp, ValueError(f"no tag key named '{tag_key_name}' was found"))

    def create_tag_key(
        self,
        namespace_id: str,
        tag_key: TagKey,
        query_params: Optional[dict] = None,
    ) -> APIResult[TagKey]:
        """
        Create a tag key in a namespace.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            tag_key (TagKey): The tag key object to create.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (TagKey, Response, error).

        Examples:
            >>> key = TagKey({"name": "env", "enabled": True, "tagValues": []})
            >>> created, _, err = client.zpa.tag_key.create_tag_key("ns-123", key)
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        body = tag_key.request_format()
        if body.get("tagValues") is None:
            body["tagValues"] = []

        api_url = format_url(f"{self._namespace_path(namespace_id)}/tagKey")
        req, err = self._request_executor.create_request("POST", api_url, body=body, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, TagKey)
        if err:
            return (None, resp, err)

        try:
            result = TagKey(self.form_response_body(resp.get_body()))
        except Exception as e:
            return (None, resp, e)
        return (result, resp, None)

    def update_tag_key(
        self,
        namespace_id: str,
        tag_key_id: str,
        tag_key: TagKey,
        query_params: Optional[dict] = None,
    ) -> APIResult[TagKey]:
        """
        Update a tag key.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            tag_key_id (str): The unique identifier of the tag key.
            tag_key (TagKey): The tag key object with updated fields.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (TagKey, Response, error).

        Examples:
            >>> key.name = "updated-name"
            >>> updated, resp, err = client.zpa.tag_key.update_tag_key("ns-123", "key-456", key)
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._namespace_path(namespace_id)}/tagKey/{tag_key_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        body = tag_key.request_format()
        if body.get("tagValues") is None:
            body["tagValues"] = []

        req, err = self._request_executor.create_request("PUT", api_url, body=body, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, TagKey)
        if err:
            return (None, resp, err)

        if resp is None or not resp.get_body():
            return (TagKey({"id": tag_key_id}), resp, None)

        try:
            result = TagKey(self.form_response_body(resp.get_body()))
        except Exception as error:
            return (None, resp, error)
        return (result, resp, None)

    def delete_tag_key(
        self,
        namespace_id: str,
        tag_key_id: str,
        query_params: Optional[dict] = None,
    ) -> APIResult[None]:
        """
        Delete a tag key.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            tag_key_id (str): The unique identifier of the tag key.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (None, Response, error).

        Examples:
            >>> _, _, err = client.zpa.tag_key.delete_tag_key("ns-123", "key-456")
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._namespace_path(namespace_id)}/tagKey/{tag_key_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        req, err = self._request_executor.create_request("DELETE", api_url, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req)
        return (None, resp, err)

    def bulk_update_status(
        self,
        namespace_id: str,
        bulk_update: BulkUpdateStatusRequest,
        query_params: Optional[dict] = None,
    ) -> APIResult[None]:
        """
        Bulk update the enabled status of tag keys.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            bulk_update (BulkUpdateStatusRequest): The bulk update request.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (None, Response, error).

        Examples:
            >>> update = BulkUpdateStatusRequest({"enabled": False, "tagKeyIds": ["k1", "k2"]})
            >>> _, _, err = client.zpa.tag_key.bulk_update_status("ns-123", update)
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._namespace_path(namespace_id)}/tagKey/bulkUpdateStatus")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        body = bulk_update.request_format()
        req, err = self._request_executor.create_request("PUT", api_url, body=body, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req)
        return (None, resp, err)
