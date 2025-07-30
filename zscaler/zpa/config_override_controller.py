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

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.config_override_controller import ConfigOverrideController
from zscaler.utils import format_url


class ConfigOverrideControllerAPI(APIClient):
    """
    A Client object for the Config Override Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_config_overrides(self, query_params=None) -> tuple:
        """
        Returns a list of all config-override details.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            list: A list of `ConfigOverrideController` instances.

        Examples:
            >>> list_details, _, err = client.zpa.config_override_controller.list_config_overrides(
            ... query_params={'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing config override details: {err}")
            ...     return
            ... print(f"Total config override details found: {len(list_details)}")
            ... for override in list_details:
            ...     print(override.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /configOverrides
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ConfigOverrideController)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ConfigOverrideController(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_config_override(
        self,
        config_id: str,
    ) -> tuple:
        """
        Returns information on the specified config-override details by ID.

        Args:
            config_id (str): The unique identifier for the config-override.

        Returns:
            dict: The config-override object.

        Examples:
            >>> fetched_config, _, err = client.zpa.config_override_controller.get_config_override('999999')
            ... if err:
            ...     print(f"Error fetching config override by ID: {err}")
            ...     return
            ... print(f"Fetched config override by ID: {fetched_config.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /configOverrides/{config_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ConfigOverrideController)
        if error:
            return (None, response, error)

        try:
            result = ConfigOverrideController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_config_override(self, **kwargs) -> tuple:
        """
        Adds a new config-override.

        Args:
            name (str): The name of the config-override.
            description (str): The description of the config-override.
            enabled (bool): Enable the config-override. Defaults to True.

        Returns:
            :obj:`Tuple`: ConfigOverrideController: The created config-override object.

        Example:
            Basic example: Add a new config-override

            >>> added_config, _, err = client.zpa.config_override_controller.add_config_override(
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /configOverrides
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ConfigOverrideController)
        if error:
            return (None, response, error)

        try:
            result = ConfigOverrideController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_config_override(self, config_id: str, **kwargs) -> tuple:
        """
        Updates the specified config-override.

        Args:
            config_id (str): The unique identifier for the config-override being updated.

        Returns:
            :obj:`Tuple`: ConfigOverrideController: The updated config-override object.

        Example:
            Basic example: Update an existing config-override

            >>> updated_config, _, err = zpa.config_override_controller.update_config_override(
            ...     config_id='25546',
            ... )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /configOverrides/{config_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, ConfigOverrideController)
        if error:
            return (None, response, error)

        if response is None:
            return (ConfigOverrideController({"id": config_id}), None, None)

        try:
            result = ConfigOverrideController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
