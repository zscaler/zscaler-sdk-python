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
from zscaler.ztw.models.location_templates import LocationTemplate
from zscaler.utils import format_url


class LocationTemplateAPI(APIClient):
    """
    A Client object for the Admin and Role resource.
    """

    _ztw_base_endpoint = "/ztw/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_location_templates(self, query_params=None) -> tuple:
        """
        List all existing location templates.

        Args:
            query_params (dict): Map of query parameters for the request.

                ``[query_params.page]`` (int):Specifies the page offset.

                ``[query_params.page_size]`` (int): Specifies the page size. The default size is 250.

        Returns:
            :obj:`Tuple`: The list of location templates.

        Examples:
            List all Provisioning Templates:

            >>> template_list, _, error = client.ztw.location_template.list_location_templates()
            ... if error:
            ...     print(f"Error listing location templates: {error}")
            ...     return
            ... print(f"Total templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())

            Gets a Provisioning Templates by name.

            >>> template_list, _, error = client.ztw.location_template.list_location_templates(query_params={'search': 'Template01'})
            ... if error:
            ...     print(f"Error listing location templates: {error}")
            ...     return
            ... print(f"Total templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /locationTemplate
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
                result.append(LocationTemplate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_template_lite(self, query_params=None) -> tuple:
        """
        Returns only the name and ID of all configured locations.

        Keyword Args:
            query_params {dict}: Optional query parameters.

                ``[query_params.page]`` {int}: Specifies the page offset.

                ``[query_params.page_size]`` {int}: Specifies the page size. The default size is 100.

        Returns:
            :obj:`Tuple`: A list of configured locations.

        Examples:
            List all Provisioning Templates:

            >>> template_list, _, error = client.ztw.location_template.list_template_lite()
            ... if error:
            ...     print(f"Error listing location templates: {error}")
            ...     return
            ... print(f"Total templates found: {len(template_list)}")
            ... for template in template_list:
            ...     print(template.as_dict())

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /locationTemplate/lite
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
                result.append(LocationTemplate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_location_template(self, name: str, template: dict = None, **kwargs) -> tuple:
        """
        Add a new location template.

        Args:
            name (str): The name of the location template.
            template (dict, optional): A dictionary containing the template settings. Possible keys include:

                - ``template_prefix`` (str): Prefix of Cloud & Branch Connector location template.
                - ``xff_forward_enabled`` (bool): Enable to use the X-Forwarded-For headers.
                - ``auth_required`` (bool): Enable if "Authentication Required" is needed.
                - ``caution_enabled`` (bool): Enable to display an end user notification for unauthenticated traffic.
                - ``aup_enabled`` (bool): Enable to display an Acceptable Use Policy (AUP) for unauthenticated traffic.
                - ``aup_timeout_in_days`` (int): Frequency in days for displaying the AUP, if enabled.
                - ``ofw_enabled`` (bool): Enable the service's firewall controls.
                - ``ips_control`` (bool): Enable IPS controls, if firewall is enabled.
                - ``enforce_bandwidth_control`` (bool): Enable to specify bandwidth limits.
                - ``up_bandwidth`` (int): Upload bandwidth in Mbps, if bandwidth control is enabled.
                - ``dn_bandwidth`` (int): Download bandwidth in Mbps, if bandwidth control is enabled.
                - ``display_time_unit`` (str): Time unit for IP Surrogate idle time to disassociation.
                - ``idle_time_in_minutes`` (int): User mapping idle time in minutes for IP Surrogate.
                - ``surrogate_ip_enforced_for_known_browsers`` (bool): Enforce IP Surrogate for all known browsers.
                - ``surrogate_refresh_time_unit`` (str): Time unit for refresh time for re-validation of surrogacy.
                - ``surrogate_refresh_time_in_minutes`` (int): Refresh time in minutes for re-validation of surrogacy.
                - ``surrogate_ip`` (bool): Enable the IP Surrogate feature.

        Keyword Args:
            description (str): The description of the location template.

        Returns:
            :obj:`Tuple`: The location template details.

        Examples:
            Add a new location template with minimal settings::

                >>> added_template, _, error = client.ztw.location_template.add_location_template(
                ...     name=f"NewTemplate_{random.randint(1000, 10000)}",
                ...     description=f"NewTemplate_{random.randint(1000, 10000)}",
                ...     template={
                ...         "template_prefix": f"Template_{random.randint(1000, 10000)}",
                ...         "xff_forward_enabled": True,
                ...         "auth_required": False,
                ...         "caution_enabled": True,
                ...         "ofw_enabled": True
                ...     }
                ... )
                >>> if error:
                ...     print(f"Error adding template: {error}")
                ... else:
                ...     print(f"Template added successfully: {added_template.as_dict()}")
        """
        if "description" in kwargs:
            kwargs["desc"] = kwargs.pop("description")

        if template is not None:
            if isinstance(template, dict):
                tmpl = template
            else:
                tmpl = template.as_dict()
        else:
            tmpl = {}

        # Build the payload by including the required keys
        payload = {"name": name, "template": tmpl}
        # Merge in any additional keyword arguments (only include those with a value)
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /locationTemplate
        """
        )

        request, error = self._request_executor.create_request(
            method=http_method, endpoint=api_url, body=payload, headers={}, params={}
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LocationTemplate)
        if error:
            return (None, response, error)

        try:
            result = LocationTemplate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_location_template(self, template_id: str, **kwargs) -> tuple:
        """
        Update an existing location template.

        Args:
            template_id (str): The ID of the location template to update.

        Keyword Args:
            name (str): The name of the location template.
            description (str): A description for the location template.
            template (dict): A dictionary containing the template settings. Possible keys include:

                - ``template_prefix`` (str): Prefix of Cloud & Branch Connector location template.
                - ``xff_forward_enabled`` (bool): Enable to use the X-Forwarded-For headers.
                - ``auth_required`` (bool): Enable if "Authentication Required" is needed.
                - ``caution_enabled`` (bool): Enable to display an end user notification for unauthenticated traffic.
                - ``aup_enabled`` (bool): Enable to display an Acceptable Use Policy (AUP) for unauthenticated traffic.
                - ``aup_timeout_in_days`` (int): Frequency in days for displaying the AUP, if enabled.
                - ``ofw_enabled`` (bool): Enable the service's firewall controls.
                - ``ips_control`` (bool): Enable IPS controls, if firewall is enabled.
                - ``enforce_bandwidth_control`` (bool): Enable to specify bandwidth limits.
                - ``up_bandwidth`` (int): Upload bandwidth in Mbps, if bandwidth control is enabled.
                - ``dn_bandwidth`` (int): Download bandwidth in Mbps, if bandwidth control is enabled.
                - ``display_time_unit`` (str): Time unit for IP Surrogate idle time to disassociation.
                - ``idle_time_in_minutes`` (int): User mapping idle time in minutes for IP Surrogate.
                - ``surrogate_ip_enforced_for_known_browsers`` (bool): Enforce IP Surrogate for all known browsers.
                - ``surrogate_refresh_time_unit`` (str): Time unit for refresh time for re-validation of surrogacy.
                - ``surrogate_refresh_time_in_minutes`` (int): Refresh time in minutes for re-validation of surrogacy.
                - ``surrogate_ip`` (bool): Enable the IP Surrogate feature.

        Returns:
            :obj:`Tuple`: The updated location template details.

        Note:
            - Any provided keys will update existing keys.
            - The template dictionary does not support partial updates. Any provided template will completely overwrite
              the existing template.

        Examples:
            Update existing location template with minimal settings::

                >>> updated_template, _, error = client.ztw.location_template.add_location_template(
                ...     template_id='12345'
                ...     name=f"UpdateTemplate_{random.randint(1000, 10000)}",
                ...     description=f"UpdateTemplate_{random.randint(1000, 10000)}",
                ...     template={
                ...         "template_prefix": f"Template_{random.randint(1000, 10000)}",
                ...         "xff_forward_enabled": True,
                ...         "auth_required": False,
                ...         "caution_enabled": True,
                ...         "ofw_enabled": True
                ...     }
                ... )
                >>> if error:
                ...     print(f"Error updating template: {error}")
                ... else:
                ...     print(f"Template updated successfully: {updated_template.as_dict()}")
        """
        if "description" in kwargs:
            kwargs["desc"] = kwargs.pop("description")

        if "template" in kwargs:
            if isinstance(kwargs["template"], dict):
                tmpl = kwargs["template"]
            else:
                tmpl = kwargs["template"].as_dict()
            kwargs["template"] = tmpl

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /locationTemplate/{template_id}
        """
        )

        payload = {k: v for k, v in kwargs.items() if v is not None}

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=payload,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, LocationTemplate)
        if error:
            return (None, response, error)

        try:
            result = LocationTemplate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_location_template(self, template_id: str):
        """
        Delete an existing location template.

        Args:
            template_id (str): The ID of the location template to delete.

        Returns:
            :obj:`Tuple`: A tuple containing:
                - `None`: Placeholder for deleted object.
                - `Response`: The response object.
                - `Exception` or `None`: Any error encountered during the operation.

        Examples:
            Delete a location template::

                >>> _, _, error = client.ztw.location_template.delete_location_template(update_template.id)
                >>> if error:
                ...     print(f"Error deleting location template: {error}")
                ... else:
                ...     print(f"Template with ID {update_template.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._ztw_base_endpoint}
            /locationTemplate/{template_id}
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
