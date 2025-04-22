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
from zscaler.zpa.models.policyset_controller_v1 import PolicySetControllerV1
from zscaler.zpa.models.policyset_controller_v2 import PolicySetControllerV2
from zscaler.utils import format_url, add_id_groups
from threading import Lock
from functools import wraps

# Define a global lock
global_rule_lock = Lock()


def synchronized(lock):
    """Decorator to ensure that a function is executed with a lock."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorator


class PolicySetControllerAPI(APIClient):
    """
    A client object for the Policy Set Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint_v1 = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    # Mapping policy types to their ZPA API equivalents
    POLICY_MAP = {
        "access": "ACCESS_POLICY",
        "capabilities": "CAPABILITIES_POLICY",
        "client_forwarding": "CLIENT_FORWARDING_POLICY",
        "clientless": "CLIENTLESS_SESSION_PROTECTION_POLICY",
        "credential": "CREDENTIAL_POLICY",
        "portal_policy": "PRIVILEGED_PORTAL_POLICY",
        "vpn_policy": "VPN_TUNNEL_POLICY",
        "inspection": "INSPECTION_POLICY",
        "isolation": "ISOLATION_POLICY",
        "redirection": "REDIRECTION_POLICY",
        "siem": "SIEM_POLICY",
        "timeout": "TIMEOUT_POLICY",
    }

    reformat_params = [
        ("app_server_group_ids", "appServerGroups"),
        ("app_connector_group_ids", "PolicySetControllers"),
        ("service_edge_group_ids", "serviceEdgeGroups"),
    ]

    @staticmethod
    def _create_conditions_v1(conditions: list) -> list:
        """
        Creates a dict template for feeding conditions into the ZPA Policies API when adding or updating a policy.

        Args:
            conditions (list): List of condition dicts or tuples.

        Returns:
            :obj:`list`: The conditions template.

        """
        template = []
        app_and_app_group_operands = []
        scim_and_scim_group_operands = []
        object_types_to_operands = {
            "CONSOLE": [],
            "MACHINE_GRP": [],
            "LOCATION": [],
            "BRANCH_CONNECTOR_GROUP": [],
            "EDGE_CONNECTOR_GROUP": [],
            "CLIENT_TYPE": [],
            "IDP": [],
            "PLATFORM": [],
            "POSTURE": [],
            "TRUSTED_NETWORK": [],
            "SAML": [],
            "SCIM": [],
            "SCIM_GROUP": [],
            "COUNTRY_CODE": [],
            "RISK_FACTOR_TYPE": [],
            "CHROME_ENTERPRISE": [],
        }

        operators_for_types = {}  # Dictionary to store specific operators for each object type

        for condition in conditions:
            # Check if the first item in a tuple is an operator, like "AND" or "OR"
            if isinstance(condition, tuple) and isinstance(condition[0], str) and condition[0].upper() in ["AND", "OR"]:
                operator = condition[0].upper()
                condition = condition[1]  # The second element is the actual condition
            else:
                operator = "OR"  # Default operator if none specified

            # Process each condition and categorize by object type and operator
            if isinstance(condition, tuple) and len(condition) == 3:
                object_type = condition[0].upper()
                lhs = condition[1]
                rhs = condition[2]
                operand = {"objectType": object_type, "lhs": lhs, "rhs": rhs}

                # Track the operator for the current object type
                operators_for_types[object_type] = operator

                if object_type in ["APP", "APP_GROUP"]:
                    app_and_app_group_operands.append(operand)
                elif object_type in ["SCIM", "SCIM_GROUP"]:
                    scim_and_scim_group_operands.append(operand)
                elif object_type in object_types_to_operands:
                    object_types_to_operands[object_type].append(operand)

            elif isinstance(condition, dict):

                condition_template = {}
                for key in ["id", "negated", "operator"]:
                    if key in condition:
                        condition_template[key] = condition[key]

                operands = condition.get("operands", [])
                condition_template["operands"] = []

                for operand in operands:
                    operand_template = {}
                    for operand_key in ["id", "idp_id", "name", "lhs", "rhs", "objectType"]:
                        if operand_key in operand:
                            operand_template[operand_key] = operand[operand_key]

                    condition_template["operands"].append(operand_template)

                template.append(condition_template)

        # Combine APP and APP_GROUP operands with their specific operator
        if app_and_app_group_operands:
            app_group_operator = operators_for_types.get("APP", "OR")
            template.append({"operator": app_group_operator, "operands": app_and_app_group_operands})

        # Combine SCIM and SCIM_GROUP operands with their specific operator
        if scim_and_scim_group_operands:
            scim_group_operator = operators_for_types.get("SCIM_GROUP", "OR")
            template.append({"operator": scim_group_operator, "operands": scim_and_scim_group_operands})

        # Combine other object types into their blocks with their respective operator
        for object_type, operands in object_types_to_operands.items():
            if operands:
                operator = operators_for_types.get(object_type, "OR")
                template.append({"operator": operator, "operands": operands})

        return template

    def _create_conditions_v2(self, conditions: list) -> list:
        """
        Creates a dict template for feeding conditions into the ZPA Policies API when adding or updating a policy.

        Args:
            conditions (list): List of condition tuples where each tuple represents a specific policy condition.

        Returns:
            :obj:`list`: List containing the conditions formatted for the ZPA Policies API.
        """

        grouped_conditions = {"app_and_app_group": []}  # Specific group for APP and APP_GROUP
        template = []

        for condition in conditions:
            object_type, values = condition[0], condition[1]

            if object_type in ["app", "app_group"]:
                # Group APP and APP_GROUP together in the same operands block
                grouped_conditions["app_and_app_group"].append({"objectType": object_type.upper(), "values": values})
            elif object_type in [
                "console",
                "machine_grp",
                "location",
                "branch_connector_group",
                "edge_connector_group",
                "client_type",
            ]:
                # Each of these object types must be under individual operands blocks
                template.append({"operands": [{"objectType": object_type.upper(), "values": values}]})
            elif object_type in ["saml", "scim", "scim_group"]:
                # These types use "entryValues" with "lhs" and "rhs"
                template.append(
                    {
                        "operands": [
                            {"objectType": object_type.upper(), "entryValues": [{"lhs": v[0], "rhs": v[1]} for v in values]}
                        ]
                    }
                )
            elif object_type in [
                "posture",
                "trusted_network",
                "country_code",
                "platform",
                "risk_factor_type",
                "chrome_enterprise",
            ]:
                # These types use "entryValues" with "lhs" as unique ID and "rhs" as "true"/"false"
                template.append(
                    {"operands": [{"objectType": object_type.upper(), "entryValues": [{"lhs": values[0], "rhs": values[1]}]}]}
                )
            else:
                # Handle other possible object types if needed in the future
                template.append({"operands": [{"objectType": object_type.upper(), "values": values}]})

        # Add the grouped APP and APP_GROUP conditions if any were specified
        if grouped_conditions["app_and_app_group"]:
            template.append({"operands": grouped_conditions["app_and_app_group"]})

        return template

    def get_policy(self, policy_type: str, query_params=None) -> tuple:
        """
        Returns the policy and rule sets for the given policy type.

        Args:
            policy_type (str): The type of policy to be returned. Accepted values are:

                |  ``access`` - returns the Access Policy
                |  ``capabilities`` - returns the Capabilities Policy
                |  ``client_forwarding`` - returns the Client Forwarding Policy
                |  ``clientless`` - returns the Clientless Session Protection Policy
                |  ``credential`` - returns the Credential Policy
                |  ``inspection`` - returns the Inspection Policy
                |  ``isolation`` - returns the Isolation Policy
                |  ``redirection`` - returns the Redirection Policy
                |  ``siem`` - returns the SIEM Policy
                |  ``timeout`` - returns the Timeout Policy

        Returns:
            PolicySetControllerV1: The resource record of the specified policy type.

        Raises:
            ValueError: If the policy_type is invalid.

        Example:
            >>> policy = zpa.policies.get_policy('access')
        """
        mapped_policy_type = self.POLICY_MAP.get(policy_type)
        if not mapped_policy_type:
            raise ValueError(f"Incorrect policy type provided: {policy_type}")

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/policyType/{mapped_policy_type}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenantId")

        # Only add `microtenantId` to query_params if it is explicitly set
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id
        else:
            query_params.pop("microtenantId", None)  # Ensure `microtenantId` isn't added if it's None

        # Prepare the request
        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        # Handle the API response and return raw response data
        try:
            response_body = response.get_body()  # Get the raw response body
            if not response_body:
                return (None, response, None)
            return (response_body, response, None)

        except Exception as error:
            return (None, response, error)

    def get_rule(self, policy_type: str, rule_id: str, query_params=None) -> tuple:
        """
        Returns the specified policy rule.

        Args:
            policy_type (str): The type of policy to be returned. Accepted values are:

                |  ``access``
                |  ``capabilities``
                |  ``client_forwarding``
                |  ``clientless``
                |  ``credential``
                |  ``inspection``
                |  ``isolation``
                |  ``redirection``
                |  ``siem``
                |  ``timeout``

            rule_id (str): The unique identifier for the policy rule.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            PolicySetControllerV1: The resource record for the requested rule.

        Example:
            >>> rule = zpa.policies.get_rule('access', rule_id='12345')
        """
        # Set up default query parameters if none provided
        query_params = query_params or {}
        microtenant_id = query_params.get("microtenantId")

        # Retrieve policy_set_id explicitly
        policy_type_response, _, err = self.get_policy(policy_type, query_params={"microtenantId": microtenant_id})
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for {policy_type}: {err}")

        # Directly extract the policy_set_id from the response
        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, f"No policy ID found for '{policy_type}' policy type")

        # Construct the API URL using the retrieved policy ID
        http_method = "get".upper()
        api_url = format_url(f"{self._zpa_base_endpoint_v1}/policySet/{policy_set_id}/rule/{rule_id}")

        # Encode query parameters for the URL
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        # Create and execute the request
        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_rules(self, policy_type: str, query_params=None) -> tuple:
        """
        Returns policy rules for a given policy type.

        Args:
            policy_type (str): The policy type. Accepted values are:

                |  ``access`` - returns Access Policy rules
                |  ``timeout`` - returns Timeout Policy rules
                |  ``client_forwarding`` - returns Client Forwarding Policy rules
                |  ``isolation`` - returns Isolation Policy rules
                |  ``inspection`` - returns Inspection Policy rules
                |  ``redirection`` - returns Redirection Policy rules
                |  ``credential`` - returns Credential Policy rules
                |  ``capabilities`` - returns Capabilities Policy rules
                |  ``siem`` - returns SIEM Policy rules

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {int}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            list: A list of PolicySetControllerV1 objects.

        Example:
            >>> rules = zpa.policies.list_rules('access')
        """
        # Map the policy type to the ZPA API equivalent
        mapped_policy_type = self.POLICY_MAP.get(policy_type)
        if not mapped_policy_type:
            raise ValueError(f"Incorrect policy type provided: {policy_type}")

        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/rules/policyType/{mapped_policy_type}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        # Prepare request
        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PolicySetControllerV1(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_access_rule(
        self,
        name: str,
        action: str,
        app_connector_group_ids: list = [],
        app_server_group_ids: list = [],
        **kwargs,
    ) -> tuple:
        """
        Add a new Access Policy rule.

        See the `ZPA Access Policy API reference <https://help.zscaler.com/zpa/access-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``allow``
                |  ``deny``
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '99999'),
                    ('app', 'id', '88888'),
                    ('app_group', 'id', '77777),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            app_connector_group_ids (:obj:`list` of :obj:`str`):
                A list of application connector IDs that will be attached to the access policy rule.
            app_server_group_ids (:obj:`list` of :obj:`str`):
                A list of application server group IDs that will be attached to the access policy rule.

        Returns:
            PolicySetControllerV1: The resource record of the newly created access policy rule.

        """
        # Retrieve policy_set_id explicitly
        policy_type_response, _, err = self.get_policy("access", query_params={"microtenantId": kwargs.get("microtenantId")})
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'access': {err}")

        # Directly extract the policy_set_id from the response
        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'access' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule
        """
        )

        # Construct the payload with any additional attributes from kwargs
        payload = {
            "name": name,
            "action": action.upper(),
            "appConnectorGroups": [{"id": group_id} for group_id in app_connector_group_ids],
            "appServerGroups": [{"id": group_id} for group_id in app_server_group_ids],
        }

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        add_id_groups(self.reformat_params, kwargs, payload)

        conditions = kwargs.pop("conditions", [])
        if conditions:
            payload["conditions"] = self._create_conditions_v1(conditions)

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_access_rule(
        self,
        rule_id: str,
        name: str = None,
        action: str = None,
        app_connector_group_ids: list = None,
        app_server_group_ids: list = None,
        **kwargs,
    ) -> tuple:
        """
        Update an existing policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``allow``
                |  ``deny``
            app_connector_group_ids (:obj:`list` of :obj:`str`):
                A list of application connector IDs that will be attached to the access policy rule. Defaults to an empty list.
            app_server_group_ids (:obj:`list` of :obj:`str`):
                A list of server group IDs that will be attached to the access policy rule. Defaults to an empty list.

        Returns:
            PolicySetControllerV1: The updated policy rule record.

        Examples:
            Update the name and description of the Access Policy Rule:

            >>> zpa.policies.update_access_rule(
            ...    rule_id="999999",
            ...    name='Update_Access_Policy_Rule_v1',
            ...    description='Update_Access_Policy_Rule_v1',
            ... )
        """
        # Ensure microtenantId is set properly as a query parameter
        microtenant_id = kwargs.get("microtenantId")
        query_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # 1. We still need to retrieve the policy set ID
        policy_type_response, _, err = self.get_policy("access", query_params=query_params)
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'access': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'access' policy type")

        http_method = "put".upper()
        api_url = format_url(f"{self._zpa_base_endpoint_v1}/policySet/{policy_set_id}/rule/{rule_id}")

        payload = {
            "name": name,
            "action": action.upper() if action else None,
            "appConnectorGroups": [{"id": group_id} for group_id in (app_connector_group_ids or [])],
            "appServerGroups": [{"id": group_id} for group_id in (app_server_group_ids or [])],
        }

        # Add remaining attributes from kwargs, transforming them to camel case
        add_id_groups(self.reformat_params, kwargs, payload)
        conditions = kwargs.pop("conditions", [])
        if conditions:
            payload["conditions"] = self._create_conditions_v1(conditions)

        # Filter out None values if you prefer not to send them
        payload = {k: v for k, v in payload.items() if v is not None}

        # 4. Create request
        params = {"microtenantId": microtenant_id} if microtenant_id else {}
        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        # 5. Execute request
        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        # If 204 No Content => return an object with only the ID to indicate success
        if response is None:
            return (PolicySetControllerV1({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, None, error)

        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_timeout_rule(self, name: str, **kwargs) -> tuple:
        """
        Add a new Timeout Policy rule.

        See the `ZPA Timeout Policy API reference <https://help.zscaler.com/zpa/timeout-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            **kwargs:
                Optional parameters.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            re_auth_idle_timeout (int):
                The re-authentication idle timeout value in seconds.
            re_auth_timeout (int):
                The re-authentication timeout value in seconds.
        """
        policy_type_response, _, err = self.get_policy("timeout", query_params={"microtenantId": kwargs.get("microtenantId")})
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'timeout': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'timeout' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": "RE_AUTH",
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
            "reauthTimeout": kwargs.get("reauth_timeout", 172800),
            "reauthIdleTimeout": kwargs.get("reauth_idle_timeout", 600),
        }

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_timeout_rule(self, rule_id: str, name: str = None, **kwargs) -> tuple:
        """
        Update an existing policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            re_auth_idle_timeout (int):
                The re-authentication idle timeout value in seconds.
            re_auth_timeout (int):
                The re-authentication timeout value in seconds.

        Returns:

        Examples:
            Updates the name only for a Timeout Policy rule:

            >>> zpa.policies.update_timeout_rule('99999', name='new_rule_name')

            Updates the description for a Timeout Policy rule:

            >>> zpa.policies.update_timeout_rule('888888', description='Updated Description')
        """
        # Retrieve policy_set_id explicitly
        policy_type_response, _, err = self.get_policy("timeout", query_params={"microtenantId": kwargs.get("microtenantId")})
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'timeout': {err}")

        # Directly extract the policy_set_id from the response
        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'timeout' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name if name else kwargs.get("name"),
            "action": "RE_AUTH",
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
            "reauthTimeout": kwargs.get("reauth_timeout", 172800),
            "reauthIdleTimeout": kwargs.get("reauth_idle_timeout", 600),
        }

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV1({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_client_forwarding_rule(self, name: str, action: str, **kwargs) -> tuple:
        """
        Add a new Client Forwarding Policy rule.

        See the
        `ZPA Client Forwarding Policy API reference <https://help.zscaler.com/zpa/client-forwarding-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``intercept``
                |  ``intercept_accessible``
                |  ``bypass``
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.

        Returns:

        Examples:
            Add a new Client Forwarding Policy rule:

            >>> zpa.policies.add_client_forwarding_rule(
            ...    name='Add_Forwarding_Rule_v1',
            ...    description='Update_Forwarding_Rule_v1',
            ...    action='isolate',
            ...    conditions=[
            ...         ("app", ["216199618143361683"]),
            ...         ("app_group", ["216199618143360301"]),
            ...         ("scim_group", "idp_id", "scim_group_id"),
            ...         ("scim_group", "idp_id", "scim_group_id"),
            ...     ],
            ... )

        """
        # Retrieve policy_set_id explicitly
        policy_type_response, _, err = self.get_policy(
            "client_forwarding", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'client_forwarding': {err}")

        # Directly extract the policy_set_id from the response
        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'client_forwarding' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
        }

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_client_forwarding_rule(self, rule_id: str, name: str = None, action: str = None, **kwargs) -> tuple:
        """
        Update an existing Client Forwarding Policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``intercept``
                |  ``intercept_accessible``
                |  ``bypass``
            description (str):
                Additional information about the Client Forwarding Policy rule.
            enabled (bool):
                Whether or not the Client Forwarding Policy rule. is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', 'app_segment_id'),
                    ('app', 'id', 'app_segment_id'),
                    ('app_group', 'id', 'segment_group_id),
                    ("scim_group", "idp_id", "scim_group_id"),
                    ("scim_group", "idp_id", "scim_group_id"),
                    ('client_type', 'zpn_client_type_exporter')]

        Returns:

        Examples:
            Updates the name only for an Client Forwarding Policy rule:

            >>> zpa.policies.update_client_forwarding_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Forwarding_Rule_v1',
            ...    description='Update_Forwarding_Rule_v1',
            ...    action='isolate',
            ...    conditions=[
            ...         ("app", ["216199618143361683"]),
            ...         ("app_group", ["216199618143360301"]),
            ...         ("scim_group", "idp_id", "scim_group_id"),
            ...         ("scim_group", "idp_id", "scim_group_id"),
            ...     ],
            ... )
        """
        # Retrieve policy_set_id explicitly
        policy_type_response, _, err = self.get_policy(
            "client_forwarding", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'client_forwarding': {err}")

        # Directly extract the policy_set_id from the response
        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'client_forwarding' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Construct the payload similar to add_client_forwarding_rule
        payload = {
            "name": name if name else kwargs.get("name"),
            "action": action.upper() if action else kwargs.get("action", "").upper(),
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
        }

        # Add remaining attributes to the payload, ensuring correct formatting
        # for key, value in kwargs.items():
        #     payload[snake_to_camel(key)] = value

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        # Handle cases where no content is returned (204 No Content)
        if response is None:
            return (PolicySetControllerV1({"id": rule_id}), None, None)

        # Parse the response into a PolicySetController instance
        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_isolation_rule(self, name: str, action: str, zpn_isolation_profile_id: str = None, **kwargs) -> tuple:
        """
        Add a new Isolation Policy rule.

        See the
        `ZPA Isolation Policy API reference <https://help.zscaler.com/zpa/configuring-isolation-policies-using-api>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``isolate``
                |  ``bypass_isolate``
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter')]
            zpn_isolation_profile_id (str):
                The isolation profile ID associated with the rule
            description (str):
                A description for the rule.

        Returns:

        """
        # Validation: Check if zpn_isolation_profile_id is required based on the action
        if action == "isolate" and not zpn_isolation_profile_id:
            return (None, None, "Error: zpn_isolation_profile_id is required when action is 'isolate'.")

        # Retrieve policy_set_id explicitly
        policy_type_response, _, err = self.get_policy(
            "isolation", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'isolation': {err}")

        # Directly extract the policy_set_id from the response
        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'isolation' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
        }

        if action == "isolate":
            payload["zpnIsolationProfileId"] = zpn_isolation_profile_id

        client_type_present = any(
            cond.get("operands", [{}])[0].get("objectType", "") == "CLIENT_TYPE" for cond in payload["conditions"]
        )
        if not client_type_present:
            payload["conditions"].append(
                {"operator": "OR", "operands": [{"objectType": "CLIENT_TYPE", "lhs": "id", "rhs": "zpn_client_type_exporter"}]}
            )

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_isolation_rule(
        self, rule_id: str, name: str = None, action: str = None, zpn_isolation_profile_id: str = None, **kwargs
    ) -> tuple:
        """
        Update an existing client isolation policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``isolate``
                |  ``bypass_isolate``
            description (str):
                Additional information about the client forwarding policy rule.
            enabled (bool):
                Whether or not the client forwarding policy rule is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            zpn_isolation_profile_id (str):
                The unique identifier of the inspection profile. This field is applicable only for inspection policies.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter')]

        Returns:

        Examples:
            Updates the name only for an Isolation Policy rule:

            >>> zpa.policiesv2.update_isolation_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Isolation_Rule_v2',
            ...    description='Update_Isolation_Rule_v2',
            ...    action='isolate',
            ...    conditions=[
            ...         ("app", ["216199618143361683"]),
            ...         ("app_group", ["216199618143360301"]),
            ...         ("scim_group", [("216199618143191058", "2079468"), ("216199618143191058", "2079446")]),
            ...     ],
            ... )
        """
        if action == "isolate" and not zpn_isolation_profile_id:
            return (None, None, "Error: zpn_isolation_profile_id is required when action is 'isolate'.")

        # Retrieve the policy_set_id
        policy_type_response, _, err = self.get_policy(
            "isolation", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'isolation': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'isolation' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
        }

        if action == "isolate":
            payload["zpnIsolationProfileId"] = zpn_isolation_profile_id

        client_type_present = any(
            cond.get("operands", [{}])[0].get("objectType", "") == "CLIENT_TYPE" for cond in payload["conditions"]
        )
        if not client_type_present:
            payload["conditions"].append(
                {"operator": "OR", "operands": [{"objectType": "CLIENT_TYPE", "lhs": "id", "rhs": "zpn_client_type_exporter"}]}
            )

        microtenant_id = kwargs.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV1({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def add_app_protection_rule(self, name: str, action: str, zpn_inspection_profile_id: str = None, **kwargs) -> tuple:
        """
        Add a new App Protection Policy rule.
        """
        if action == "inspect" and not zpn_inspection_profile_id:
            return (None, None, "Error: zpn_inspection_profile_id is required when action is 'inspect'.")

        policy_type_response, _, err = self.get_policy("inspection")
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'inspection': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'inspection' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule
        """
        )

        payload = {
            "name": name,
            "action": action.upper(),
            "zpnInspectionProfileId": zpn_inspection_profile_id,
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
        }

        if action == "inspect":
            payload["zpnInspectionProfileId"] = zpn_inspection_profile_id

        request, error = self._request_executor.create_request(http_method, api_url, body=payload)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_app_protection_rule(
        self, rule_id: str, name: str, action: str, zpn_inspection_profile_id: str = None, **kwargs
    ) -> tuple:
        """
        Update an existing app protection policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``isolate``
                |  ``bypass_isolate``
            description (str):
                Additional information about the app protection policy rule.
            enabled (bool):
                Whether or not the app protection policy rule is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            zpn_inspection_profile_id (str):
                The unique identifier of the inspection profile. This field is applicable only for inspection policies.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter')]

        Returns:

        Examples:
            Updates the name only for an Inspection Policy rule:

            >>> zpa.policiesv2.update_app_protection_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Inspection_Rule_v2',
            ...    description='Update_Inspection_Rule_v2',
            ...    action='inspect',
            ...    zpn_inspection_profile_id='216199618143363055'
            ...    conditions=[
            ...         ("app", ["216199618143361683"]),
            ...         ("app_group", ["216199618143360301"]),
            ...         ("scim_group", [("216199618143191058", "2079468"), ("216199618143191058", "2079446")]),
            ...     ],
            ... )
        """
        if action == "inspect" and not zpn_inspection_profile_id:
            return (None, None, "Error: zpn_inspection_profile_id is required when action is 'inspect'.")

        policy_type_response, _, err = self.get_policy("inspection")
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'inspection': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'inspection' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
        }

        if action == "inspect":
            payload["zpnInspectionProfileId"] = zpn_inspection_profile_id

        request, error = self._request_executor.create_request(http_method, api_url, body=payload)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV1)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV1({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV1(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_access_rule_v2(
        self,
        name: str,
        action: str,
        **kwargs,
    ) -> tuple:
        """
        Add a new Access Policy rule.

        See the `ZPA Access Policy API reference <https://help.zscaler.com/zpa/access-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``allow``
                |  ``deny``
            **kwargs:
                Optional keyword args.

        Keyword Args:
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            app_connector_group_ids (:obj:`list` of :obj:`str`):
                A list of application connector IDs that will be attached to the access policy rule.
            app_server_group_ids (:obj:`list` of :obj:`str`):
                A list of application server group IDs that will be attached to the access policy rule.

            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '99999'),
                    ('app', 'id', '88888'),
                    ('app_group', 'id', '77777),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx', True)]

        Returns:
            :obj:`Tuple`: The resource record of the newly created access policy rule.

        """
        policy_type_response, _, err = self.get_policy("access", query_params={"microtenantId": kwargs.get("microtenantId")})
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'access': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'access' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule
        """
        )

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        add_id_groups(self.reformat_params, kwargs, payload)

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_access_rule_v2(self, rule_id: str, name: str = None, action: str = None, **kwargs) -> tuple:
        """
        Update an existing policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            app_connector_group_ids (:obj:`list` of :obj:`str`, optional):
                A list of application connector IDs that will be attached to the access policy rule. Defaults to an empty list.
            app_server_group_ids (:obj:`list` of :obj:`str`, optional):
                A list of server group IDs that will be attached to the access policy rule. Defaults to an empty list.

            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:
                |  ``ALLOW``
                |  ``DENY``
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.

        Returns:

        Examples:
            Updates the description for an Access Policy rule:

            >>> zpa.policiesv2.update_access_rule(
            ...    rule_id='216199618143320419',
            ...    description='Updated Description',
            ...    action='ALLOW',
            ...    conditions=[
            ...         ("client_type", ['zpn_client_type_exporter', 'zpn_client_type_zapp']),
            ...     ],
            ... )
        """
        policy_type_response, _, err = self.get_policy("access", query_params={"microtenantId": kwargs.get("microtenantId")})
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'client_forwarding': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'access' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name if name else kwargs.get("name"),
            "action": action.upper() if action else kwargs.get("action", "").upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        add_id_groups(self.reformat_params, kwargs, payload)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV2({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_timeout_rule_v2(self, name: str, **kwargs) -> tuple:
        """
        Update an existing policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            app_connector_group_ids (:obj:`list` of :obj:`str`, optional):
                A list of application connector IDs that will be attached to the access policy rule. Defaults to an empty list.
            app_server_group_ids (:obj:`list` of :obj:`str`, optional):
                A list of server group IDs that will be attached to the access policy rule. Defaults to an empty list.

            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:
                |  ``ALLOW``
                |  ``DENY``
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.

        Returns:

        Examples:
            Updates the description for an Access Policy rule:

            >>> zpa.policiesv2.update_access_rule(
            ...    rule_id='216199618143320419',
            ...    description='Updated Description',
            ...    action='ALLOW',
            ...    conditions=[
            ...         ("client_type", ['zpn_client_type_exporter', 'zpn_client_type_zapp']),
            ...     ],
            ... )
        """
        policy_type_response, _, err = self.get_policy("timeout", query_params={"microtenantId": kwargs.get("microtenantId")})
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'timeout': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'timeout' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": "RE_AUTH",
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
            "reauthTimeout": kwargs.get("reauth_timeout", 172800),
            "reauthIdleTimeout": kwargs.get("reauth_idle_timeout", 600),
        }

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_timeout_rule_v2(self, rule_id: str, name: str = None, **kwargs) -> tuple:
        """
        Update an existing policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            re_auth_idle_timeout (int):
                The re-authentication idle timeout value in seconds.
            re_auth_timeout (int):
                The re-authentication timeout value in seconds.

        Returns:

        Examples:
            Updates the name only for a Timeout Policy rule:

            >>> zpa.policies.update_timeout_rule('99999', name='new_rule_name')

            Updates the description for a Timeout Policy rule:

            >>> zpa.policies.update_timeout_rule('888888', description='Updated Description')
        """
        policy_type_response, _, err = self.get_policy("timeout", query_params={"microtenantId": kwargs.get("microtenantId")})
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'timeout': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'timeout' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": "RE_AUTH",
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
            "reauthTimeout": kwargs.get("reauth_timeout", 172800),
            "reauthIdleTimeout": kwargs.get("reauth_idle_timeout", 600),
        }

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV2({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_client_forwarding_rule_v2(self, name: str, action: str, **kwargs) -> tuple:
        """
        Add a new Client Forwarding Policy rule.

        See the
        `ZPA Client Forwarding Policy API reference <https://help.zscaler.com/zpa/client-forwarding-policy-use-cases>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``bypass``
                |  ``intercept``
                |  ``intercept_accessible``
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter', 'zpn_client_type_zapp'),
                    ('trusted_network', 'b15e4cad-fa6e-8182-9fc3-8125ee6a65e1', True)]
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
        """
        policy_type_response, _, err = self.get_policy(
            "client_forwarding", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'client_forwarding': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'client_forwarding' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_client_forwarding_rule_v2(self, rule_id: str, name: str = None, action: str = None, **kwargs) -> tuple:
        """
        Update an existing client forwarding policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:

            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``bypass``
                |  ``intercept``
                |  ``intercept_accessible``
            description (str):
                Additional information about the client forwarding policy rule.
            enabled (bool):
                Whether or not the client forwarding policy rule is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.

            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    ("client_type",
                        ['zpn_client_type_edge_connector',
                        'zpn_client_type_branch_connector',
                        'zpn_client_type_machine_tunnel',
                        'zpn_client_type_zapp', 'zpn_client_type_zapp_partner'
                    ]),

        Examples:
            Updates the name only for an Access Policy rule:

            >>> zpa.policiesv2.update_client_forwarding_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Redirection_Rule_v2',
            ...    description='Update_Redirection_Rule_v2',
            ...    action='redirect_default',
            ...    conditions=[
            ...         ("client_type",
            ...         ['zpn_client_type_edge_connector',
            ...          'zpn_client_type_branch_connector',
            ...          'zpn_client_type_machine_tunnel',
            ...          'zpn_client_type_zapp',
            ...          'zpn_client_type_zapp_partner']),
            ...     ],
            ... )
        """
        policy_type_response, _, err = self.get_policy(
            "client_forwarding", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'client_forwarding': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'client_forwarding' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name if name else kwargs.get("name"),
            "action": action.upper() if action else kwargs.get("action", "").upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV2({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_isolation_rule_v2(self, name: str, action: str, zpn_isolation_profile_id: str = None, **kwargs) -> tuple:
        """
        Add a new Isolation Policy rule.

        See the
        `ZPA Isolation Policy API reference <https://help.zscaler.com/zpa/configuring-isolation-policies-using-api>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``isolate``
                |  ``bypass_isolate``
            **kwargs:
                Optional keyword args.

        Keyword Args:
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter')]
            zpn_isolation_profile_id (str):
                The isolation profile ID associated with the rule
            description (str):
                A description for the rule.
        """
        if action == "isolate" and not zpn_isolation_profile_id:
            return (None, None, "Error: zpn_isolation_profile_id is required when action is 'isolate'.")

        policy_type_response, _, err = self.get_policy(
            "isolation", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'isolation': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'isolation' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": action.upper(),
            "zpnIsolationProfileId": zpn_isolation_profile_id,
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if action == "isolate":
            payload["zpnIsolationProfileId"] = zpn_isolation_profile_id

        payload["conditions"].append({"operands": [{"objectType": "CLIENT_TYPE", "values": ["zpn_client_type_exporter"]}]})

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_isolation_rule_v2(
        self, rule_id: str, name: str = None, action: str = None, zpn_isolation_profile_id: str = None, **kwargs
    ) -> tuple:
        """
        Update an existing client isolation policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``isolate``
                |  ``bypass_isolate``
            description (str):
                Additional information about the client forwarding policy rule.
            enabled (bool):
                Whether or not the client forwarding policy rule is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            zpn_isolation_profile_id (str):
                The unique identifier of the inspection profile. This field is applicable only for inspection policies.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter')]

        Examples:
            Updates the name only for an Isolation Policy rule:

            >>> zpa.policiesv2.update_isolation_rule_v1(
            ...    rule_id='216199618143320419',
            ...    name='Update_Isolation_Rule_v2',
            ...    description='Update_Isolation_Rule_v2',
            ...    action='isolate',
            ...    conditions=[
            ...         ("app", ["216199618143361683"]),
            ...         ("app_group", ["216199618143360301"]),
            ...         ("scim_group", [("216199618143191058", "2079468"), ("216199618143191058", "2079446")]),
            ...     ],
            ... )
        """
        if action == "isolate" and not zpn_isolation_profile_id:
            return (None, None, "Error: zpn_isolation_profile_id is required when action is 'isolate'.")

        policy_type_response, _, err = self.get_policy(
            "isolation", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'isolation': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'isolation' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        payload = {
            "name": name,
            "action": action.upper(),
            "zpnIsolationProfileId": zpn_isolation_profile_id,
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if action == "isolate":
            payload["zpnIsolationProfileId"] = zpn_isolation_profile_id

        if "conditions" not in payload:
            payload["conditions"] = []
        payload["conditions"].append({"operands": [{"objectType": "CLIENT_TYPE", "values": ["zpn_client_type_exporter"]}]})

        microtenant_id = kwargs.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV2({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_app_protection_rule_v2(self, name: str, action: str, zpn_inspection_profile_id: str = None, **kwargs) -> tuple:
        """
        Update an existing app protection policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``isolate``
                |  ``bypass_isolate``
            description (str):
                Additional information about the app protection policy rule.
            enabled (bool):
                Whether or not the app protection policy rule is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            zpn_inspection_profile_id (str):
                The unique identifier of the inspection profile. This field is applicable only for inspection policies.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    [('app', 'id', '926196382959075416'),
                    ('app', 'id', '926196382959075417'),
                    ('app_group', 'id', '926196382959075332),
                    ('client_type', 'zpn_client_type_exporter')]

        Examples:
            Updates the name only for an Inspection Policy rule:

            >>> zpa.policiesv2.update_app_protection_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Inspection_Rule_v2',
            ...    description='Update_Inspection_Rule_v2',
            ...    action='inspect',
            ...    zpn_inspection_profile_id='216199618143363055'
            ...    conditions=[
            ...         ("app", ["216199618143361683"]),
            ...         ("app_group", ["216199618143360301"]),
            ...         ("scim_group", [("216199618143191058", "2079468"), ("216199618143191058", "2079446")]),
            ...     ],
            ... )
        """
        if action == "inspect" and not zpn_inspection_profile_id:
            return (None, None, "Error: zpn_inspection_profile_id is required when action is 'inspect'.")

        policy_type_response, _, err = self.get_policy(
            "inspection", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'inspection': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'inspection' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule
        """
        )

        payload = {
            "name": name,
            "action": action.upper(),
            "zpnInspectionProfileId": zpn_inspection_profile_id,
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if action == "inspect":
            payload["zpnInspectionProfileId"] = zpn_inspection_profile_id

        request, error = self._request_executor.create_request(http_method, api_url, body=payload)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_app_protection_rule_v2(
        self, rule_id: str, name: str, action: str, zpn_inspection_profile_id: str = None, **kwargs
    ) -> tuple:
        """
        Add a new App Protection Policy rule.

        See the
        `ZPA App Protection Policies API reference <https://help.zscaler.com/zpa/configuring-privileged-policies-using-api>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            credential_id (str):
                The ID of the privileged credential for the rule.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the rule. Accepted value is: ``inject_credentials``
            description (str):
                Additional information about the credential rule.
            enabled (bool):
                Whether or not the credential rule is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`, `RHS value`.
                If you are adding multiple values for the same object type then you will need a new entry for each value.

                * `conditions`: This is for providing the set of conditions for the policy
                    * `object_type`: This is for specifying the policy criteria.
                        The following values are supported: "app", "app_group", "saml", "scim", "scim_group"
                        * `saml`: The unique Identity Provider ID and SAML attribute ID
                        * `scim`: The unique Identity Provider ID and SCIM attribute ID
                        * `scim_group`: The unique Identity Provider ID and SCIM_GROUP ID

                .. code-block:: python

                    zpa.policiesv2.add_privileged_credential_rule(
                        name='new_pra_credential_rule',
                        description='new_pra_credential_rule',
                        credential_id='credential_id',
                        conditions=[
                            ("scim_group", [("idp_id", "scim_group_id"), ("idp_id", "scim_group_id")])
                            ("console", ["console_id"]),
                        ],
                    )
        """
        if action == "inspect" and not zpn_inspection_profile_id:
            return (None, None, "Error: zpn_inspection_profile_id is required when action is 'inspect'.")

        policy_type_response, _, err = self.get_policy(
            "inspection", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'inspection': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'inspection' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if action == "inspect":
            payload["zpnInspectionProfileId"] = zpn_inspection_profile_id

        if "conditions" in payload and "conditions" not in kwargs:
            del payload["conditions"]

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)

        request, error = self._request_executor.create_request(http_method, api_url, body=payload)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV2({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_privileged_credential_rule_v2(self, name: str, credential_id: str, **kwargs) -> tuple:
        """
        Add a new Privileged Remote Access Credential Policy rule.
        """
        policy_type_response, _, err = self.get_policy(
            "credential", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'credential': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'credential' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": "INJECT_CREDENTIALS",
            "credential": {"id": credential_id},
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_privileged_credential_rule_v2(self, rule_id: str, credential_id: str, name: str = None, **kwargs) -> tuple:
        """
        Update an existing privileged credential policy rule.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            action (str):
                The action for the rule. Accepted value is: ``inject_credentials``
            description (str):
                Additional information about the credential rule.
            enabled (bool):
                Whether or not the credential rule is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            credential_id (str):
                The ID of the privileged credential for the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.

                Examples:

                .. code-block:: python

                    [('saml', 'id', '926196382959075416'),
                    ('scim', 'id', '926196382959075417'),
                    ('scim_group', 'id', '926196382959075332),
                    'credential_id', '926196382959075332, 'zpn_client_type_zapp'),

        Examples:
            Updates the name only for an Credential Policy rule:

            >>> zpa.policiesv2.update_privileged_credential_rule(
            ...   rule_id='888888',
            ...   name='credential_rule_new_name')
        """
        policy_type_response, _, err = self.get_policy(
            "credential", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'credential': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'credential' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": "INJECT_CREDENTIALS",
            "credential": {"id": credential_id},
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV2({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_capabilities_rule_v2(self, name: str, **kwargs) -> tuple:
        """
        Add a new Capability Access rule.

        See the
        `ZPA Capabilities Policies API reference:
        <https://help.zscaler.com/zpa/configuring-privileged-policies-using-api#postV2cap>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new capability rule.
            action (str):
                The action for the policy. Accepted value is: ``CHECK_CAPABILITIES``

            **kwargs:
                Optional keyword args.

        Keyword Args:
            rule_order (str):
                The new order for the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`, `RHS value`.
                If you are adding multiple values for the same object type then you will need a new entry for each value.

                - `conditions`: This is for providing the set of conditions for the policy
                    - `object_type`: This is for specifying the policy criteria.
                        The following values are supported: "app", "app_group", "saml", "scim", "scim_group"
                        - `app`: The unique Application Segment ID
                        - `app_group`: The unique Segment Group ID
                        - `saml`: The unique Identity Provider ID and SAML attribute ID
                        - `scim`: The unique Identity Provider ID and SCIM attribute ID
                        - `scim_group`: The unique Identity Provider ID and SCIM_GROUP ID

            privileged_capabilities (dict): A dictionary specifying the privileged capabilities with boolean values.
                The supported capabilities are:

                - clipboard_copy (bool): Indicates the PRA Clipboard Copy function.
                - clipboard_paste (bool): Indicates the PRA Clipboard Paste function.
                - file_upload (bool): Indicates the PRA File Transfer capabilities that enables the File Upload function.
                - file_download (bool): Indicates the PRA File Transfer capabilities that enables the File Download function.
                - inspect_file_upload (bool): Inspects the file via ZIA sandbox and uploads the file after inspection.
                - inspect_file_download (bool): Inspects the file via ZIA sandbox and downloads the file after the inspection.
                - monitor_session (bool): Indicates the PRA Monitoring Capabilities to enable the PRA Session Monitoring.
                - record_session (bool): Indicates PRA Session Recording capabilities to enable PRA Session Recording.
                - share_session (bool): Indicates PRA Session Control/Monitoring capabilities to enable PRA Session Monitoring.

        Returns:
            :obj:`Tuple`: The resource record of the newly created Capabilities rule.

        Example:
            Add a new capability rule with various capabilities and conditions:

            .. code-block:: python

                zpa.policiesv2.add_capabilities_rule(
                    name='New_Capability_Rule',
                    description='New_Capability_Rule',
                    conditions=[
                        ("app", ["app_segment_id"]),
                        ("app_group", ["segment_group_id"]),
                        ("scim_group", [("idp_id", "scim_group_id"), ("idp_id", "scim_group_id")])
                    ],
                    privileged_capabilities={
                        "clipboard_copy": True,
                        "clipboard_paste": True,
                        "file_download": True,
                        "file_upload": True,  # This will add "FILE_UPLOAD" to the capabilities list
                        "record_session": True,
                        # To handle the edge case, set file_upload to None to disable it
                        "file_upload": None
                    }
                )
        """
        policy_type_response, _, err = self.get_policy(
            "capabilities", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, "Error retrieving policy for 'capabilities': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'capabilities' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": "CHECK_CAPABILITIES",
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if "privileged_capabilities" in kwargs:
            capabilities = []
            priv_caps_map = kwargs.pop("privileged_capabilities")

            if priv_caps_map.get("clipboard_copy", False):
                capabilities.append("CLIPBOARD_COPY")
            if priv_caps_map.get("clipboard_paste", False):
                capabilities.append("CLIPBOARD_PASTE")
            if priv_caps_map.get("file_download", False):
                capabilities.append("FILE_DOWNLOAD")

            if priv_caps_map.get("file_upload") is True:
                capabilities.append("FILE_UPLOAD")
            elif priv_caps_map.get("file_upload") is False:
                capabilities.append("INSPECT_FILE_UPLOAD")

            if priv_caps_map.get("inspect_file_download", False):
                capabilities.append("INSPECT_FILE_DOWNLOAD")
            if priv_caps_map.get("inspect_file_upload", False):
                capabilities.append("INSPECT_FILE_UPLOAD")
            if priv_caps_map.get("monitor_session", False):
                capabilities.append("MONITOR_SESSION")
            if priv_caps_map.get("record_session", False):
                capabilities.append("RECORD_SESSION")
            if priv_caps_map.get("share_session", False):
                capabilities.append("SHARE_SESSION")

            payload["privilegedCapabilities"] = {"capabilities": capabilities}

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_capabilities_rule_v2(self, rule_id: str, name: str = None, **kwargs) -> tuple:
        """
        Update an existing capabilities policy rule.

        See the
        `ZPA Capabilities Policies API reference:
        <https://help.zscaler.com/zpa/configuring-privileged-policies-using-api#postV2cap>`_
        for further detail on optional keyword parameter structures.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            rule_order (str):
                The new order for the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`, `RHS value`.
                If you are adding multiple values for the same object type then you will need a new entry for each value.

                - `conditions`: This is for providing the set of conditions for the policy
                    - `object_type`: This is for specifying the policy criteria.
                        The following values are supported: "app", "app_group", "saml", "scim", "scim_group"
                        - `app`: The unique Application Segment ID
                        - `app_group`: The unique Segment Group ID
                        - `saml`: The unique Identity Provider ID and SAML attribute ID
                        - `scim`: The unique Identity Provider ID and SCIM attribute ID
                        - `scim_group`: The unique Identity Provider ID and SCIM_GROUP ID

            privileged_capabilities (dict): A dictionary specifying the privileged capabilities with boolean values.
                The supported capabilities are:

                - clipboard_copy (bool): Indicates the PRA Clipboard Copy function.
                - clipboard_paste (bool): Indicates the PRA Clipboard Paste function.
                - file_upload (bool): Indicates the PRA File Transfer capabilities that enables the File Upload function.
                - file_download (bool): Indicates the PRA File Transfer capabilities that enables the File Download function.
                - inspect_file_upload (bool): Inspects the file via ZIA sandbox and uploads the file after the inspection.
                - inspect_file_download (bool): Inspects the file via ZIA sandbox and downloads the file after inspection.
                - monitor_session (bool): Indicates PRA Monitoring Capabilities to enable the PRA Session Monitoring.
                - record_session (bool): Indicates PRA Session Recording capabilities to enable PRA Session Recording.
                - share_session (bool): Indicates PRA Session Control/Monitoring capabilities to enable PRA Session Monitoring.

        Returns:
            :obj:`Tuple`: The updated policy-capability-rule resource record.

        Examples:
            Updates the name and capabilities for an existing Capability Policy rule:

            >>> zpa.policiesv2.update_capabilities_rule_v2(
            ... rule_id='888888',
            ... name='Updated_Capability_Rule',
            ... conditions=[
            ...     ("app", ["216199618143361683"]),
            ...     ("app_group", ["216199618143360301"]),
            ...     ("scim_group", [("216199618143191058", "2079468"), ("216199618143191058", "2079446")])
            ... ],
            ... privileged_capabilities={
            ...     "clipboard_copy": True,
            ...     "clipboard_paste": True,
            ...     "file_download": True,
            ...     "file_upload": None
            ... }
            ... )
        """
        policy_type_response, _, err = self.get_policy(
            "capabilities", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'capabilities': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'capabilities' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": "CHECK_CAPABILITIES",
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if "conditions" in payload and "conditions" not in kwargs:
            del payload["conditions"]

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)
            elif key == "privileged_capabilities":
                capabilities = []
                priv_caps_map = value

                if priv_caps_map.get("clipboard_copy", False):
                    capabilities.append("CLIPBOARD_COPY")
                if priv_caps_map.get("clipboard_paste", False):
                    capabilities.append("CLIPBOARD_PASTE")
                if priv_caps_map.get("file_download", False):
                    capabilities.append("FILE_DOWNLOAD")

                if priv_caps_map.get("file_upload") is True:
                    capabilities.append("FILE_UPLOAD")
                elif priv_caps_map.get("file_upload") is False:
                    capabilities.append("INSPECT_FILE_UPLOAD")

                if priv_caps_map.get("inspect_file_download", False):
                    capabilities.append("INSPECT_FILE_DOWNLOAD")
                if priv_caps_map.get("inspect_file_upload", False):
                    capabilities.append("INSPECT_FILE_UPLOAD")
                if priv_caps_map.get("monitor_session", False):
                    capabilities.append("MONITOR_SESSION")
                if priv_caps_map.get("record_session", False):
                    capabilities.append("RECORD_SESSION")
                if priv_caps_map.get("share_session", False):
                    capabilities.append("SHARE_SESSION")

                payload["privilegedCapabilities"] = {"capabilities": capabilities}

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload["action"] = "CHECK_CAPABILITIES"

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV2({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def add_redirection_rule_v2(self, name: str, action: str, service_edge_group_ids: list = [], **kwargs) -> tuple:
        """
        Add a new Redirection Policy rule.

        See the
        `ZPA Redirection Policy API reference <https://help.zscaler.com/zpa/configuring-redirection-policies-using-api>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new redirection rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``redirect_default``
                |  ``redirect_preferred``
                |  ``redirect_always``
            **kwargs:
                Optional keyword args.

        Keyword Args:
            rule_order (str):
                The new order for the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`, `RHS value`.
                If you are adding multiple values for the same object type then you will need a new entry for each value.

                - `conditions`: This is for providing the set of conditions for the policy
                    - `object_type`: This is for specifying the policy criteria.
                        The following values are supported: "client_type", "country_code"
                    - `client_type`: The client type, must be one of the following:
                        `zpn_client_type_edge_connector`, `zpn_client_type_branch_connector`,
                        `zpn_client_type_machine_tunnel`, `zpn_client_type_zapp`, `zpn_client_type_zapp_partner`

        Returns:
            :obj:`Tuple`: The resource record of the newly created Redirection Policy rule.

        Example:
            Add a new redirection rule with various conditions and service edge group IDs:

            .. code-block:: python

                zpa.policiesv2.add_redirection_rule(
                    name='New_Redirection_Rule',
                    action='redirect_preferred',
                    service_edge_group_ids=['12345', '67890'],
                    conditions=[
                        ("client_type",
                            'zpn_client_type_edge_connector',
                            'zpn_client_type_branch_connector',
                            'zpn_client_type_machine_tunnel',
                            'zpn_client_type_zapp',
                            'zpn_client_type_zapp_partner'),
                    ]
                )
        """
        # Validate action and service_edge_group_ids based on action type
        if action.lower() == "redirect_default" and service_edge_group_ids:
            raise ValueError("service_edge_group_ids cannot be set when action is 'redirect_default'.")
        elif action.lower() in ["redirect_preferred", "redirect_always"] and not service_edge_group_ids:
            raise ValueError("service_edge_group_ids must be set when action is 'redirect_preferred' or 'redirect_always'.")

        policy_type_response, _, err = self.get_policy(
            "redirection", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'redirection': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'redirection' policy type")

        http_method = "post".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if service_edge_group_ids:
            payload["serviceEdgeGroups"] = [{"id": group_id} for group_id in service_edge_group_ids]

        valid_client_types = [
            "zpn_client_type_edge_connector",
            "zpn_client_type_branch_connector",
            "zpn_client_type_machine_tunnel",
            "zpn_client_type_zapp",
            "zpn_client_type_zapp_partner",
        ]

        for condition in payload["conditions"]:
            for operand in condition.get("operands", []):
                if operand["objectType"] == "CLIENT_TYPE" and operand["values"][0] not in valid_client_types:
                    raise ValueError(f"Invalid client_type value: {operand['values'][0]}. Must be one of {valid_client_types}")

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @synchronized(global_rule_lock)
    def update_redirection_rule_v2(
        self, rule_id: str, name: str, action: str, service_edge_group_ids: list = [], **kwargs
    ) -> tuple:
        """
        Update an existing policy rule.
        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:

            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``redirect_default``
                |  ``redirect_preferred``
                |  ``redirect_always``
            description (str):
                Additional information about the redirection rule.
            enabled (bool):
                Whether or not the redirection rule is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.
                E.g.

                .. code-block:: python

                    ("client_type", [
                        'zpn_client_type_edge_connector',
                        'zpn_client_type_branch_connector',
                        'zpn_client_type_machine_tunnel',
                        'zpn_client_type_zapp',
                        'zpn_client_type_zapp_partner'
                    ]),

        Returns:
            :obj:`Tuple`: The updated policy-rule resource record.

        Examples:
            Updates the name only for an Access Policy rule:

            >>> zpa.policiesv2.update_redirection_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Redirection_Rule_v2',
            ...    description='Update_Redirection_Rule_v2',
            ...    action='redirect_default',
            ...    conditions=[
            ...         ("client_type", [
            ...          'zpn_client_type_edge_connector',
            ...          'zpn_client_type_branch_connector',
            ...          'zpn_client_type_machine_tunnel',
            ...          'zpn_client_type_zapp',
            ...          'zpn_client_type_zapp_partner']),
            ...     ],
            ... )
        """
        # Validate action and service_edge_group_ids based on action type
        if action.lower() == "redirect_default" and service_edge_group_ids:
            raise ValueError("service_edge_group_ids cannot be set when action is 'redirect_default'.")
        elif action.lower() in ["redirect_preferred", "redirect_always"] and not service_edge_group_ids:
            raise ValueError("service_edge_group_ids must be set when action is 'redirect_preferred' or 'redirect_always'.")

        policy_type_response, _, err = self.get_policy(
            "redirection", query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for 'redirection': {err}")

        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, "No policy ID found for 'redirection' policy type")

        http_method = "put".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint_v2}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if service_edge_group_ids:
            payload["serviceEdgeGroups"] = [{"id": group_id} for group_id in service_edge_group_ids]

        valid_client_types = [
            "zpn_client_type_edge_connector",
            "zpn_client_type_branch_connector",
            "zpn_client_type_machine_tunnel",
            "zpn_client_type_zapp",
            "zpn_client_type_zapp_partner",
        ]

        for condition in payload["conditions"]:
            for operand in condition.get("operands", []):
                if operand["objectType"] == "CLIENT_TYPE" and operand["values"][0] not in valid_client_types:
                    raise ValueError(f"Invalid client_type value: {operand['values'][0]}. Must be one of {valid_client_types}")

        request, error = self._request_executor.create_request(http_method, api_url, body=payload, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, PolicySetControllerV2)
        if error:
            return (None, response, error)

        if response is None:
            return (PolicySetControllerV2({"id": rule_id}), None, None)

        try:
            result = PolicySetControllerV2(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @synchronized(global_rule_lock)
    def delete_rule(self, policy_type: str, rule_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes the specified policy rule.

        Args:
            policy_type (str):
                The type of policy the rule belongs to. Accepted values are:

                 |  ``access`` - returns the Access Policy
                 |  ``capabilities`` - returns the Capabilities Policy
                 |  ``client_forwarding`` - returns the Client Forwarding Policy
                 |  ``clientless`` - returns the Clientlesss Session Protection Policy
                 |  ``credential`` - returns the Credential Policy
                 |  ``inspection`` - returns the Inspection Policy
                 |  ``isolation`` - returns the Isolation Policy
                 |  ``redirection`` - returns the Redirection Policy
                 |  ``siem`` - returns the SIEM Policy
                 |  ``timeout`` - returns the Timeout Policy

            rule_id (str):
                The unique identifier for the policy rule.

        Examples:
            >>> zpa.policies.delete_rule(policy_type='access',
            ...    rule_id='88888')
        """
        # Retrieve policy_set_id explicitly
        policy_type_response, _, err = self.get_policy(policy_type, query_params={"microtenantId": microtenant_id})
        if err or not policy_type_response:
            return (None, None, f"Error retrieving policy for {policy_type}: {err}")

        # Directly extract the policy_set_id from the response
        policy_set_id = policy_type_response.get("id")
        if not policy_set_id:
            return (None, None, f"No policy ID found for '{policy_type}' policy type")

        # Construct the HTTP method and URL
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/rule/{rule_id}
        """
        )

        # Handle microtenant_id in URL params if provided
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)

    @synchronized(global_rule_lock)
    def reorder_rule(self, policy_type: str, rule_id: str, rule_order: str, **kwargs) -> tuple:
        """
        Change the order of an existing policy rule.

        Args:
            policy_type (str):
                The policy type. Accepted values:

                - ``access``
                - ``timeout``
                - ``client_forwarding``
                - ``isolation``
                - ``inspection``
                - ``redirection``
                - ``credential``
                - ``capabilities``
                - ``siem``

            rule_id (str):
                The unique ID of the rule that will be reordered.
            rule_order (str):
                The new order for the rule.

            **kwargs:
                Optional keyword arguments.
                - **microtenant_id** (str):
                The ID of the microtenant, if applicable.

        Returns:
            tuple:
                (Updated rule, response, error)

        Examples:
            Updates the order for an existing access policy rule:

            >>> zpa.policies.reorder_rule(
            ...     policy_type='access',
            ...     rule_id='88888',
            ...     rule_order='2'
            ... )

            Updates the order for an existing timeout policy rule with a specific microtenant:

            >>> zpa.policies.reorder_rule(
            ...     policy_type='timeout',
            ...     rule_id='77777',
            ...     rule_order='1',
            ...     microtenant_id='1234567890'
            ... )
        """
        http_method = "put".upper()
        policy_set_id, response, error = self.get_policy(
            policy_type, query_params={"microtenantId": kwargs.get("microtenantId")}
        )
        if error or not policy_set_id:
            return (None, response, error)

        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id.get("id")}/rule/{rule_id}/reorder/{rule_order}
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    @synchronized(global_rule_lock)
    def bulk_reorder_rules(self, policy_type: str, rules_orders: list[str], **kwargs) -> tuple:
        """
        Bulk change the order of policy rules.

        Args:
            policy_type (str): The policy type. Accepted values are:

                |  ``access``
                |  ``timeout``
                |  ``client_forwarding``
                |  ``isolation``
                |  ``inspection``
                |  ``redirection``
                |  ``credential``
                |  ``capabilities``
                |  ``siem``
            rules_orders (list[str]): A list of rule IDs in the desired order.
            **kwargs: Optional keyword arguments.

        Returns:
            tuple: (Response, error)

        Examples:
            Reordering access policy rules:

            >>> zpa.policies.bulk_reorder_rules(
            ...     policy_type='access',
            ...     rules_orders=[
            ...         '216199618143374210',
            ...         '216199618143374209',
            ...         '216199618143374208',
            ...         '216199618143374207',
            ...         '216199618143374206',
            ...         '216199618143374205',
            ...         '216199618143374204',
            ...         '216199618143374203',
            ...         '216199618143374202',
            ...         '216199618143374201',
            ...     ]
            ... )

            Reordering timeout policy rules for a specific microtenant:

            >>> zpa.policies.bulk_reorder_rules(
            ...     policy_type='timeout',
            ...     rules_orders=[
            ...         '216199618143374220',
            ...         '216199618143374219',
            ...         '216199618143374218',
            ...         '216199618143374217',
            ...         '216199618143374216',
            ...     ],
            ...     microtenant_id='1234567890'
            ... )
        """
        http_method = "put".upper()
        policy_data, _, err = self.get_policy(policy_type)
        if err or not policy_data:
            return (None, None, f"Error retrieving policy for {policy_type}: {err}")

        policy_set_id = policy_data.get("id")
        if not policy_set_id:
            return (None, None, f"No policy ID found for policy_type: {policy_type}")

        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v1}
            /policySet/{policy_set_id}/reorder
        """
        )

        # Extract microtenant_id if present in kwargs
        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Call create_request without the need for custom headers
        request, error = self._request_executor.create_request(http_method, api_url, body=rules_orders, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
