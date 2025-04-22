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
from zscaler.zpa.models.app_protection import InspectionProfile
from zscaler.zpa.models.app_protection import AppProtectionCustomControl
from zscaler.zpa.models.app_protection_predefined_controls import PredefinedInspectionControlResource
from zscaler.utils import format_url
from requests.utils import quote


class InspectionControllerAPI(APIClient):
    """
    A client object for the ZPA Inspection Profiles resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    @staticmethod
    def _create_rule(rule: dict) -> dict:
        if not isinstance(rule, dict):
            raise TypeError(f"Expected rule to be a dictionary, got {type(rule).__name__}: {rule}")

        rule_set = {
            "type": rule["type"],
            "conditions": [],
        }
        if "names" in rule:
            rule_set["names"] = rule["names"]
        for condition in rule["conditions"]:
            rule_set["conditions"].append(
                {
                    "lhs": condition["lhs"],
                    "op": condition["op"],
                    "rhs": condition["rhs"],
                }
            )
        return rule_set

    def list_profiles(
        self,
        query_params=None,
    ) -> tuple:
        """
        Enumerates App Protection Profile in your organization with pagination.
        A subset of App Protection Profile can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            tuple: A tuple containing (list of InspectionProfile instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionProfile
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(InspectionProfile(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_profile(self, profile_id: str, **kwargs) -> tuple:
        """
        Gets information on the specified inspection profile.

        Args:
            profile_id (str): The unique identifier for the inspection profile.

        Returns:
            InspectionProfile: The corresponding inspection profile object.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionProfile/{profile_id}
            """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {}, kwargs)
        if error:
            return None

        response, error = self._request_executor.execute(request, InspectionProfile)
        if error:
            return (None, response, error)

        try:
            result = InspectionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_profile(self, **kwargs) -> tuple:
        """
        Create a new inspection profile.

        Args:
            name (str):
                The name of the inspection profile.

            description (str):
                The description of the inspection profile.

            check_control_deployment_status (bool):
                Indicates whether or not the service needs to perform additional validations.

            paranoia_level (str):
                The OWASP Predefined Paranoia Level.

            incarnation_number (str):
                A version or incarnation marker for the inspection profile.

            global_control_actions (list):
                The actions of the predefined, custom, or override controls.

            predefined_controls_version (list):
                The protocol for the AppProtection application.

            zs_defined_control_choice (str):
                Indicates the user's choice for the ThreatLabZ Controls.

                Supported values:
                - ``ALL``: Zscaler handles the ThreatLabZ Controls for the AppProtection profile.
                - ``SPECIFIC``: User handles the ThreatLabZ Controls for the AppProtection profile.

            custom_controls (list):
                The set of AppProtection controls used to define how inspections are managed.

                Each control item may include:
                - **action** (str):
                Action of the custom control. Supported values: ``PASS``, ``BLOCK``, or ``REDIRECT``.
                - **action_value** (str):
                The value for the defined control's action; only required if the action is ``REDIRECT``.
                - **default_action_value** (str):
                The redirect URL if the default action is set to ``REDIRECT``.

            controls_info (list):
                A list of server group IDs for the control set.

                Each item may include:
                - **control_type** (str):
                The control type. Supported values: ``WEBSOCKET_PREDEFINED``, ``WEBSOCKET_CUSTOM``,
                ``THREATLABZ``, ``CUSTOM``, ``PREDEFINED``.
                - **count** (int):
                The count of controls in this set.

            threat_labz_controls (list):
                The ThreatLabZ predefined controls.

                Each item may include:
                - **action** (str):
                Supported values: ``PASS``, ``BLOCK``, or ``REDIRECT``.
                - **action_value** (str):
                Required only if the action is ``REDIRECT``.
                - **default_action_value** (str):
                Redirect URL if the default action is ``REDIRECT``.

            websocket_controls (list):
                The WebSocket controls.

                Each item may include:
                - **action** (str):
                Supported values: ``PASS``, ``BLOCK``, or ``REDIRECT``.
                - **action_value** (str):
                Required only if the action is ``REDIRECT``.
                - **default_action_value** (str):
                Redirect URL if the default action is ``REDIRECT``.

        Returns:
            tuple:
                A tuple containing the `InspectionProfile` instance, the response object, and an error (if any).
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionProfile
        """
        )

        # Fetch all predefined control groups
        control_groups, _, err = self.list_predef_controls()
        if err or not control_groups:
            return (None, None, f"Failed to retrieve predefined control groups: {err}")

        # Aggregate controls from all groups marked as `defaultGroup`
        predefined_controls = []
        for group in control_groups:
            if isinstance(group, PredefinedInspectionControlResource) and group.default_group:
                for control in group.predefined_inspection_controls:
                    predefined_controls.append(
                        {
                            "id": control["id"],
                            "action": control["defaultAction"],
                            "default_action": control["defaultAction"],
                        }
                    )

        # Debugging: Ensure predefined_controls is populated
        if not predefined_controls:
            return (None, None, "Default predefined controls are missing or empty.")

        # Construct the payload starting with predefined controls and predefinedControlsVersion
        payload = {
            "predefinedControls": predefined_controls,
            "predefinedControlsVersion": "OWASP_CRS/3.3.0",
        }

        # Add predefined controls if provided
        if kwargs.get("predef_controls"):
            predef_controls = kwargs.pop("predef_controls")
            payload["predefinedControls"].extend(
                [{"id": control[0], "action": control[1], "default_action": control[1]} for control in predef_controls]
            )

        # Add custom controls if provided
        if kwargs.get("custom_controls"):
            custom_controls = kwargs.pop("custom_controls")
            payload["customControls"] = [{"id": control[0], "action": control[1]} for control in custom_controls]

        # Add additional parameters
        payload.update(kwargs)

        # Debugging: Log the payload before sending the request
        print("Payload being sent:", payload)

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body=payload, headers={}, params={})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, InspectionProfile)
        if error:
            return (None, response, error)

        try:
            result = InspectionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_profile(self, profile_id: str, **kwargs) -> tuple:
        """
        Updates the specified inspection profile.

        Args:
            profile_id (str): The unique ID of the profile to be updated.

        Returns:
            InspectionProfile: The updated inspection profile object.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionProfile/{profile_id}
        """
        )

        # Fetch all predefined control groups
        control_groups, _, err = self.list_predef_controls()
        if err or not control_groups:
            return (None, None, f"Failed to retrieve predefined control groups: {err}")

        # Aggregate controls from all groups marked as `defaultGroup`
        predefined_controls = []
        for group in control_groups:
            if isinstance(group, PredefinedInspectionControlResource) and group.default_group:
                for control in group.predefined_inspection_controls:
                    predefined_controls.append(
                        {
                            "id": control["id"],
                            "action": control["defaultAction"],
                            "default_action": control["defaultAction"],
                        }
                    )

        # Debugging: Ensure predefined_controls is populated
        if not predefined_controls:
            return (None, None, "Default predefined controls are missing or empty.")

        # Construct the payload starting with predefined controls and predefinedControlsVersion
        payload = {
            "predefinedControls": predefined_controls,
            "predefinedControlsVersion": "OWASP_CRS/3.3.0",
        }

        # Add predefined controls if provided
        if kwargs.get("predef_controls"):
            predef_controls = kwargs.pop("predef_controls")
            payload["predefinedControls"].extend(
                [{"id": control[0], "action": control[1], "default_action": control[1]} for control in predef_controls]
            )

        # Add custom controls if provided
        if kwargs.get("custom_controls"):
            custom_controls = kwargs.pop("custom_controls")
            payload["customControls"] = [{"id": control[0], "action": control[1]} for control in custom_controls]

        # Add additional parameters
        payload.update(kwargs)

        # Debugging: Log the payload before sending the request
        print("Payload being sent:", payload)

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, headers={}, params={})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, InspectionProfile)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            return (InspectionProfile({"id": profile_id}), None, None)

        # Parse the response into an InspectionProfile instance
        try:
            result = InspectionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_profile(self, profile_id: str) -> int:
        """
        Deletes the specified inspection profile.

        Args:
            profile_id (str): The unique identifier for the inspection profile to be deleted.

        Returns:
            int: Status code of the delete operation.
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionProfile/{profile_id}
        """
        )

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)

    def profile_control_attach(self, profile_id: str, action: str, **kwargs) -> tuple:
        """
        Attaches or detaches all predefined ZPA Inspection Controls to a ZPA Inspection Profile.

        Args:
            profile_id (str): The unique ID for the ZPA Inspection Profile that will be modified.
            action (str): The association action that will be taken, accepted values are:
                * ``attach``: Attaches all predefined controls to the Inspection Profile with the specified version.
                * ``detach``: Detaches all predefined controls from the Inspection Profile.
            **kwargs: Additional keyword arguments.

        Keyword Args:
            profile_version (str): The version of the Predefined Controls to attach. Only required when using the
                attach action. Defaults to ``OWASP_CRS/3.3.0``.

        Returns:
            InspectionProfile: The updated ZPA Inspection Profile resource record.
        """
        http_method = "put".upper()
        if action == "attach":
            api_url = format_url(f"{self._zpa_base_endpoint}/inspectionProfile/{profile_id}/associateAllPredefinedControls")
            payload = {"version": kwargs.pop("profile_version", "OWASP_CRS/3.3.0")}
        elif action == "detach":
            api_url = format_url(f"{self._zpa_base_endpoint}/inspectionProfile/{profile_id}/deAssociateAllPredefinedControls")
            payload = {}
        else:
            raise ValueError("Unknown action provided. Valid actions are 'attach' or 'detach'.")

        request, error = self._request_executor.create_request(http_method, api_url, payload)
        if error:
            return None

        # Execute the request
        response, error = self._request_executor.execute(request, InspectionProfile)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            return (InspectionProfile({"id": profile_id}), None, None)

        try:
            result = InspectionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_profile_and_controls(self, profile_id: str, **kwargs) -> tuple:
        """
        Updates the inspection profile and controls for the specified ID.

        Args:
            profile_id (str): The unique ID of the inspection profile.
            inspection_profile (dict): The new inspection profile object.
            **kwargs: Additional keyword arguments.

        Returns:
            InspectionProfile: The updated ZPA Inspection Profile resource record.
        """
        http_method = "patch".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionProfile/{profile_id}/patch
        """
        )

        # Fetch all predefined control groups
        control_groups, _, err = self.list_predef_controls()
        if err or not control_groups:
            return (None, None, f"Failed to retrieve predefined control groups: {err}")

        # Aggregate controls from all groups marked as `defaultGroup`
        predefined_controls = []
        for group in control_groups:
            if isinstance(group, PredefinedInspectionControlResource) and group.default_group:
                for control in group.predefined_inspection_controls:
                    predefined_controls.append(
                        {
                            "id": control["id"],
                            "action": control["defaultAction"],
                            "default_action": control["defaultAction"],
                        }
                    )

        # Debugging: Ensure predefined_controls is populated
        if not predefined_controls:
            return (None, None, "Default predefined controls are missing or empty.")

        # Construct the payload starting with predefined controls and predefinedControlsVersion
        payload = {
            "predefinedControls": predefined_controls,
            "predefinedControlsVersion": "OWASP_CRS/3.3.0",
        }

        # Add predefined controls if provided
        if kwargs.get("predef_controls"):
            predef_controls = kwargs.pop("predef_controls")
            payload["predefinedControls"].extend(
                [{"id": control[0], "action": control[1], "default_action": control[1]} for control in predef_controls]
            )

        # Add custom controls if provided
        if kwargs.get("custom_controls"):
            custom_controls = kwargs.pop("custom_controls")
            payload["customControls"] = [{"id": control[0], "action": control[1]} for control in custom_controls]

        # Add additional parameters
        payload.update(kwargs)

        # Debugging: Log the payload before sending the request
        print("Payload being sent:", payload)

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body=payload, headers={}, params={})
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, InspectionProfile)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            return (InspectionProfile({"id": profile_id}), None, None)

        # Parse the response into an InspectionProfile instance
        try:
            result = InspectionProfile(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_custom_controls(
        self,
        query_params=None,
    ) -> tuple:
        """
        Enumerates App Protection Custom Control in your organization with pagination.
        A subset of App Protection Custom Control can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {int}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.

                ``[query_params.sort_dir]`` {str}: Specifies the sorting order (ascending/descending) for the search results.
                    Available values : ASC, DESC

        Returns:
            tuple: A tuple containing (list of AppProtectionCustomControl instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/custom
        """
        )

        query_params = query_params or {}

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(AppProtectionCustomControl(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_predef_control(self, control_id: str) -> tuple:
        """
        Returns the specified predefined ZPA Inspection Control.

        Args:
            control_id (str): The unique ID of the predefined control.

        Returns:
            AppProtectionCustomControl: The corresponding predefined control object.
        """
        http_method = "get".upper()
        api_url = format_url(
            f""""
            {self._zpa_base_endpoint}
            /inspectionControls/predefined/{control_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {})
        if error:
            return None

        response, error = self._request_executor.execute(request, PredefinedInspectionControlResource)
        if error:
            return (None, response, error)

        try:
            result = PredefinedInspectionControlResource(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_custom_control(self, control_id: str) -> tuple:
        """
        Returns the specified custom ZPA Inspection Control.

        Args:
            control_id (str): The unique ID of the custom control.

        Returns:
            AppProtectionCustomControl: The corresponding custom control object.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}/inspectionControls/custom/{control_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {})
        if error:
            return None

        response, error = self._request_executor.execute(request, AppProtectionCustomControl)
        if error:
            return (None, response, error)

        try:
            result = AppProtectionCustomControl(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_custom_control(self, **kwargs) -> tuple:
        """
        Adds a new ZPA Inspection Custom Control.

        Args:
            kwargs (dict): A dictionary of attributes to create the custom control.

        Returns:
            AppProtectionCustomControl: The newly created custom control object.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}/inspectionControls/custom
        """
        )

        # Extract rules from kwargs
        rules = kwargs.pop("rules", [])
        kwargs["rules"] = [self._create_rule(rule) for rule in rules]

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, kwargs)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, AppProtectionCustomControl)
        if error:
            return (None, response, error)

        try:
            result = AppProtectionCustomControl(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_custom_control(self, control_id: str, **kwargs) -> tuple:
        """
        Updates the specified custom ZPA Inspection Control.

        Args:
            control_id (str): The unique ID of the custom control.
            kwargs (dict): A dictionary of attributes to update the custom control.

        Returns:
            AppProtectionCustomControl: The updated custom control object.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/custom/{control_id}
        """
        )

        # Fetch existing control and handle errors
        existing_control, _, err = self.get_custom_control(control_id)
        if err or not existing_control:
            return (None, None, f"Failed to retrieve custom control with ID {control_id}: {err}")

        # Prepare the payload using the existing control
        payload = existing_control.request_format()

        # Update rules if provided
        if "rules" in kwargs:
            rules = kwargs.pop("rules")
            payload["rules"] = [self._create_rule(rule) for rule in rules]

        # Add other attributes from kwargs
        payload.update(kwargs)

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, payload)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, AppProtectionCustomControl)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            return (AppProtectionCustomControl({"id": control_id}), None, None)

        try:
            result = AppProtectionCustomControl(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_custom_control(self, control_id: str) -> int:
        """
        Deletes the specified custom ZPA Inspection Control.

        Args:
            control_id (str): The unique ID for the custom control.

        Returns:
            int: The status code for the operation.
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/custom/{control_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url, {})
        if error:
            return None

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)

    def list_predef_controls(self, query_params=None) -> tuple:
        """
        Returns a list of predefined ZPA Inspection Controls.

        Args:
            query_params (dict):
                Additional query parameters for the request.

                Includes:
                    - ``search`` (str): The field name to search for.
                    - ``search_field`` (str): The value to search for within the field.

        Returns:
            tuple:
                A tuple containing (list of PredefinedInspectionControl objects, Response, error).

        Examples:
            >>> for control in zpa.inspection.list_predef_controls():
            ...     print(control)

            >>> for control in zpa.inspection.list_predef_controls(
            ...         query_params={"search": "controlGroup", "search_field": "Protocol Issues"}):
            ...     print(control)
        """
        http_method = "get".upper()
        encoded_version = quote("OWASP_CRS/3.3.0", safe="")
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/predefined?version={encoded_version}
        """
        )

        # Handle query parameters
        query_params = query_params or {}
        search_field = query_params.pop("search_field", None)
        if "search" in query_params and search_field:
            # Construct the search query: field +EQ+ value
            query_params["search"] = f"{query_params['search']}+EQ+{search_field}"

        # Add additional query parameters to the URL
        if query_params:
            additional_params = "&".join(f"{key}={quote(str(value))}" for key, value in query_params.items())
            api_url = f"{api_url}&{additional_params}"

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [PredefinedInspectionControlResource(self.form_response_body(item)) for item in response.get_results()]
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_control_action_types(self) -> tuple:
        """
        Returns a list of ZPA Inspection Control Action Types.

        Returns:
            tuple: A tuple containing (list of action types, Response, error).

        Examples:
            >>> for action_type in zpa.inspection.list_control_action_types():
            ...     print(action_type)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/actionTypes
        """
        )

        body = {}
        headers = {}
        form = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, form)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, str)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_control_severity_types(self) -> tuple:
        """
        Returns a list of Inspection Control Severity Types.

        Returns:
            tuple: A dictionary containing all valid Inspection Control Severity Types.

        Examples:
            >>> for severity in zpa.inspection.list_control_severity_types():
            ...     print(severity)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/severityTypes
        """
        )

        body = {}
        headers = {}
        form = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, form)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, str)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_control_types(self) -> tuple:
        """
        Returns a list of ZPA Inspection Control Types.

        Returns:
            tuple: A dictionary containing ZPA Inspection Control Types.

        Examples:
            >>> for control_type in zpa.inspection.list_control_types():
            ...     print(control_type)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/controlTypes
        """
        )

        body = {}
        headers = {}
        form = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, form)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, str)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_custom_http_methods(self) -> tuple:
        """
        Returns a list of custom ZPA Inspection Control HTTP Methods.

        Returns:
            tuple: A dictionary containing custom ZPA Inspection Control HTTP Methods.

        Examples:
            >>> for method in zpa.inspection.list_custom_http_methods():
            ...     print(method)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/custom/httpMethods
        """
        )

        body = {}
        headers = {}
        form = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, form)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, str)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_predef_control_versions(self) -> tuple:
        """
        Returns a list of predefined ZPA Inspection Control versions.

        Returns:
            tuple: A dictionary containing all predefined ZPA Inspection Control versions.

        Examples:
            >>> for version in zpa.inspection.list_predef_control_versions():
            ...     print(version)

        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/predefined/versions
        """
        )

        body = {}
        headers = {}
        form = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, form)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, str)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def list_predef_control_adp(self, query_params=None) -> tuple:
        """
        Returns all predefined ADP inspection controls for the specified customer.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            AppProtectionCustomControl: The corresponding predefined control object.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/predefined/adp
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
                result.append(PredefinedInspectionControlResource(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_predef_control_api(self, query_params=None) -> tuple:
        """
        Returns all predefined inspection controls for the specified customer.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            AppProtectionCustomControl: The corresponding predefined control object.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /inspectionControls/predefined/api
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
                result.append(PredefinedInspectionControlResource(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
