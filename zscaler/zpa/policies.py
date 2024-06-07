# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import functools

from box import Box, BoxList
from requests import Response

from zscaler.utils import add_id_groups, convert_keys, snake_to_camel
from zscaler.zpa.client import ZPAClient


class PolicySetsAPI:
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

    @staticmethod
    def _create_conditions_v1(conditions: list) -> list:
        """
        Creates a dict template for feeding conditions into the ZPA Policies API when adding or updating a policy.

        Args:
            conditions (list): List of condition dicts or tuples.

        Returns:
            :obj:`dict`: The conditions template.

        """
        template = []
        app_and_app_group_operands = []
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
        }

        for condition in conditions:
            if isinstance(condition, tuple) and len(condition) == 3:
                # Handle each object type according to its pattern
                object_type = condition[0].upper()
                lhs = condition[1]
                rhs = condition[2]

                if object_type in ["APP", "APP_GROUP"]:
                    app_and_app_group_operands.append({"objectType": object_type, "lhs": "id", "rhs": rhs})
                elif object_type in object_types_to_operands:
                    if object_type == "CLIENT_TYPE":
                        if rhs in {
                            "zpn_client_type_exporter",
                            "zpn_client_type_machine_tunnel",
                            "zpn_client_type_ip_anchoring",
                            "zpn_client_type_edge_connector",
                            "zpn_client_type_zapp",
                            "zpn_client_type_slogger",
                        }:
                            object_types_to_operands[object_type].append({"objectType": object_type, "lhs": "id", "rhs": rhs})
                    elif object_type in [
                        "PLATFORM",
                        "POSTURE",
                        "TRUSTED_NETWORK",
                        "SAML",
                        "SCIM",
                        "SCIM_GROUP",
                        "COUNTRY_CODE",
                    ]:
                        object_types_to_operands[object_type].append({"objectType": object_type, "lhs": lhs, "rhs": rhs})
                    else:
                        object_types_to_operands[object_type].append({"objectType": object_type, "lhs": "id", "rhs": rhs})
            elif isinstance(condition, dict):
                # Handle the dictionary logic based on the Go code schema
                condition_template = {}

                # Extracting keys from the condition dictionary
                for key in ["id", "negated", "operator"]:
                    if key in condition:
                        condition_template[key] = condition[key]

                # Handling the operands
                operands = condition.get("operands", [])
                condition_template["operands"] = []

                for operand in operands:
                    operand_template = {}

                    # Extracting keys from the operand dictionary
                    for operand_key in [
                        "id",
                        "idp_id",
                        "name",
                        "lhs",
                        "rhs",
                        "objectType",
                    ]:
                        if operand_key in operand:
                            operand_template[operand_key] = operand[operand_key]

                    condition_template["operands"].append(operand_template)

                template.append(condition_template)

        # Combine APP and APP_GROUP operands into one block
        if app_and_app_group_operands:
            template.append({"operator": "OR", "operands": app_and_app_group_operands})

        # Combine other object types into their own blocks
        for object_type, operands in object_types_to_operands.items():
            if operands:
                template.append({"operator": "OR", "operands": operands})

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

    def get_policy(self, policy_type: str, **kwargs) -> Box:
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
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get(f"policySet/policyType/{mapped_policy_type}", params=params)

    def get_rule(self, policy_type: str, rule_id: str, **kwargs) -> Box:
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
            >>> policy_rule = zpa.policies.get_rule(policy_type='access',
            ...    rule_id='88888')

        """
        policy_id = self.get_policy(policy_type).id

        policy_params = {}
        if "microtenant_id" in kwargs:
            policy_params["microtenantId"] = kwargs.pop("microtenant_id")
        policy_id = self.get_policy(policy_type, **policy_params).id

        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.get(f"policySet/{policy_id}/rule/{rule_id}", params=params)

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
            >>> for policy in zpa.policies.list_rules('access')
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
            :obj:`Box`: The resource record of the newly created access policy rule.

        """
        payload = {
            "name": name,
            "action": action.upper(),
        }

        conditions = kwargs.pop("conditions", [])
        if conditions:
            payload["conditions"] = self._create_conditions_v1(conditions)
        else:
            payload["conditions"] = []

        if app_connector_group_ids:
            payload["appConnectorGroups"] = [{"id": group_id} for group_id in app_connector_group_ids]

        if app_server_group_ids:
            payload["appServerGroups"] = [{"id": group_id} for group_id in app_server_group_ids]

        add_id_groups(self.reformat_params, kwargs, payload)
        policy_id = self.get_policy("access").id

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params)
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_access_rule(
        self,
        rule_id: str,
        app_connector_group_ids: list = None,
        app_server_group_ids: list = None,
        **kwargs,
    ) -> Box:
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
            :obj:`Box`: The  policy-rule resource record.

        Examples:
            Update the name and description of the Access Policy Rule:

            >>> zpa.policies.update_access_rule(
            ...    rule_id="999999",
            ...    name='Update_Access_Policy_Rule_v1',
            ...    description='Update_Access_Policy_Rule_v1',
            ... )
        """
        app_connector_group_ids = app_connector_group_ids or []
        app_server_group_ids = app_server_group_ids or []

        policy_type = "access"

        current_rule = self.get_rule(policy_type, rule_id)
        payload = convert_keys(current_rule)
        kwargs["app_connector_group_ids"] = app_connector_group_ids
        kwargs["app_server_group_ids"] = app_server_group_ids

        add_id_groups(self.reformat_params, kwargs, payload)

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v1(value)
            elif key == "action":
                payload["action"] = value.upper()
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "conditions" not in kwargs:
            payload["conditions"] = []

        policy_id = self.get_policy(policy_type).id
        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v1")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

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
        payload = {
            "name": name,
            "action": "RE_AUTH",
            "conditions": self._create_conditions_v1(kwargs.pop("conditions", [])),
        }
        policy_id = self.get_policy("timeout").id
        payload["reauthTimeout"] = kwargs.get("re_auth_timeout", 172800)
        payload["reauthIdleTimeout"] = kwargs.get("re_auth_idle_timeout", 600)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params)
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_timeout_rule(self, rule_id: str, **kwargs) -> Box:
        """
        Update an existing Timeout Policy Rule rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The only supported action for this policy is RE_AUTH and it's pre-set during the payload submission.

                |  ``RE_AUTH``

            description (str):
                Additional information about the Timeout Policy Rule rule.
            enabled (bool):
                Whether or not the Timeout Policy Rule rule. is enabled.
            rule_order (str):
                The rule evaluation order number of the rule.
            custom_msg (str):
                A custom message.
            description (str):
                A description for the rule.
            re_auth_idle_timeout (int):
                The re-authentication idle timeout value in seconds.
            re_auth_timeout (int):
                The re-authentication timeout value in seconds.
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
            :obj:`Box`: The updated policy-rule resource record.

        Examples:
            Updates the name only for an Timeout Policy Rule rule:

            >>> zpa.policies.update_timeout_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_Timeout_Rule_v1',
            ...    description='Update_Timeout_Rule_v1',
            ...    conditions=[
            ...         ("app", ["216199618143361683"]),
            ...         ("app_group", ["216199618143360301"]),
            ...         ("scim_group", "idp_id", "scim_group_id"),
            ...         ("scim_group", "idp_id", "scim_group_id"),
            ...     ],
            ... )
        """
        policy_type = "timeout"
        current_rule = self.get_rule(policy_type, rule_id)
        payload = convert_keys(current_rule)
        payload["action"] = "RE_AUTH"
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v1(value)
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "conditions" not in kwargs:
            payload["conditions"] = []

        payload["reauthTimeout"] = kwargs.get("re_auth_timeout", 172800)
        payload["reauthIdleTimeout"] = kwargs.get("re_auth_idle_timeout", 600)

        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v1")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

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
            :obj:`Box`: The resource record of the newly created Client Forwarding Policy rule.

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
        payload = {
            "name": name,
            "action": action.upper(),
        }

        conditions = kwargs.pop("conditions", [])
        if conditions:
            payload["conditions"] = self._create_conditions_v1(conditions)
        else:
            payload["conditions"] = []

        policy_id = self.get_policy("client_forwarding").id
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v1")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_client_forwarding_rule(self, rule_id: str, **kwargs) -> Box:
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
            :obj:`Box`: The updated policy-rule resource record.

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
        policy_type = "client_forwarding"

        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()
        current_rule = self.get_rule(policy_type, rule_id)

        payload = convert_keys(current_rule)

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v1(value)
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "conditions" not in kwargs:
            payload["conditions"] = []

        payload["action"] = action
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v1")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

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
        payload = {
            "name": name,
            "action": action.upper(),
            "zpnIsolationProfileId": zpn_isolation_profile_id,
        }
        conditions = kwargs.pop("conditions", [])
        if conditions:
            payload["conditions"] = self._create_conditions_v1(conditions)
        else:
            payload["conditions"] = []

        client_type_present = any(
            cond.get("operands", [{}])[0].get("objectType", "") == "CLIENT_TYPE" for cond in payload["conditions"]
        )
        if not client_type_present:
            payload["conditions"].append(
                {"operator": "OR", "operands": [{"objectType": "CLIENT_TYPE", "lhs": "id", "rhs": "zpn_client_type_exporter"}]}
            )

        policy_id = self.get_policy("isolation").id

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", params=params, json=payload, api_version="v1")
        if isinstance(response, Response):
            status_code = response.status_code
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
        policy_type = "isolation"
        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()
        current_rule = self.get_rule(policy_type, rule_id)
        payload = convert_keys(current_rule)

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v1(value)
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        if "conditions" not in kwargs:
            payload["conditions"] = []

        client_type_present = any(
            cond.get("operands", [{}])[0].get("objectType", "") == "CLIENT_TYPE" for cond in payload["conditions"]
        )
        if not client_type_present:
            payload["conditions"].append(
                {"operator": "OR", "operands": [{"objectType": "CLIENT_TYPE", "lhs": "id", "rhs": "zpn_client_type_exporter"}]}
            )
        payload["action"] = action
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v1")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

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
        payload = {
            "name": name,
            "action": action.upper(),
            "zpnInspectionProfileId": zpn_inspection_profile_id,
        }

        conditions = kwargs.pop("conditions", [])
        if conditions:
            payload["conditions"] = self._create_conditions_v1(conditions)
        else:
            payload["conditions"] = []

        policy_id = self.get_policy("inspection").id
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v1")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_app_protection_rule(self, rule_id: str, **kwargs) -> Box:
        """
        Update an existing App Protection Policy Rule rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``inspect``
                |  ``bypass_inspect``
            description (str):
                Additional information about the App Protection Policy Rule rule.
            enabled (bool):
                Whether or not the App Protection Policy Rule rule. is enabled.
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
            :obj:`Box`: The updated policy-rule resource record.

        Examples:
            Updates the name only for an App Protection Policy Rule rule:

            >>> zpa.policies.update_app_protection_rule(
            ...    rule_id='216199618143320419',
            ...    name='Update_App_Protection_Rule_v1',
            ...    description='Update_App_Protection_Rule_v1',
            ...    action='bypass_inspect',
            ...    conditions=[
            ...         ("app", ["216199618143361683"]),
            ...         ("app_group", ["216199618143360301"]),
            ...         ("scim_group", "idp_id", "scim_group_id"),
            ...         ("scim_group", "idp_id", "scim_group_id"),
            ...     ],
            ... )
        """
        policy_type = "inspection"
        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()
        current_rule = self.get_rule(policy_type, rule_id)

        payload = convert_keys(current_rule)

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v1(value)
            else:
                payload[snake_to_camel(key)] = value

        if "conditions" not in kwargs:
            payload["conditions"] = []

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload["action"] = action
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v1")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def add_access_rule_v2(
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
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        if app_connector_group_ids:
            payload["appConnectorGroups"] = [{"id": group_id} for group_id in app_connector_group_ids]

        if app_server_group_ids:
            payload["appServerGroups"] = [{"id": group_id} for group_id in app_server_group_ids]

        add_id_groups(self.reformat_params, kwargs, payload)

        policy_id = self.get_policy("access").id
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v2")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_access_rule_v2(
        self,
        rule_id: str,
        app_connector_group_ids: list = None,
        app_server_group_ids: list = None,
        **kwargs,
    ) -> Box:
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
            :obj:`Box`: The updated policy-rule resource record.

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
        app_connector_group_ids = app_connector_group_ids or []
        app_server_group_ids = app_server_group_ids or []

        policy_type = "access"

        current_rule = self.get_rule(policy_type, rule_id)
        payload = convert_keys(current_rule)

        if "conditions" in payload and "conditions" not in kwargs:
            del payload["conditions"]

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)
            elif key == "action":
                payload["action"] = value.upper()
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        add_id_groups(self.reformat_params, kwargs, payload)
        payload = {k: v for k, v in payload.items() if k != "conditions" or v}
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v2")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def add_timeout_rule_v2(self, name: str, **kwargs) -> Box:
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
        payload = {
            "name": name,
            "action": "RE_AUTH",
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        policy_id = self.get_policy("timeout").id
        payload["reauthTimeout"] = kwargs.get("re_auth_timeout", 172800)
        payload["reauthIdleTimeout"] = kwargs.get("re_auth_idle_timeout", 600)

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v2")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_timeout_rule_v2(self, rule_id: str, **kwargs) -> Box:
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
            :obj:`Box`: The updated policy-rule resource record.

        Examples:
            Updates the name only for a Timeout Policy rule:

            >>> zpa.policies.update_timeout_rule('99999', name='new_rule_name')

            Updates the description for a Timeout Policy rule:

            >>> zpa.policies.update_timeout_rule('888888', description='Updated Description')
        """
        policy_type = "timeout"
        kwargs["action"] = "RE_AUTH"

        current_rule = self.get_rule(policy_type, rule_id)

        payload = convert_keys(current_rule)

        if "conditions" in payload and "conditions" not in kwargs:
            del payload["conditions"]

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)
            elif key == "action":
                payload["action"] = value.upper()
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {k: v for k, v in payload.items() if k != "conditions" or v}
        policy_id = self.get_policy(policy_type).id
        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v2")

        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def add_client_forwarding_rule_v2(self, name: str, action: str, **kwargs) -> Box:
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
        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        policy_id = self.get_policy("client_forwarding").id
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v2")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_client_forwarding_rule_v2(self, rule_id: str, **kwargs) -> Box:
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
            ...         ("client_type",
            ...         ['zpn_client_type_edge_connector',
            ...          'zpn_client_type_branch_connector',
            ...          'zpn_client_type_machine_tunnel',
            ...          'zpn_client_type_zapp',
            ...          'zpn_client_type_zapp_partner']),
            ...     ],
            ... )
        """
        policy_type = "client_forwarding"
        current_rule = self.get_rule(policy_type, rule_id)
        payload = convert_keys(current_rule)

        if "conditions" in payload and "conditions" not in kwargs:
            del payload["conditions"]

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)
            elif key == "action":
                payload["action"] = value.upper()
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {k: v for k, v in payload.items() if k != "conditions" or v}
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v2")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def add_isolation_rule_v2(self, name: str, action: str, zpn_isolation_profile_id: str, **kwargs) -> Box:
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
        payload = {
            "name": name,
            "action": action.upper(),
            "zpnIsolationProfileId": zpn_isolation_profile_id,
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        payload["conditions"].append({"operands": [{"objectType": "CLIENT_TYPE", "values": ["zpn_client_type_exporter"]}]})
        policy_id = self.get_policy("isolation").id

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v2")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_isolation_rule_v2(self, rule_id: str, **kwargs) -> Box:
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
        policy_type = "isolation"

        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()
        current_rule = self.get_rule(policy_type, rule_id)

        payload = convert_keys(current_rule)

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload["conditions"].append({"operands": [{"objectType": "CLIENT_TYPE", "values": ["zpn_client_type_exporter"]}]})
        payload["action"] = action

        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v2")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def add_app_protection_rule_v2(self, name: str, action: str, zpn_inspection_profile_id: str, **kwargs) -> Box:
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
        payload = {
            "name": name,
            "action": action.upper(),
            "zpnInspectionProfileId": zpn_inspection_profile_id,
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }
        policy_id = self.get_policy("inspection").id
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v2")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_app_protection_rule_v2(self, rule_id: str, **kwargs) -> Box:
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
        policy_type = "inspection"

        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()
        current_rule = self.get_rule(policy_type, rule_id)

        payload = convert_keys(current_rule)

        if "conditions" in payload and "conditions" not in kwargs:
            del payload["conditions"]

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)
            elif key == "action":
                payload["action"] = value.upper()
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload = {k: v for k, v in payload.items() if k != "conditions" or v}

        payload["action"] = action
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v2")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def add_privileged_credential_rule_v2(self, name: str, credential_id: str, **kwargs) -> Box:
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

        Returns:
            :obj:`Box`: The resource record of the newly created Privileged Remote Access Credential rule.
        """
        payload = {
            "name": name,
            "action": "INJECT_CREDENTIALS",
            "credential": {"id": credential_id},
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
        }

        policy_id = self.get_policy("credential").id

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v2")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_privileged_credential_rule_v2(self, rule_id: str, **kwargs) -> Box:
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
        policy_type = "credential"
        current_rule = self.get_rule(policy_type, rule_id)

        payload = convert_keys(current_rule)

        if "conditions" in payload and "conditions" not in kwargs:
            del payload["conditions"]

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)
            elif key == "credential_id":
                payload["credential"] = {"id": value}
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload["action"] = "INJECT_CREDENTIALS"
        payload = {k: v for k, v in payload.items() if k != "conditions" or v}
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v2")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def add_capabilities_rule_v2(self, name: str, **kwargs) -> Box:
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
            :obj:`Box`: The resource record of the newly created Capabilities rule.

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

            # Handling the edge case for file_upload
            if priv_caps_map.get("file_upload") is True:
                capabilities.append("FILE_UPLOAD")
            elif priv_caps_map.get("file_upload") is False:
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

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        policy_id = self.get_policy("capabilities").id

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v2")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_capabilities_rule_v2(self, rule_id: str, **kwargs) -> Box:
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
            :obj:`Box`: The updated policy-capability-rule resource record.

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
        policy_type = "capabilities"

        current_rule = self.get_rule(policy_type, rule_id)
        payload = convert_keys(current_rule)

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

                # Handling the edge case for file_upload
                if priv_caps_map.get("file_upload") is True:
                    capabilities.append("FILE_UPLOAD")
                elif priv_caps_map.get("file_upload") is False:
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

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload["action"] = "CHECK_CAPABILITIES"

        payload = {k: v for k, v in payload.items() if k != "conditions" or v}
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v2")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def add_redirection_rule_v2(self, name: str, action: str, service_edge_group_ids: list = [], **kwargs) -> Box:
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
            :obj:`Box`: The resource record of the newly created Redirection Policy rule.

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

        payload = {
            "name": name,
            "action": action.upper(),
            "conditions": self._create_conditions_v2(kwargs.pop("conditions", [])),
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

        policy_id = self.get_policy("redirection").id

        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload, params=params, api_version="v2")
        if isinstance(response, Response):
            status_code = response.status_code
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_redirection_rule_v2(self, rule_id: str, **kwargs) -> Box:
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
            :obj:`Box`: The updated policy-rule resource record.

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
        policy_type = "redirection"

        if "action" not in kwargs:
            raise ValueError("The 'action' attribute is mandatory.")

        action = kwargs.pop("action").upper()
        current_rule = self.get_rule(policy_type, rule_id)

        payload = convert_keys(current_rule)

        if "conditions" in payload and "conditions" not in kwargs:
            del payload["conditions"]

        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions_v2(value)
            else:
                payload[snake_to_camel(key)] = value

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        payload["action"] = action
        payload = {k: v for k, v in payload.items() if k != "conditions" or v}
        policy_id = self.get_policy(policy_type).id

        response = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload, params=params, api_version="v2")
        if response.status_code == 204:
            updated_rule = self.get_rule(policy_type, rule_id)
            if not updated_rule:
                raise Exception(f"Failed to retrieve the updated rule with ID {rule_id}")
            return updated_rule
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def reorder_rule(self, policy_type: str, rule_id: str, rule_order: str, **kwargs) -> Box:
        """
        Change the order of an existing policy rule.

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

            rule_id (str): The unique ID of the rule that will be reordered.
            rule_order (str): The new order for the rule.
            **kwargs: Optional keyword arguments.
                microtenant_id (str): The ID of the microtenant, if applicable.

        Returns:
            Box: The updated policy rule resource record.

        Raises:
            Exception: If the API call fails, an exception is raised with the response status code.

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
        policy_id = self.get_policy(policy_type).id

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        resp = self.rest.put(
            f"policySet/{policy_id}/rule/{rule_id}/reorder/{rule_order}", params=params, api_version="v1"
        ).status_code
        if resp == 204:
            return self.get_rule(policy_type, rule_id)
        else:
            raise Exception(f"API call failed with status {resp}")

    def bulk_reorder_rules(self, policy_type: str, rules_orders: list[str], **kwargs) -> Box:
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
                microtenant_id (str): The ID of the microtenant, if applicable.

        Returns:
            Box: The response object from the API if the reorder is successful.

        Raises:
            Exception: If the API call fails, an exception is raised with the response status code and message.

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
        policy_set = self.get_policy(policy_type).id
        path = f"policySet/{policy_set}/reorder"

        microtenant_id = kwargs.pop("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}
        response = self.rest.put(path, json=rules_orders, params=params, api_version="v1")
        if response.status_code == 204:
            return Box({})
        elif response.status_code <= 299:
            return None
        else:
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

    def delete_rule(self, policy_type: str, rule_id: str, **kwargs) -> int:
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
            >>> zpa.policies.delete_rule(policy_type='access',
            ...    rule_id='88888')

        """
        policy_id = self.get_policy(policy_type).id
        params = {}
        if "microtenant_id" in kwargs:
            params["microtenantId"] = kwargs.pop("microtenant_id")
        return self.rest.delete(f"policySet/{policy_id}/rule/{rule_id}", params=params).status_code
