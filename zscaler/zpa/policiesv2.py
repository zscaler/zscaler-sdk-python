import functools

from box import Box, BoxList
from requests import Response

from zscaler.utils import add_id_groups, convert_keys, snake_to_camel
from zscaler.zpa.client import ZPAClient


class PolicySetsV2API:
    def __init__(self, client: ZPAClient):
        self.rest = client

    POLICY_MAP = {
        "access": "ACCESS_POLICY",
        "capabilities": "CAPABILITIES_POLICY",
        "client_forwarding": "CLIENT_FORWARDING_POLICY",
        "clientless": "CLIENTLESS_SESSION_PROTECTION_POLICY",
        "credential": "CREDENTIAL_POLICY",
        "inspection": "INSPECTION_POLICY",
        "isolation": "ISOLATION_POLICY",
        "redirection": "REDIRECTION_POLICY",
        "siem": "SIEM_POLICY",
        "timeout": "TIMEOUT_POLICY",
    }

    reformat_params = [
        ("app_server_group_ids", "appServerGroups"),
        ("app_connector_group_ids", "appConnectorGroups"),
        ("service_edge_group_ids", "serviceEdgeGroups"),
    ]

    def _create_conditions(self, conditions: list) -> list:
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
            elif object_type in ["posture", "trusted_network", "country_code", "platform"]:
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

    def get_policy(self, policy_type: str) -> Box:
        """
        Returns the policy and rule sets for the given policy type.

        Args:
            policy_type (str): The type of policy to be returned. Accepted values are:

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

        Returns:
            :obj:`Box`: The resource record of the specified policy type.

        Examples:
            Request the specified Policy.

            >>> pprint(zpa.policies.get_policy('access'))

        """
        # Map the simplified policy_type name to the name expected by the Zscaler API
        mapped_policy_type = self.POLICY_MAP.get(policy_type, None)

        # If the user provided an incorrect name, raise an error
        if not mapped_policy_type:
            raise ValueError(
                f"Incorrect policy type provided: {policy_type}\n "
                f"Policy type must be 'access', 'timeout', 'client_forwarding' or 'siem'."
            )

        return self.rest.get(f"policySet/policyType/{mapped_policy_type}")

    def get_rule(self, policy_type: str, rule_id: str) -> Box:
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

        Returns:
            :obj:`Box`: The resource record for the requested rule.

        Examples:
            >>> policy_rule = zpa.policies.get_rule(policy_id='99999',
            ...    rule_id='88888')

        """
        # Get the policy id for the supplied policy_type
        policy_id = self.get_policy(policy_type).id

        return self.rest.get(f"policySet/{policy_id}/rule/{rule_id}")

    def get_rule_by_name(self, policy_type: str, rule_name: str) -> Box:
        """
        Returns the specified policy rule by its name.

        Args:
            policy_type (str): The type of policy to be returned.
                Accepted values are: ``access``, ``timeout``, ``client_forwarding``, ``siem``
            rule_name (str): The name of the policy rule.

        Returns:
            :obj:`Box`: The resource record for the requested rule.

        Examples:
            >>> policy_rule = zpa.policies.get_rule_by_name(policy_type='access', rule_name='MyRule')

        """
        all_rules = self.list_rules(policy_type)
        for rule in all_rules:
            if rule.name == rule_name:
                return rule
        return None

    def list_rules(self, policy_type: str, **kwargs) -> BoxList:
        """
        Returns policy rules for a given policy type.

        Args:
            policy_type (str):
                The policy type. Accepted values are:

                |  ``access`` - returns Access Policy rules
                |  ``timeout`` - returns Timeout Policy rules
                |  ``client_forwarding`` - returns Client Forwarding Policy rules
                |  ``isolation`` - returns Isolation Policy rules
                |  ``inspection`` - returns Inspection Policy rules
                |  ``redirection`` - returns Redirection Policy rules
                |  ``credential`` - returns Credential Policy rules
                |  ``capabilities`` - returns Capabilities Policy rules
                |  ``siem`` - returns SIEM Policy rules
        Returns:
            :obj:`list`: A list of all policy rules that match the requested type.

        Examples:
            >>> for policy in zpa.policies.list_type('type')
            ...    pprint(policy)

        """

        # Map the simplified policy_type name to the name expected by the Zscaler API
        mapped_policy_type = self.POLICY_MAP.get(policy_type, None)

        # If the user provided an incorrect name, raise an error
        if not mapped_policy_type:
            raise ValueError(
                f"Incorrect policy type provided: {policy_type}\n "
                f"Policy type must be 'access', 'timeout', 'client_forwarding' or 'siem'."
            )
        list, _ = self.rest.get_paginated_data(
            path=f"policySet/rules/policyType/{mapped_policy_type}",
            **kwargs,
            api_version="v1",
        )
        return list

    def add_access_rule(
        self,
        name: str,
        action: str,
        app_connector_group_ids: list = [],
        app_server_group_ids: list = [],
        **kwargs,
    ) -> Box:
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
            :obj:`Box`: The resource record of the newly created access policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        if app_connector_group_ids:
            payload["appConnectorGroups"] = [{"id": group_id} for group_id in app_connector_group_ids]

        if app_server_group_ids:
            payload["appServerGroups"] = [{"id": group_id} for group_id in app_server_group_ids]

        add_id_groups(self.reformat_params, kwargs, payload)

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("access").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, api_version="v2")
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_access_rule(
        self,
        policy_type: str,
        rule_id: str,
        app_connector_group_ids: list = None,
        app_server_group_ids: list = None,
        **kwargs,
    ) -> Box:
        """
        Update an existing policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            policy_type (str):
                The policy type. Accepted values are:
                 |  ``access``
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
            :obj:`Box`: The updated policy-rule resource record.

        Examples:
            ...
        """
        # Handle default values for app_connector_group_ids and app_server_group_ids
        app_connector_group_ids = app_connector_group_ids or []
        app_server_group_ids = app_server_group_ids or []

        # Get policy id for specified policy type
        policy_id = self.get_policy(policy_type).id

        payload = convert_keys(self.get_rule(policy_type, rule_id))

        # Update kwargs with app_connector_group_ids and app_server_group_ids for processing with add_id_groups
        kwargs["app_connector_group_ids"] = app_connector_group_ids
        kwargs["app_server_group_ids"] = app_server_group_ids

        add_id_groups(self.reformat_params, kwargs, payload)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, api_version="v2").status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_rule(policy_type, rule_id)

    def add_timeout_rule(self, name: str, **kwargs) -> Box:
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

        Returns:
            :obj:`Box`: The resource record of the newly created Timeout Policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": "RE_AUTH",
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("timeout").id

        # Use specified timeouts or default to UI values
        payload["reauthTimeout"] = kwargs.get("re_auth_timeout", 172800)
        payload["reauthIdleTimeout"] = kwargs.get("re_auth_idle_timeout", 600)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, api_version="v2")
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_timeout_rule(self, rule_id: str, **kwargs) -> Box:
        """
        Update an existing policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            policy_type (str):
                The policy type. Accepted values are:

                 |  ``timeout``
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
            :obj:`Box`: The updated policy-rule resource record.

        Examples:
            Updates the name only for an Timeout Policy rule:

            >>> zpa.policies.update_rule('timeout', '99999', name='new_rule_name')

            Updates the action only for a Timeout Policy rule:

            >>> zpa.policies.update_rule('timeout', '888888', action='BYPASS')

        """
        # Get policy id for specified policy type
        policy_id = self.get_policy("timeout").id

        payload = convert_keys(self.get_rule(policy_id, rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, api_version="v2").status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_rule(policy_id, rule_id)

    def add_client_forwarding_rule(self, name: str, action: str, **kwargs) -> Box:
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

        Returns:
            :obj:`Box`: The resource record of the newly created Client Forwarding Policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("client_forwarding").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, api_version="v2")
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_client_forwarding_rule(self, rule_id: str, **kwargs) -> Box:
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

                    ("client_type", ['zpn_client_type_edge_connector', 'zpn_client_type_branch_connector', 'zpn_client_type_machine_tunnel', 'zpn_client_type_zapp', 'zpn_client_type_zapp_partner']),

        Returns:
            :obj:`Box`: The updated policy-rule resource record.

        Examples:
            Updates the name only for an Access Policy rule:

            >>> zpa.policiesv2.update_client_forwarding_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Redirection_Rule_v2',
            ...    description='Update_Redirection_Rule_v2',
            ...    action='redirect_default',
            ...    conditions=[
            ...         ("client_type", ['zpn_client_type_edge_connector', 'zpn_client_type_branch_connector', 'zpn_client_type_machine_tunnel', 'zpn_client_type_zapp', 'zpn_client_type_zapp_partner']),
            ...     ],
            ...         )
        """

        # Ensure the action is provided and convert to uppercase
        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()

        # Get policy id for specified policy type
        policy_id = self.get_policy("client_forwarding").id

        payload = convert_keys(self.get_rule("client_forwarding", rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        # Set the action in the payload
        payload["action"] = action

        # Make the PUT request to update the rule
        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, api_version="v2")
        # Return the object if it was updated successfully
        if not isinstance(response, Response):
            return self.get_rule("client_forwarding", rule_id)

    def add_isolation_rule(self, name: str, action: str, zpn_isolation_profile_id: str, **kwargs) -> Box:
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
            :obj:`Box`: The resource record of the newly created Client Isolation Policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "zpnIsolationProfileId": zpn_isolation_profile_id,
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Pre-configure client_type to 'zpn_client_type_exporter'
        payload["conditions"].append({"operands": [{"objectType": "CLIENT_TYPE", "values": ["zpn_client_type_exporter"]}]})

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("isolation").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, api_version="v2")
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_isolation_rule(self, rule_id: str, **kwargs) -> Box:
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
            :obj:`Box`: The updated policy-rule resource record.

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

        # Ensure the action is provided and convert to uppercase
        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()

        # Get policy id for specified policy type
        policy_id = self.get_policy("isolation").id

        payload = convert_keys(self.get_rule("isolation", rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        # Pre-configure client_type to 'zpn_client_type_exporter'
        payload["conditions"].append({"operands": [{"objectType": "CLIENT_TYPE", "values": ["zpn_client_type_exporter"]}]})

        # Set the action in the payload
        payload["action"] = action

        # Make the PUT request to update the rule
        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, api_version="v2")
        # Return the object if it was updated successfully
        if not isinstance(response, Response):
            return self.get_rule("isolation", rule_id)

    def add_app_protection_rule(self, name: str, action: str, zpn_inspection_profile_id: str, **kwargs) -> Box:
        """
        Add a new AppProtection Policy rule.

        See the
        `ZPA AppProtection Policy API reference <https://help.zscaler.com/zpa/configuring-appprotection-policies-using-api>`_
        for further detail on optional keyword parameter structures.

        Args:
            name (str):
                The name of the new rule.
            action (str):
                The action for the policy. Accepted values are:

                |  ``inspect``
                |  ``bypass_inspect``
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
            zpn_inspection_profile_id (str):
                The AppProtection profile ID associated with the rule
            description (str):
                A description for the rule.

        Returns:
            :obj:`Box`: The resource record of the newly created Client Inspection Policy rule.

        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "zpnInspectionProfileId": zpn_inspection_profile_id,
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("inspection").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, api_version="v2")
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_app_protection_rule(self, rule_id: str, **kwargs) -> Box:
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
            :obj:`Box`: The updated policy-rule resource record.

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

        # Ensure the action is provided and convert to uppercase
        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()

        # Get policy id for specified policy type
        policy_id = self.get_policy("inspection").id

        payload = convert_keys(self.get_rule("inspection", rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        # Set the action in the payload
        payload["action"] = action

        # Make the PUT request to update the rule
        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, api_version="v2")
        # Return the object if it was updated successfully
        if not isinstance(response, Response):
            return self.get_rule("inspection", rule_id)

    def add_privileged_credential_rule(self, name: str, credential_id: str, **kwargs) -> Box:
        """
        Add a new Privileged Remote Access Credential Policy rule.

        See the
        `ZPA Privileged Policies API reference <https://help.zscaler.com/zpa/configuring-privileged-policies-using-api>`_
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
                    * `object_type`: This is for specifying the policy criteria. The following values are supported: "app", "app_group", "saml", "scim", "scim_group"
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

        Returns:
            :obj:`Box`: The resource record of the newly created Privileged Remote Access Credential rule.
        """

        # Initialise the payload
        payload = {
            "name": name,
            "action": "INJECT_CREDENTIALS",
            "credential": {"id": credential_id},
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("credential").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, api_version="v2")
        if isinstance(response, Response):
            # This is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_privileged_credential_rule(self, rule_id: str, **kwargs) -> Box:
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

        Returns:
            :obj:`Box`: The updated policy-credential-rule resource record.

        Examples:
            Updates the name only for an Credential Policy rule:

            >>> zpa.policiesv2.update_privileged_credential_rule(
            ...   rule_id='888888',
            ...   name='credential_rule_new_name')

        """
        # Get the policy id for the specified policy type
        policy_id = self.get_policy("credential").id

        # Retrieve the existing rule to update
        payload = convert_keys(self.get_rule("credential", rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            elif key == "credential_id":
                payload["credential"] = {"id": value}
            else:
                payload[snake_to_camel(key)] = value

        # Ensure the action is set to CHECK_CAPABILITIES
        payload["action"] = "INJECT_CREDENTIALS"

        # Make the PUT request to update the rule
        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, api_version="v2")
        # Return the object if it was updated successfully
        if not isinstance(response, Response):
            return self.get_rule("credential", rule_id)

    def add_capabilities_rule(self, name: str, **kwargs) -> Box:
        """
        Add a new Capability Access rule.

        See the
        `ZPA Capabilities Policies API reference <https://help.zscaler.com/zpa/configuring-privileged-policies-using-api#postV2cap>`_
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
                    - `object_type`: This is for specifying the policy criteria. The following values are supported: "app", "app_group", "saml", "scim", "scim_group"
                        - `app`: The unique Application Segment ID
                        - `app_group`: The unique Segment Group ID
                        - `saml`: The unique Identity Provider ID and SAML attribute ID
                        - `scim`: The unique Identity Provider ID and SCIM attribute ID
                        - `scim_group`: The unique Identity Provider ID and SCIM_GROUP ID

            privileged_capabilities (dict): A dictionary specifying the privileged capabilities with boolean values. The supported capabilities are:

                - clipboard_copy (bool): Indicates the PRA Clipboard Copy function.
                - clipboard_paste (bool): Indicates the PRA Clipboard Paste function.
                - file_upload (bool): Indicates the PRA File Transfer capabilities that enables the File Upload function.
                - file_download (bool): Indicates the PRA File Transfer capabilities that enables the File Download function.
                - inspect_file_upload (bool): Inspects the file via ZIA sandbox and uploads the file following the inspection.
                - inspect_file_download (bool): Inspects the file via ZIA sandbox and downloads the file following the inspection.
                - monitor_session (bool): Indicates the PRA Monitoring Capabilities to enable the PRA Session Monitoring function.
                - record_session (bool): Indicates the PRA Session Recording capabilities to enable PRA Session Recording.
                - share_session (bool): Indicates the PRA Session Control and Monitoring capabilities to enable PRA Session Monitoring.

        Returns:
            :obj:`Box`: The resource record of the newly created Capabilities rule.

        Example:
            Add a new capability rule with various capabilities and conditions:

            .. code-block:: python

                zpa.policiesv2.add_capabilities_rule(
                    name='New_Capability_Rule',
                    description='New_Capability_Rule',
                    action='check_capabilities',
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

        # Initialise the payload
        payload = {
            "name": name,
            "action": "CHECK_CAPABILITIES",
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        # Process privileged capabilities
        if "privileged_capabilities" in kwargs:
            capabilities = []
            priv_caps_map = kwargs.pop("privileged_capabilities")

            if priv_caps_map.get("clipboard_copy", False):
                capabilities.append("CLIPBOARD_COPY")
            if priv_caps_map.get("clipboard_paste", False):
                capabilities.append("CLIPBOARD_PASTE")
            if priv_caps_map.get("file_download", False):
                capabilities.append("FILE_DOWNLOAD")

            # Handling the edge case for file_upload
            if priv_caps_map.get("file_upload") == True:
                capabilities.append("FILE_UPLOAD")
            elif priv_caps_map.get("file_upload") == False:
                capabilities.append("INSPECT_FILE_UPLOAD")
            # If file_upload is not present or set to None, do not append either capability

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

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("capabilities").id

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, api_version="v2")
        if isinstance(response, Response):
            # This is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_capabilities_rule(self, rule_id: str, **kwargs) -> Box:
        """
        Update an existing capabilities policy rule.

        See the
        `ZPA Capabilities Policies API reference <https://help.zscaler.com/zpa/configuring-privileged-policies-using-api#postV2cap>`_
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
                    - `object_type`: This is for specifying the policy criteria. The following values are supported: "app", "app_group", "saml", "scim", "scim_group"
                        - `app`: The unique Application Segment ID
                        - `app_group`: The unique Segment Group ID
                        - `saml`: The unique Identity Provider ID and SAML attribute ID
                        - `scim`: The unique Identity Provider ID and SCIM attribute ID
                        - `scim_group`: The unique Identity Provider ID and SCIM_GROUP ID

            privileged_capabilities (dict): A dictionary specifying the privileged capabilities with boolean values. The supported capabilities are:

                - clipboard_copy (bool): Indicates the PRA Clipboard Copy function.
                - clipboard_paste (bool): Indicates the PRA Clipboard Paste function.
                - file_upload (bool): Indicates the PRA File Transfer capabilities that enables the File Upload function.
                - file_download (bool): Indicates the PRA File Transfer capabilities that enables the File Download function.
                - inspect_file_upload (bool): Inspects the file via ZIA sandbox and uploads the file following the inspection.
                - inspect_file_download (bool): Inspects the file via ZIA sandbox and downloads the file following the inspection.
                - monitor_session (bool): Indicates the PRA Monitoring Capabilities to enable the PRA Session Monitoring function.
                - record_session (bool): Indicates the PRA Session Recording capabilities to enable PRA Session Recording.
                - share_session (bool): Indicates the PRA Session Control and Monitoring capabilities to enable PRA Session Monitoring.

        Returns:
            :obj:`Box`: The updated policy-capability-rule resource record.

        Examples:
            Updates the name and capabilities for an existing Capability Policy rule:

            >>> zpa.policiesv2.update_capabilities_rule(
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
        # Get the policy id for the specified policy type
        policy_id = self.get_policy("capabilities").id

        # Retrieve the existing rule to update
        payload = convert_keys(self.get_rule("capabilities", rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            elif key == "privileged_capabilities":
                capabilities = []
                priv_caps_map = value

                if priv_caps_map.get("clipboard_copy", False):
                    capabilities.append("CLIPBOARD_COPY")
                if priv_caps_map.get("clipboard_paste", False):
                    capabilities.append("CLIPBOARD_PASTE")
                if priv_caps_map.get("file_download", False):
                    capabilities.append("FILE_DOWNLOAD")

                # Handling the edge case for file_upload
                if priv_caps_map.get("file_upload") == True:
                    capabilities.append("FILE_UPLOAD")
                elif priv_caps_map.get("file_upload") == False:
                    capabilities.append("INSPECT_FILE_UPLOAD")
                # If file_upload is not present or set to None, do not append either capability

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
            else:
                payload[snake_to_camel(key)] = value

        payload["action"] = "CHECK_CAPABILITIES"

        # Make the PUT request to update the rule
        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, api_version="v2")
        # Return the object if it was updated successfully
        if not isinstance(response, Response):
            return self.get_rule("capabilities", rule_id)

    def add_redirection_rule(self, name: str, action: str, service_edge_group_ids: list = [], **kwargs) -> Box:
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
            conditions (list):
                A list of conditional rule tuples. Tuples must follow the convention: `Object Type`, `LHS value`,
                `RHS value`. If you are adding multiple values for the same object type then you will need
                a new entry for each value.

                * `conditions`: This is for providing the set of conditions for the policy
                    * `object_type`: This is for specifying the policy criteria. The following values are supported: "app", "app_group", "saml", "scim", "scim_group", "client_type"
                        * `client_type`: The client type, must be one of the following:
                            - 'zpn_client_type_edge_connector'
                            - 'zpn_client_type_branch_connector'
                            - 'zpn_client_type_machine_tunnel'
                            - 'zpn_client_type_zapp'
                            - 'zpn_client_type_zapp_partner'

        Returns:
            :obj:`Box`: The resource record of the newly created Redirection Policy rule.

        Example:
            Add a new redirection rule with various conditions and service edge group IDs:

            .. code-block:: python

                zpa.policiesv2.add_redirection_rule(
                    name='New_Redirection_Rule',
                    action='redirect_preferred',
                    service_edge_group_ids=['12345', '67890'],
                    conditions=[
                        ("client_type", 'zpn_client_type_edge_connector', 'zpn_client_type_branch_connector', 'zpn_client_type_machine_tunnel', 'zpn_client_type_zapp', 'zpn_client_type_zapp_partner'),
                    ]
                )
        """
        # Validate action and service_edge_group_ids based on action type
        if action.lower() == "redirect_default" and service_edge_group_ids:
            raise ValueError("service_edge_group_ids cannot be set when action is 'redirect_default'.")
        elif action.lower() in ["redirect_preferred", "redirect_always"] and not service_edge_group_ids:
            raise ValueError("service_edge_group_ids must be set when action is 'redirect_preferred' or 'redirect_always'.")

        # Initialise the payload
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions(kwargs.pop("conditions", [])),
        }

        if service_edge_group_ids:
            payload["serviceEdgeGroups"] = [{"id": group_id} for group_id in service_edge_group_ids]

        # Validate client_type values within conditions
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

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("redirection").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, api_version="v2")
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_redirection_rule(self, rule_id: str, **kwargs) -> Box:
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

                    ("client_type", ['zpn_client_type_edge_connector', 'zpn_client_type_branch_connector', 'zpn_client_type_machine_tunnel', 'zpn_client_type_zapp', 'zpn_client_type_zapp_partner']),

        Returns:
            :obj:`Box`: The updated policy-rule resource record.

        Examples:
            Updates the name only for an Access Policy rule:

            >>> zpa.policiesv2.update_redirection_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Redirection_Rule_v2',
            ...    description='Update_Redirection_Rule_v2',
            ...    action='redirect_default',
            ...    conditions=[
            ...         ("client_type", ['zpn_client_type_edge_connector', 'zpn_client_type_branch_connector', 'zpn_client_type_machine_tunnel', 'zpn_client_type_zapp', 'zpn_client_type_zapp_partner']),
            ...     ],
            ...         )
        """

        # Ensure the action is provided and convert to uppercase
        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()

        # Get policy id for specified policy type
        policy_id = self.get_policy("redirection").id

        payload = convert_keys(self.get_rule("redirection", rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        # Set the action in the payload
        payload["action"] = action

        # Make the PUT request to update the rule
        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, api_version="v2")
        # Return the object if it was updated successfully
        if not isinstance(response, Response):
            return self.get_rule("redirection", rule_id)

    def reorder_rule(self, policy_type: str, rule_id: str, rule_order: str) -> Box:
        """
        Change the order of an existing policy rule.

        Args:
            rule_id (str):
                The unique id of the rule that will be reordered.
            rule_order (str):
                The new order for the rule.
            policy_type (str):
                The policy type. Accepted values are:

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


        Returns:
             :obj:`Box`: The updated policy rule resource record.

        Examples:
            Updates the order for an existing policy rule:

            >>> zpa.policies.reorder_rule(policy_type='access',
            ...    rule_id='88888',
            ...    rule_order='2')

        """
        # Get policy id for specified policy type
        policy_id = self.get_policy(policy_type).id

        resp = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}/reorder/{rule_order}").status_code

        if resp == 204:
            return self.get_rule(policy_type, rule_id)

    def sort_key(self, rules_orders: dict[str, int]):
        def key(a, b):
            if a.id in rules_orders and b.id in rules_orders:
                if rules_orders[a.id] < rules_orders[b.id]:
                    return -1
                return 1
            if a.id in rules_orders:
                return -1
            elif b.id in rules_orders:
                return 1

            if a.rule_order < b.rule_order:
                return -1
            return 1

        return key

    def bulk_reorder_rules(self, policy_type: str, rules_orders: dict[str, int]) -> Box:
        """
        Bulk change the order of policy rules.

        Args:
            rules_orders (dict(rule_id=>order)):
                A map of rule IDs and orders
            policy_type (str):
                The policy type. Accepted values are:

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


        """
        # Get policy id for specified policy type
        policy_set = self.get_policy(policy_type).id
        all = self.list_rules(policy_type)
        all.sort(key=functools.cmp_to_key(self.sort_key(rules_orders=rules_orders)))
        orderedRules = [r.id for r in all]

        # Construct the URL pathx
        path = f"policySet/{policy_set}/reorder"

        # Create a new PUT request
        resp = self.rest.put(path, json=orderedRules)
        if resp.status_code <= 299:
            # Return the updated rule information
            return None
        else:
            # Handle the case when the request fails (modify as needed)
            return resp

    def delete_rule(self, policy_type: str, rule_id: str) -> int:
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

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zpa.policies.delete_rule(policy_id='99999',
            ...    rule_id='88888')

        """

        # Get policy id for specified policy type
        policy_id = self.get_policy(policy_type).id

        return self.rest.delete(f"policySet/{policy_id}/rule/{rule_id}").status_code
