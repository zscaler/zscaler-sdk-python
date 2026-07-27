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

from typing import List, Optional

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.eun_feature_enablement_status import EunFeatureEnablementStatus
from zscaler.zia.models.eun_template_product import EunTemplateProduct
from zscaler.zia.models.eun_user_confirmation_product import EunUserConfirmationProduct


class EndUserNotificationTemplatesAPI(APIClient):
    """
    A Client object for the End User Notification Templates resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_eun_templates_by_product(
        self, template_type: str, product: str, query_params: Optional[dict] = None
    ) -> APIResult[List[EunTemplateProduct]]:
        """
        Lists the end user notification templates for the specified template type and product (e.g. browser-based or Zscaler Client Connector).

        Args:
            template_type (str): The notification template type (e.g. ``ZCC``, ``BROWSER``).
            product (str): The product the template applies to.
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of EunTemplateProduct instances, Response, error)

        Examples:
            List EUN notification templates:

            >>> template_list, _, error = client.zia.end_user_notification.list_eun_templates_by_product('ZCC', 'ALL')
            >>> if error:
            ...     print(f"Error listing EUN notification templates: {error}")
            ...     return
            ... print(f"Total EUN notification templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /eunTemplate/{template_type}/product/{product}
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
                result.append(EunTemplateProduct(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_eun_feature_enablement_status(
        self, template_type: str, query_params: Optional[dict] = None
    ) -> APIResult[EunFeatureEnablementStatus]:
        """
        Retrieves the end user notification feature enablement status for the specified template type.

        Args:
            template_type (str): The notification template type (e.g. ``ZCC``, ``BROWSER``).
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.product_type]`` {str}: Optional policy type filter (e.g. ``INLINE``, ``ENDPOINT_DLP``).

        Returns:
            tuple: A tuple containing (EunFeatureEnablementStatus instance, Response, error).

        Examples:
            Print a specific EUN notification template:

            >>> fetched_template, _, error = client.zia.end_user_notification.get_eun_feature_enablement_status('ZCC')
            >>> if error:
            ...     print(f"Error fetching EUN notification template: {error}")
            ...     return
            ... print(f"Fetched EUN notification template: {fetched_template.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /eunTemplate/{template_type}/featureEnablementStatus
        """)

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EunFeatureEnablementStatus)
        if error:
            return (None, response, error)

        try:
            result = EunFeatureEnablementStatus(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_user_confirmation_by_policy(
        self, product: str, query_params: Optional[dict] = None
    ) -> APIResult[List[EunUserConfirmationProduct]]:
        """
        Lists the user confirmation notification templates for the specified policy type (INLINE, ENDPOINT_DLP, CLOUDAPP, URL, FILE_TYPE, FIREWALL, DNS, IPS).

        Args:
            product (str): The policy type the confirmation template applies to.
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of EunUserConfirmationProduct instances, Response, error)

        Examples:
            List EUN notification templates:

            >>> template_list, _, error = client.zia.end_user_notification.list_user_confirmation_by_policy('INLINE')
            >>> if error:
            ...     print(f"Error listing EUN notification templates: {error}")
            ...     return
            ... print(f"Total EUN notification templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /userConfirmation/product/{product}
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
                result.append(EunUserConfirmationProduct(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_global_default_templates(
        self, query_params: Optional[dict] = None
    ) -> APIResult[List[EunUserConfirmationProduct]]:
        """
        Lists the global default user confirmation templates for all policy types and channels. Takes no parameters.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of EunUserConfirmationProduct instances, Response, error)

        Examples:
            List EUN notification templates:

            >>> template_list, _, error = client.zia.end_user_notification.list_global_default_templates()
            >>> if error:
            ...     print(f"Error listing EUN notification templates: {error}")
            ...     return
            ... print(f"Total EUN notification templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /userConfirmation/globalDefaultTemplates
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
                result.append(EunUserConfirmationProduct(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_notification_enablement_status(self, template_type: str, query_params: Optional[dict] = None) -> APIResult[dict]:
        """
        Retrieves the user confirmation notification enablement status for the specified template type. User confirmation notifications are supported via Zscaler Client Connector only, so the type is typically ``ZCC``.

        Args:
            template_type (str): The notification template type (e.g. ``ZCC``).
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.product_type]`` {str}: Optional policy type filter (e.g. ``INLINE``, ``ENDPOINT_DLP``).

        Returns:
            tuple: A tuple containing (the raw response value, Response, error).

        Examples:
            >>> result, _, error = client.zia.end_user_notification.get_notification_enablement_status('ZCC')
            >>> if error:
            ...     print(f"Error calling get_notification_enablement_status: {error}")
            ...     return
            ... print(f"Result: {result}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /userConfirmation/{template_type}/featureEnablementStatus
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
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
