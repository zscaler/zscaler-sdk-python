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
from zscaler.zpa.models.tag_namespace import Namespace, UpdateStatusRequest
from zscaler.utils import format_url
from zscaler.types import APIResult


def _post_search_all_pages(
    request_executor: RequestExecutor,
    api_url: str,
    model_class: type,
    search_body: Dict[str, Any],
    params: Optional[Dict[str, Any]],
    form_response_body,
) -> tuple:
    """Fetch all pages from a ZPA POST search endpoint."""
    all_items = []
    page = 1
    page_size = 100
    last_response = None

    while True:
        body = dict(search_body)
        body["pageBy"] = {
            "page": page,
            "pageSize": page_size,
            "validPage": 0,
            "validPageSize": 0,
        }

        req, err = request_executor.create_request("POST", api_url, body=body, params=params)
        if err:
            return (None, last_response, err)

        resp, err = request_executor.execute(req, model_class)
        if err:
            return (None, resp, err)

        last_response = resp
        items = resp.get_results() if resp else []

        try:
            for item in items:
                all_items.append(model_class(form_response_body(item)))
        except Exception as error:
            return (None, resp, error)

        total_pages = 1
        if resp and resp.get_body():
            body_data = resp.get_body()
            if isinstance(body_data, dict):
                tp = body_data.get("totalPages")
                if tp is not None:
                    total_pages = int(tp) if isinstance(tp, (int, str)) else 1

        if page >= total_pages:
            break
        page += 1

    return (all_items, last_response, None)


class TagNamespaceAPI(APIClient):
    """A client object for the Tag Namespace resource."""

    def __init__(self, request_executor: RequestExecutor, config: Dict[str, Any]) -> None:
        super().__init__()
        self._request_executor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._namespace_endpoint = f"{self._zpa_base_endpoint}/namespace"
        self._namespace_search_endpoint = f"{self._zpa_base_endpoint}/namespace/search"

    def list_namespaces(self, query_params: Optional[dict] = None) -> APIResult[List[Namespace]]:
        """
        Get all tag namespaces.

        Args:
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant, if applicable.

        Returns:
            tuple: (list of Namespace, Response, error).

        Examples:
            >>> namespaces, _, err = client.zpa.tag_namespace.list_namespaces()
            >>> if err:
            ...     print(err)
            >>> for ns in namespaces:
            ...     print(ns.as_dict())
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        if microtenant_id:
            params = {"microtenantId": microtenant_id}
        else:
            params = {}

        search_body = {
            "sortBy": {"sortName": "name", "sortOrder": "ASC"},
        }
        try:
            return _post_search_all_pages(
                self._request_executor,
                self._namespace_search_endpoint,
                Namespace,
                search_body,
                params,
                self.form_response_body,
            )
        except Exception as error:
            return (None, None, error)

    def get_namespace(self, namespace_id: str, query_params: Optional[dict] = None) -> APIResult[Namespace]:
        """
        Get a tag namespace by ID.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (Namespace, Response, error).

        Examples:
            >>> ns, _, err = client.zpa.tag_namespace.get_namespace("123456")
            >>> if err:
            ...     print(err)
            >>> print(ns.as_dict())
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._namespace_endpoint}/{namespace_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        req, err = self._request_executor.create_request("GET", api_url, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, Namespace)
        if err:
            return (None, resp, err)

        try:
            result = Namespace(self.form_response_body(resp.get_body()))
        except Exception as e:
            return (None, resp, e)
        return (result, resp, None)

    def get_namespace_by_name(self, namespace_name: str, query_params: Optional[dict] = None) -> APIResult[Namespace]:
        """
        Get a tag namespace by name (case-insensitive).

        Args:
            namespace_name (str): The name of the namespace.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (Namespace, Response, error).

        Examples:
            >>> ns, _, err = client.zpa.tag_namespace.get_namespace_by_name("MyNamespace")
            >>> if err:
            ...     print(err)
            >>> print(ns.as_dict())
        """
        namespaces, resp, err = self.list_namespaces(query_params)
        if err:
            return (None, resp, err)
        name_lower = namespace_name.lower()
        for ns in namespaces or []:
            if ns.name and ns.name.lower() == name_lower:
                return (ns, resp, None)
        return (None, resp, ValueError(f"no namespace named '{namespace_name}' was found"))

    def create_namespace(self, namespace: Namespace, query_params: Optional[dict] = None) -> APIResult[Namespace]:
        """
        Create a tag namespace.

        Args:
            namespace (Namespace): The namespace object to create.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (Namespace, Response, error).

        Examples:
            >>> ns = Namespace({"name": "MyNS", "enabled": True})
            >>> created, _, err = client.zpa.tag_namespace.create_namespace(ns)
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        body = namespace.request_format()
        req, err = self._request_executor.create_request("POST", self._namespace_endpoint, body=body, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, Namespace)
        if err:
            return (None, resp, err)

        try:
            result = Namespace(self.form_response_body(resp.get_body()))
        except Exception as e:
            return (None, resp, e)
        return (result, resp, None)

    def update_namespace(
        self,
        namespace_id: str,
        namespace: Namespace,
        query_params: Optional[dict] = None,
    ) -> APIResult[Namespace]:
        """
        Update a tag namespace.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            namespace (Namespace): The namespace object with updated fields.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (Namespace, Response, error).

        Examples:
            >>> ns.name = "UpdatedName"
            >>> updated, resp, err = client.zpa.tag_namespace.update_namespace("123", ns)
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._namespace_endpoint}/{namespace_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        body = namespace.request_format()
        req, err = self._request_executor.create_request("PUT", api_url, body=body, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req, Namespace)
        if err:
            return (None, resp, err)

        if resp is None or not resp.get_body():
            return (Namespace({"id": namespace_id}), resp, None)

        try:
            result = Namespace(self.form_response_body(resp.get_body()))
        except Exception as error:
            return (None, resp, error)
        return (result, resp, None)

    def delete_namespace(self, namespace_id: str, query_params: Optional[dict] = None) -> APIResult[None]:
        """
        Delete a tag namespace.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (None, Response, error).

        Examples:
            >>> _, _, err = client.zpa.tag_namespace.delete_namespace("123")
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._namespace_endpoint}/{namespace_id}")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        req, err = self._request_executor.create_request("DELETE", api_url, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req)
        return (None, resp, err)

    def update_namespace_status(
        self,
        namespace_id: str,
        status_update: UpdateStatusRequest,
        query_params: Optional[dict] = None,
    ) -> APIResult[None]:
        """
        Update the enabled status of a tag namespace.

        Args:
            namespace_id (str): The unique identifier of the namespace.
            status_update (UpdateStatusRequest): The status update request.
            query_params (dict, optional): Map of query parameters.
                ``[query_params.microtenant_id]`` (str): ID of the microtenant.

        Returns:
            tuple: (None, Response, error).

        Examples:
            >>> status = UpdateStatusRequest({"enabled": False})
            >>> _, _, err = client.zpa.tag_namespace.update_namespace_status("123", status)
            >>> if err:
            ...     print(err)
        """
        params = query_params or {}
        microtenant_id = params.get("microtenant_id")
        api_url = format_url(f"{self._namespace_endpoint}/{namespace_id}/status")
        req_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        body = status_update.request_format()
        req, err = self._request_executor.create_request("PUT", api_url, body=body, params=req_params)
        if err:
            return (None, None, err)

        resp, err = self._request_executor.execute(req)
        return (None, resp, err)
