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
from zscaler.ztb.models.site import (
    Site,
    SiteUpdateBody,
    AppSegment,
    CloudSiteCreateBody,
    HostnameConfig,
    SiteNameItem,
    SiteOverview,
    StaticIpMappingBody,
)


class SiteAPI(APIClient):
    """
    Client for the ZTB Site resource.

    Provides CRUD and utility operations for sites in the Zero Trust Branch API.
    Endpoints under ``/api/v2/Site/``.
    """

    _ztb_base_endpoint = "/ztb/api/v2"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_sites(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get list of sites with pagination and search.

        Args:
            query_params (dict, optional): Map of query parameters.
                ``[query_params.search]`` (str): Search filter.
                ``[query_params.page]`` (int): Page number.
                ``[query_params.limit]`` (int): Page size.
                ``[query_params.sort]`` (str): Sort field.
                ``[query_params.sortdir]`` (str): asc or desc.
                ``[query_params.siteId]`` (str): Site ID filter.
                ``[query_params.gatewayType]`` (str): Gateway type filter.

        Returns:
            tuple: (list of Site instances, Response, error).

        Examples:
            >>> sites, _, err = client.ztb.site.list_sites()
            >>> sites, _, err = client.ztb.site.list_sites(
            ...     query_params={"search": "prod", "page": 1, "limit": 25}
            ... )

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/
        """)
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
                result.append(Site(self.form_response_body(item)))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_site_by_id(self, site_id: str) -> APIResult:
        """
        Get site by ID.

        Args:
            site_id (str): The site ID.

        Returns:
            tuple: (Site instance, Response, error).
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/siteByID/{site_id}
        """)
        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = Site(self.form_response_body(payload))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_site_by_name(self, name: str) -> APIResult:
        """
        Get site by name.

        Args:
            name (str): The site name.

        Returns:
            tuple: (Site instance, Response, error).
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/siteByName/{name}
        """)
        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = Site(self.form_response_body(payload))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def create_site(self, **kwargs) -> APIResult:
        """
        Create a new site.

        Args:
            **kwargs: Site fields (e.g. name, display_name, deployment_type, etc).

        Returns:
            tuple: (created Site or None, Response, error).
        """
        http_method = "POST"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/
        """)
        body = kwargs
        request, error = self._request_executor.create_request(
            http_method, api_url, body, {"Content-Type": "application/json"}
        )
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body()
            result = Site(self.form_response_body(payload)) if payload else None
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def update_site(self, site_id: str, body: Optional[SiteUpdateBody] = None, **kwargs) -> APIResult:
        """
        Update a site.

        Args:
            site_id (str): The site ID.
            body (SiteUpdateBody, optional): Update payload.
            **kwargs: Override body fields.

        Returns:
            tuple: (None or updated Site, Response, error).
        """
        http_method = "PUT"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/{site_id}
        """)
        if body:
            req_body = body.request_format()
        else:
            req_body = {}
        req_body.update(kwargs)
        request, error = self._request_executor.create_request(
            http_method, api_url, req_body, {"Content-Type": "application/json"}
        )
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def delete_site(self, site_id: str) -> APIResult:
        """
        Delete a site.

        Args:
            site_id (str): The site ID.

        Returns:
            tuple: (None, Response, error).
        """
        http_method = "DELETE"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/{site_id}
        """)
        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_md5(self) -> APIResult:
        """
        Get Gateway MD5.

        Returns:
            tuple: (result string, Response, error).
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/MD5
        """)
        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = payload.get("result") if isinstance(payload.get("result"), str) else None
        except Exception:
            result = None
        return (result, response, None)

    def list_app_segments(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get list of ZPA app segments with pagination.

        Args:
            query_params (dict, optional): page, limit, search.

        Returns:
            tuple: (list of AppSegment, Response, error).

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/app_segments
        """)
        query_params = query_params or {}
        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            result = []
            for item in response.get_results():
                result.append(AppSegment(self.form_response_body(item)))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def update_app_segments(self, site_id: str) -> APIResult:
        """
        Update ZPA app segments for a site.

        Args:
            site_id (str): The site ID.

        Returns:
            tuple: (None, Response, error).
        """
        http_method = "POST"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/app_segments/{site_id}
        """)
        request, error = self._request_executor.create_request(http_method, api_url, {}, {"Content-Type": "application/json"})
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def create_cloud_site(self, body: Optional[CloudSiteCreateBody] = None, **kwargs) -> APIResult:
        """
        Create a cloud gateway site.

        Args:
            body (CloudSiteCreateBody, optional): Create payload.
            **kwargs: Override body fields.

        Returns:
            tuple: (response data or None, Response, error).
        """
        http_method = "POST"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/cloudSite/
        """)
        req_body = (body.request_format() if body else {}) | kwargs
        request, error = self._request_executor.create_request(
            http_method, api_url, req_body, {"Content-Type": "application/json"}
        )
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def get_hostname_config(
        self,
        gateway_ipaddress: str,
        site_name: str,
        query_params: Optional[dict] = None,
    ) -> APIResult:
        """
        Get hostname config.

        Args:
            gateway_ipaddress (str): Gateway IP address.
            site_name (str): Site name.
            query_params (dict, optional): Additional query params.

        Returns:
            tuple: (HostnameConfig instance, Response, error).
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/hostnameconfig
        """)
        params = dict(query_params) if query_params else {}
        params["gateway_ipaddress"] = gateway_ipaddress
        params["site_name"] = site_name
        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, params=params)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = HostnameConfig(self.form_response_body(payload))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def list_site_names(self, query_params: Optional[dict] = None) -> APIResult:
        """
        Get all site names.

        Args:
            query_params (dict, optional): siteId, gatewayType, full.

        Returns:
            tuple: (list of SiteNameItem, Response, error).

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.

        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/names
        """)
        query_params = query_params or {}
        request, error = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            raw = payload.get("result") or []
            result = [SiteNameItem(self.form_response_body(item)) for item in raw]
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def get_site_overview(self, site_id: str) -> APIResult:
        """
        Get site overview data.

        Args:
            site_id (str): The site ID.

        Returns:
            tuple: (SiteOverview instance, Response, error).
        """
        http_method = "GET"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/siteByID/{site_id}/overview
        """)
        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        try:
            payload = response.get_body() or {}
            result = SiteOverview(self.form_response_body(payload))
        except Exception as err:
            return (None, response, err)
        return (result, response, None)

    def update_static_ips_mapping(self, site_id: str, enabled: bool) -> APIResult:
        """
        Update app segment static IP mapping for a site.

        Args:
            site_id (str): The site ID.
            enabled (bool): Whether to enable static IP mapping.

        Returns:
            tuple: (None, Response, error).
        """
        http_method = "PUT"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/{site_id}/static_ips_mapping
        """)
        body = {"enabled": enabled}
        request, error = self._request_executor.create_request(
            http_method, api_url, body, {"Content-Type": "application/json"}
        )
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def update_site_template(self, site_id: str, template_id: str) -> APIResult:
        """
        Change template for a site.

        Args:
            site_id (str): The site ID.
            template_id (str): The template ID.

        Returns:
            tuple: (None, Response, error).
        """
        http_method = "PUT"
        api_url = format_url(f"""
            {self._ztb_base_endpoint}
            /Site/{site_id}/template/{template_id}
        """)
        request, error = self._request_executor.create_request(http_method, api_url, {}, {})
        if error:
            return (None, None, error)
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
