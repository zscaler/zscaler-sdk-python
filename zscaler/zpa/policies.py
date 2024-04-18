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
        "timeout": "TIMEOUT_POLICY",
        "client_forwarding": "CLIENT_FORWARDING_POLICY",
        "isolation": "ISOLATION_POLICY",
        "inspection": "INSPECTION_POLICY",
        "siem": "SIEM_POLICY",
    }

    reformat_params = [
        ("app_server_group_ids", "appServerGroups"),
        ("app_connector_group_ids", "appConnectorGroups"),
    ]

    @staticmethod
    def _create_conditions(conditions: list):
        """
        Creates a dict template for feeding conditions into the ZPA Policies API when adding or updating a policy.

        Args:
            conditions (list): List of condition dicts or tuples.

        Returns:
            :obj:`dict`: The conditions template.

        """
        template = []

        for condition in conditions:
            if isinstance(condition, tuple) and len(condition) == 3:
                # Previous tuple logic
                operand = {
                    "operands": [
                        {
                            "objectType": condition[0].upper(),
                            "lhs": condition[1],
                            "rhs": condition[2],
                        }
                    ]
                }
                template.append(operand)
            elif isinstance(condition, dict):
                # New dictionary logic based on Go code schema
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

        return template

    def get_policy(self, policy_type: str) -> Box:
        """
        Returns the policy and rule sets for the given policy type.

        Args:
            policy_type (str): The type of policy to be returned. Accepted values are:

                 |  ``access`` - returns the Access Policy
                 |  ``timeout`` - returns the Timeout Policy
                 |  ``client_forwarding`` - returns the Client Forwarding Policy
                 |  ``isolation`` - returns the Isolation Policy
                 |  ``inspection`` - returns the Inspection Policy
                 |  ``siem`` - returns the SIEM Policy

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
                 |  ``timeout``
                 |  ``client_forwarding``
                 |  ``siem``
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

    def delete_rule(self, policy_type: str, rule_id: str) -> int:
        """
        Deletes the specified policy rule.

        Args:
            policy_type (str):
                The type of policy the rule belongs to. Accepted values are:

                 |  ``access``
                 |  ``timeout``
                 |  ``client_forwarding``
                 |  ``siem``
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

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

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

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

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

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

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

        # Get the policy id of the provided policy type for the URL.
        policy_id = self.get_policy("isolation").id

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

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

        response = self.rest.post(f"policySet/{policy_id}/rule", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_rule(self, policy_type: str, rule_id: str, **kwargs) -> Box:
        """
        Update an existing policy rule.

        Ensure you are using the correct arguments for the policy type that you want to update.

        Args:
            policy_type (str):
                The policy type. Accepted values are:

                 |  ``access``
                 |  ``timeout``
                 |  ``client_forwarding``
            rule_id (str):
                The unique identifier for the rule to be updated.
            **kwargs:
                Optional keyword args.

        Keyword Args:
            action (str):
                The action for the policy. Accepted values are:

                |  ``allow``
                |  ``deny``
                |  ``intercept``
                |  ``intercept_accessible``
                |  ``bypass``
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
            Updates the name only for an Access Policy rule:

            >>> zpa.policies.update_rule('access', '99999', name='new_rule_name')

            Updates the action only for a Client Forwarding Policy rule:

            >>> zpa.policies.update_rule('client_forwarding', '888888', action='BYPASS')

        """
        # Get policy id for specified policy type
        policy_id = self.get_policy(policy_type).id

        payload = convert_keys(self.get_rule(policy_type, rule_id))

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key == "conditions":
                payload["conditions"] = self._create_conditions(value)
            else:
                payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_rule(policy_type, rule_id)

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
                ...
            rule_id (str):
                ...
            **kwargs:
                ...

        Keyword Args:
            ...
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

        resp = self.rest.put(f"policySet/{policy_id}/rule/{rule_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_rule(policy_type, rule_id)

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

                 |  ``access``
                 |  ``timeout``
                 |  ``client_forwarding``

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

        resp = self._put(f"policySet/{policy_id}/rule/{rule_id}/reorder/{rule_order}").status_code

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

                 |  ``access``
                 |  ``timeout``
                 |  ``client_forwarding``

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
