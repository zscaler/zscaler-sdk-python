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

from typing import Dict, Any, Optional, List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.utils import format_url
from zscaler.types import APIResult
from zscaler.ztb.models.template_router import TemplateRouter
from zscaler.ztb.models.common import Common


class TemplateRouterAPI(APIClient):
    """
    Client for the ZTB Groups Router resource.

    Provides CRUD operations for groups router in the
    Zero Trust Branch API.
    """

    _ztb_base_endpoint = "/ztb/api/v3"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_templates(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get Gateway Template

        Args:
            query_params (dict):
                Map of query parameters for the request.

                ``[query_params.search]`` (str):

                ``[query_params.page]`` (int):

                ``[query_params.size]`` (int):

                ``[query_params.sort]`` (str): Available values : name, private_dns, dhcp_service, deployment_type, platform_type, sites, is_default, created_at

                ``[query_params.sortdir]`` (str): Available values : asc, desc

        Returns:
            tuple: A tuple containing (list of TemplateRouter instances, Response, error).

        Examples:
            List all templates:

            >>> template_list, _, error = client.ztb.template_router.list_templates()
            >>> if error:
            ...     print(f"Error listing templates: {error}")
            ...     return
            ... print(f"Total templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /templates
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(TemplateRouter(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_template(self, template_id: str) -> APIResult:
        """
        Fetches a specific template by ID.

        Args:
            template_id (int): The unique identifier for the template.

        Returns:
            tuple: A tuple containing (TemplateRouter instance, Response, error).

        Examples:
            Print a specific Template:

            >>> fetched_template, _, error = client.ztb.template_router.get_template('73459')
            >>> if error:
            ...     print(f"Error fetching template by ID: {error}")
            ...     return
            ... print(f"Fetched template by ID: {fetched_template.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /templates/{template_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TemplateRouter)
        if error:
            return (None, response, error)

        try:
            result = TemplateRouter(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_template(self, **kwargs) -> APIResult:
        """
        Creates a new ZTB Template.

        Args:
            name (str): The name of the template.
            **kwargs: Optional keyword args.

        Keyword Args:
            display_name (str): The display name for the group.
            type (str): The group type (e.g. ``device``).
            autonomous (bool): Whether the group is autonomous.
            owner (str): The owner of the group.
            member_attributes (dict): Member attribute filters.

        Returns:
            tuple: A tuple containing the newly created Group, response, and error.

        Examples:
            Create a new Group:

            >>> created_group, _, error = client.ztb.groups_router.create_group(
            ...     name="Group01",
            ...     display_name="Group01",
            ...     type="device",
            ...     autonomous=True,
            ...     owner="user",
            ... )
            >>> if error:
            ...     print(f"Error creating group: {error}")
            ...     return
            ... print(f"Group created successfully: {created_group.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /templates
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TemplateRouter)
        if error:
            return (None, response, error)

        try:
            result = TemplateRouter(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_template_put(self, template_id: int, **kwargs) -> APIResult:
        """
        Updates information for the specified ZTB Template (PUT).

        Args:
            template_id (int): The unique ID for the Template.
            **kwargs: Full template replacement fields.

        Returns:
            tuple: A tuple containing the updated Template, response, and error.

        Examples:
            Update an existing Template:

            >>> updated_group, _, error = client.ztb.groups_router.update_group_put(
            ...     group_id='73459',
            ...     name="Group01",
            ...     display_name="Group01",
            ...     type="device",
            ...     autonomous=True,
            ...     owner="user",
            ... )
            >>> if error:
            ...     print(f"Error updating group: {error}")
            ...     return
            ... print(f"Group updated successfully (PUT): {updated_group.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /templates/{template_id}
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, headers={})

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, TemplateRouter)
        if error:
            return (None, response, error)

        try:
            result = TemplateRouter(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_template(self, template_id: int) -> APIResult[dict]:
        """
        Deletes the specified Template.

        Args:
            template_id (int): The unique identifier of the Template.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Template:

            >>> _, _, error = client.ztb.template_router.delete_template('73459')
            >>> if error:
            ...     print(f"Error deleting template: {error}")
            ...     return
            ... print(f"Template with ID 73459 deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /templates/{template_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def list_template_interfaces(self, platform: str, query_params: Optional[dict] = None) -> APIResult:
        """
        Get Gateway Template Interfaces.

        Args:
            platform (str): The platform type (e.g. ``vm``, ``hardware``).
            query_params (dict):
                Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of Common instances, Response, error).

        Examples:
            List all template interfaces for a platform:

            >>> template_list, _, error = client.ztb.template_router.list_template_interfaces(
            ...     platform="vm"
            ... )
            >>> if error:
            ...     print(f"Error listing interfaces: {error}")
            ...     return
            ... print(f"Total interfaces found: {len(template_list)}")
            ... for iface in template_list:
            ...     print(iface.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /templates/interfaces/{platform}
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(Common(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_template_names(self) -> APIResult:
        """
        Get Gateway Template Names.

        Returns:
            tuple: A tuple containing (list of Common instances, Response, error).

        Examples:
            List all template interfaces for a platform:

            >>> template_list, _, error = client.ztb.template_router.list_template_interfaces(
            ...     platform="vm"
            ... )
            >>> if error:
            ...     print(f"Error listing template names: {error}")
            ...     return
            ... print(f"Total template names found: {len(template_names)}")
            ... for name in template_names:
            ...     print(name.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztb_base_endpoint}
            /templates/names
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(Common(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
