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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zia.models.dlp_templates import DLPTemplates
from zscaler.utils import format_url


class DLPTemplatesAPI(APIClient):
    """
    A Client object for the DLP Templates resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_dlp_templates(
        self,
        query_params: Optional[dict] = None,
    ) -> List[DLPTemplates]:
        """
        Lists DLP Notification Templates. in your organization.
        If the `search` parameter is provided, the function filters the rules client-side.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:

        Examples:
            Print all dlp templates

            >>> template_list, response, error = client.zia.dlp_templates.list_dlp_templates()
            ... if error:
            ...     print(f"Error listing templates: {error}")
            ...     return
            ... print(f"Total templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())

            Print templates that match the name 'Standard_Template'

            >>> template_list, response, error = client.zia.dlp_templates.list_dlp_templates(
                query_params={"search": 'Standard_Template'})
            ... if error:
            ...     print(f"Error listing templates: {error}")
            ...     return
            ... print(f"Total templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpNotificationTemplates
        """
        )

        query_params = query_params or {}

        local_search = query_params.pop("search", None)

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        response = self._request_executor.execute(request)
        results = []
        for item in response.get_results():
            results.append(DLPTemplates(self.form_response_body(item)))
        if local_search:
            lower_search = local_search.lower()
            results = [r for r in results if lower_search in (r.name.lower() if r.name else "")]

        return results

    def get_dlp_templates(self, template_id: int) -> DLPTemplates:
        """
        Returns the dlp notification template details for a given DLP template.

        Args:
            template_id (int): The unique identifer for the DLP notification template.

        Returns:
            :obj:`Tuple`: The DLP template resource record.

        Examples:
            >>> fetched_template, response, error = client.zia.dlp_templates.get_dlp_templates('63578')
            ... if error:
            ...     print(f"Error fetching Template by ID: {error}")
            ...     return
            ... print(f"Fetched Template by ID: {fetched_template.as_dict()}")

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpNotificationTemplates/{template_id}
        """
        )

        body = {}
        headers = {}

        # Create the request
        request = self._request_executor.create_request(http_method, api_url, body, headers)

        # Execute the request
        response = self._request_executor.execute(request, DLPTemplates)
        result = DLPTemplates(self.form_response_body(response.get_body()))
        return result

    def add_dlp_template(self, **kwargs) -> DLPTemplates:
        """
        Adds a new DLP notification template to ZIA.

        Args:
            name (str): The name of the DLP notification template.
            subject (str): The subject line displayed within the DLP notification email.

        Keyword Args:
            attach_content (bool): If true, the content in violation is attached to the DLP notification email.
            plain_text_message (str): Template for the plain text UTF-8 message body displayed in the DLP notification email.
            html_message (str): Template for the HTML message body displayed in the DLP notification email.
            tls_enabled (bool): If true, enables TLS for the notification template.

        Returns:
            :obj:`Tuple`: The newly created DLP Notification Template resource record.

        Examples:
            Create a new DLP Notification Template:

            >>> zia.dlp.add_dlp_template(name="New DLP Template",
            ...                         subject="Alert: DLP Violation Detected",
            ...                         attach_content=True,
            ...                         plain_text_message="Text message content",
            ...                         html_message="<html><body>HTML message content</body></html>")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpNotificationTemplates
        """
        )

        body = kwargs

        request = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        response = self._request_executor.execute(request, DLPTemplates)
        result = DLPTemplates(self.form_response_body(response.get_body()))
        return result

    def update_dlp_template(self, template_id: str, **kwargs) -> DLPTemplates:
        """
        Updates the specified DLP Notification Template.

        Args:
            template_id (str): The unique identifier for the DLP notification template.

        Keyword Args:
            name (str): The new name of the DLP notification template.
            subject (str): The new subject line for the DLP notification email.
            attach_content (bool): If true, updates the setting for attaching content in violation.
            plain_text_message (str): New template for the plain text UTF-8 message body.
            html_message (str): New template for the HTML message body.
            tls_enabled (bool): If true, enables TLS for the notification template.

        Returns:

        Examples:
            Create a new DLP Notification Template:

            >>> zia.dlp.add_dlp_template('63578'
            ...                         name="New DLP Template",
            ...                         subject="Alert: DLP Violation Detected",
            ...                         attach_content=True,
            ...                         plain_text_message="Text message content",
            ...                         html_message="<html><body>HTML message content</body></html>")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpNotificationTemplates/{template_id}
        """
        )

        body = {}

        body.update(kwargs)

        request = self._request_executor.create_request(http_method, api_url, body, {}, {})
        response = self._request_executor.execute(request, DLPTemplates)
        result = DLPTemplates(self.form_response_body(response.get_body()))
        return result

    def delete_dlp_template(self, template_id: str) -> None:
        """
        Deletes the DLP Notification Template that matches the specified Template id.

        Args:
            template_id (str): The unique id for the DLP Notification Template.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> _, response, error = client.zia.dlp_templates.delete_dlp_template('63578')
            ... if error:
            ...     print(f"Error deleting Template: {error}")
            ...     return
            ...print(f"Template with ID {'63578'} deleted successfully.")

        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /dlpNotificationTemplates/{template_id}
        """
        )

        params = {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        response = self._request_executor.execute(request)
        return None
