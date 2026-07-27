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
from zscaler.types import APIResult
from zscaler.utils import format_url
from zscaler.zia.models.endpoint_dlp_rules import SubRule


class EndpointDLPSubRulesAPI(APIClient):
    """
    A Client object for the Endpoint DLP Sub-Rules resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def add_sub_rule(self, rule_id: int, **kwargs) -> APIResult[SubRule]:
        """
        Creates a new sub-rule under the specified parent Endpoint DLP rule.

        Args:
            rule_id (int): The unique identifier for the parent Endpoint DLP rule.
            name (str): The name of the endpoint DLP sub-rule.
            **kwargs: Optional keyword args.

        Keyword Args:
            state (str): The endpoint DLP sub-rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            order (int): The order of the endpoint DLP sub-rule, defaults to adding the endpoint DLP sub-rule to the bottom of the list.
            rank (int): The admin rank of the endpoint DLP sub-rule.
            file_types (str): The file types for this endpoint DLP sub-rule. Accepted values include e.g. ``ANY``.
            data_transfer_method (str): The data transfer method for this endpoint DLP sub-rule. Accepted values include e.g. ``NETWORK_DRIVE_TRANSFER``.
            description (str): Additional information about the endpoint DLP sub-rule.
            min_size (int): The min size for this endpoint DLP sub-rule.
            action (str): The action taken when traffic matches the endpoint DLP sub-rule criteria.
            external_auditor_email (str): The email address of an external auditor to whom DLP email notifications are sent.
            parent_rule (int): The parent rule for this endpoint DLP sub-rule.
            severity (str): The severity level assigned to the endpoint DLP sub-rule.
            eun_enabled (bool): A Boolean value indicating whether eun is enabled for this endpoint DLP sub-rule.
            eun_template_id (int): The eun template id for this endpoint DLP sub-rule.
            uc_template_id (int): The uc template id for this endpoint DLP sub-rule.
            network_type (str): The network type for this endpoint DLP sub-rule. Accepted values include e.g. ``TRUSTED``.
            without_content_inspection (bool): A Boolean value indicating whether without content inspection applies to this endpoint DLP sub-rule.
            dlp_engines (list): The IDs for the dlp engines that this endpoint DLP sub-rule applies to.
            users (list): The IDs for the users that this endpoint DLP sub-rule applies to.
            groups (list): The IDs for the groups that this endpoint DLP sub-rule applies to.
            departments (list): The IDs for the departments that this endpoint DLP sub-rule applies to.
            devices (list): The IDs for the devices that this endpoint DLP sub-rule applies to.
            device_groups (list): The IDs for the device groups that this endpoint DLP sub-rule applies to.
            device_trust_levels (list): The list of device trust levels for this endpoint DLP sub-rule. Accepted values include e.g. ``ANY``.
            time_windows (list): The IDs for the time windows that this endpoint DLP sub-rule applies to.
            labels (list): The IDs for the labels that this endpoint DLP sub-rule applies to.
            end_point_applications (list): The list of end point applications for this endpoint DLP sub-rule.
            end_point_application_groups (list): The list of end point application groups for this endpoint DLP sub-rule.
            resources (list): The IDs for the resources that this endpoint DLP sub-rule applies to.
            resource_groups (list): The IDs for the resource groups that this endpoint DLP sub-rule applies to.
            user_risk_score_levels (list): The list of user risk score levels for this endpoint DLP sub-rule. Accepted values include e.g. ``ANY``.
            notification_template (dict): The ID of the notification template for this endpoint DLP sub-rule, e.g. ``{'id': 12345}``.
            auditor (dict): The ID of the auditor for this endpoint DLP sub-rule, e.g. ``{'id': 12345}``.
            receiver (dict): The ID of the receiver for this endpoint DLP sub-rule, e.g. ``{'id': 12345}``.

        Returns:
            tuple: A tuple containing the newly added SubRule instance, response, and error.

        Examples:
            Add a new endpoint DLP sub-rule:

            >>> added_sub_rule, _, error = client.zia.endpoint_dlp_sub_rules.add_sub_rule(
            ...     1013,
            ...     name=f"NewSubRule_{random.randint(1000, 10000)}",
            ...     description=f"NewSubRule_{random.randint(1000, 10000)}",
            ...     state='ENABLED',
            ...     action='ALLOW',
            ...     order=1,
            ...     rank=7,
            ...     device_trust_levels=['ANY'],
            ... )
            >>> if error:
            ...     print(f"Error adding endpoint DLP sub-rule: {error}")
            ...     return
            ... print(f"Endpoint dlp sub-rule added successfully: {added_sub_rule.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules/{rule_id}/subRule
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SubRule)
        if error:
            return (None, response, error)

        try:
            result = SubRule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_sub_rule(self, rule_id: int, sub_rule_id: int, **kwargs) -> APIResult[SubRule]:
        """
        Updates the specified sub-rule of the parent Endpoint DLP rule.

        Args:
            rule_id (int): The unique identifier for the parent Endpoint DLP rule.
            sub_rule_id (int): The unique identifier for the endpoint DLP sub-rule.

        Keyword Args:
            name (str): The name of the endpoint DLP sub-rule.
            state (str): The endpoint DLP sub-rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            order (int): The order of the endpoint DLP sub-rule, defaults to adding the endpoint DLP sub-rule to the bottom of the list.
            rank (int): The admin rank of the endpoint DLP sub-rule.
            file_types (str): The file types for this endpoint DLP sub-rule. Accepted values include e.g. ``ANY``.
            data_transfer_method (str): The data transfer method for this endpoint DLP sub-rule. Accepted values include e.g. ``NETWORK_DRIVE_TRANSFER``.
            description (str): Additional information about the endpoint DLP sub-rule.
            min_size (int): The min size for this endpoint DLP sub-rule.
            action (str): The action taken when traffic matches the endpoint DLP sub-rule criteria.
            external_auditor_email (str): The email address of an external auditor to whom DLP email notifications are sent.
            parent_rule (int): The parent rule for this endpoint DLP sub-rule.
            severity (str): The severity level assigned to the endpoint DLP sub-rule.
            eun_enabled (bool): A Boolean value indicating whether eun is enabled for this endpoint DLP sub-rule.
            eun_template_id (int): The eun template id for this endpoint DLP sub-rule.
            uc_template_id (int): The uc template id for this endpoint DLP sub-rule.
            network_type (str): The network type for this endpoint DLP sub-rule. Accepted values include e.g. ``TRUSTED``.
            without_content_inspection (bool): A Boolean value indicating whether without content inspection applies to this endpoint DLP sub-rule.
            dlp_engines (list): The IDs for the dlp engines that this endpoint DLP sub-rule applies to.
            users (list): The IDs for the users that this endpoint DLP sub-rule applies to.
            groups (list): The IDs for the groups that this endpoint DLP sub-rule applies to.
            departments (list): The IDs for the departments that this endpoint DLP sub-rule applies to.
            devices (list): The IDs for the devices that this endpoint DLP sub-rule applies to.
            device_groups (list): The IDs for the device groups that this endpoint DLP sub-rule applies to.
            device_trust_levels (list): The list of device trust levels for this endpoint DLP sub-rule. Accepted values include e.g. ``ANY``.
            time_windows (list): The IDs for the time windows that this endpoint DLP sub-rule applies to.
            labels (list): The IDs for the labels that this endpoint DLP sub-rule applies to.
            end_point_applications (list): The list of end point applications for this endpoint DLP sub-rule.
            end_point_application_groups (list): The list of end point application groups for this endpoint DLP sub-rule.
            resources (list): The IDs for the resources that this endpoint DLP sub-rule applies to.
            resource_groups (list): The IDs for the resource groups that this endpoint DLP sub-rule applies to.
            user_risk_score_levels (list): The list of user risk score levels for this endpoint DLP sub-rule. Accepted values include e.g. ``ANY``.
            notification_template (dict): The ID of the notification template for this endpoint DLP sub-rule, e.g. ``{'id': 12345}``.
            auditor (dict): The ID of the auditor for this endpoint DLP sub-rule, e.g. ``{'id': 12345}``.
            receiver (dict): The ID of the receiver for this endpoint DLP sub-rule, e.g. ``{'id': 12345}``.

        Returns:
            tuple: A tuple containing the updated SubRule instance, response, and error.

        Examples:
            Update an existing endpoint DLP sub-rule:

            >>> updated_sub_rule, _, error = client.zia.endpoint_dlp_sub_rules.update_sub_rule(
            ...     1013,
            ...     sub_rule_id=1013,
            ...     name=f"UpdatedSubRule_{random.randint(1000, 10000)}",
            ...     description=f"UpdatedSubRule_{random.randint(1000, 10000)}",
            ...     state='ENABLED',
            ...     action='ALLOW',
            ... )
            >>> if error:
            ...     print(f"Error updating endpoint DLP sub-rule: {error}")
            ...     return
            ... print(f"Endpoint dlp sub-rule updated successfully: {updated_sub_rule.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules/{rule_id}/subRule/{sub_rule_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, SubRule)
        if error:
            return (None, response, error)

        try:
            result = SubRule(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_sub_rule(self, rule_id: int, sub_rule_id: int) -> APIResult[None]:
        """
        Deletes the specified sub-rule of the parent Endpoint DLP rule.

        Args:
            rule_id (int): The unique identifier for the parent Endpoint DLP rule.
            sub_rule_id (int): The unique identifier for the endpoint DLP sub-rule.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a endpoint DLP sub-rule:

            >>> _, _, error = client.zia.endpoint_dlp_sub_rules.delete_sub_rule(1013, 1013)
            >>> if error:
            ...     print(f"Error deleting endpoint DLP sub-rule: {error}")
            ...     return
            ... print(f"Endpoint dlp sub-rule deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._zia_base_endpoint}
            /endPointDlpRules/{rule_id}/subRule/{sub_rule_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
