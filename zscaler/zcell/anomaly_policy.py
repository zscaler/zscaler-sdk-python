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

from typing import List

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url, zcell_params
from zscaler.zcell.models.anomaly_policy import (
    AnomalyPolicy,
    AnomalyPolicyLogContent,
    GetViolationDetails,
)


class AnomalyPolicyAPI(APIClient):

    _zcell_base_endpoint_customer = "/zcell/config/api/v1/customers"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    @zcell_params
    def list_anomaly_policy(
        self, id: str, start_date_time: int = None, end_date_time: int = None, query_params=None
    ) -> APIResult[List[AnomalyPolicy]]:
        """
        Get all Anomaly Policies.

        Args:
            id (str): Path parameter.
            start_date_time (int): Window start as epoch seconds. Required unless ``days`` is supplied.
            end_date_time (int): Window end as epoch seconds. Required unless ``days`` is supplied.
            days (int): Convenience shorthand — sets a [now - days, now] start_date_time/end_date_time epoch-seconds window.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.policy_type]`` {str}
                ``[query_params.page]`` {int}: Page number (0-based)
                ``[query_params.size]`` {int}: Page size (1-100)
                ``[query_params.sort_by]`` {str}: Field to sort by. Default: policyName. Sortable fields: id,
                  policyType, policyName, violations
                ``[query_params.sort_dir]`` {str}: ASC or DESC. Default: ASC

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            List all anomaly policies for a customer using the ``days`` shorthand
            (the ``@zcell_params`` decorator turns it into a ``startDateTime`` /
            ``endDateTime`` epoch-seconds window of ``[now - days, now]``)::

                >>> list_policies, _, err = client.zcell.anomaly_policy.list_anomaly_policy(
                ...     id='gi754cvqb07r0',
                ...     days=7,
                ... )
                >>> if err:
                ...     print(f"Error listing anomaly policies: {err}")
                ...     return
                >>> print(f"Total anomaly policies found: {len(list_policies)}")
                >>> for policy in list_policies:
                ...     print(policy.as_dict())

            Filter by policy name (client-side ``name`` filter via ``query_params``)::

                >>> policy_list, _, err = client.zcell.anomaly_policy.list_anomaly_policy(
                ...     id='gi754cvqb07r0',
                ...     query_params={'name': 'PolicyRule01_2451'},
                ...     days=7,
                ... )
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/anomaly-policy")

        query_params = query_params or {}
        if start_date_time is not None:
            query_params["start_date_time"] = start_date_time
        if end_date_time is not None:
            query_params["end_date_time"] = end_date_time

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
                result.append(AnomalyPolicy(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def create_anomaly_policy(self, id: str, **kwargs) -> APIResult[AnomalyPolicy]:
        """
        Create a new Anomaly Policy.

        Args:
            id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            Create a new GeoFencing anomaly policy::

                >>> added_policy, _, error = client.zcell.anomaly_policy.create_anomaly_policy(
                ...     id='gi754cvqb07r0',
                ...     policy_name='PolicyRule01_2451',
                ...     policy_type='GEOFENCING',
                ...     sim_location_groups_ids=['219'],
                ... )
                >>> if error:
                ...     print(f"Error adding anomaly policy: {error}")
                ...     return
                >>> print(f"Anomaly Policy added successfully: {added_policy.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/anomaly-policy")

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AnomalyPolicy)
        if error:
            return (None, response, error)
        try:
            result = AnomalyPolicy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_anomaly_policy(self, id: str, policy_id: str, **kwargs) -> APIResult[AnomalyPolicy]:
        """
        Update an existing Anomaly Policy.

        Args:
            id (str): Path parameter.
            policy_id (str): Path parameter.
            **kwargs: Request body fields.

        Returns:
            tuple: (result, Response, error)

        Examples:
            Update an existing anomaly policy::

                >>> updated_policy, _, error = client.zcell.anomaly_policy.update_anomaly_policy(
                ...     id='gi754cvqb07r0',
                ...     policy_id=added_policy.id,
                ...     policy_name='PolicyRule01_2451',
                ...     sim_location_groups_ids=['219'],
                ... )
                >>> if error:
                ...     print(f"Error updating Anomaly Policy: {error}")
                ...     return
                >>> print(f"Anomaly Policy updated successfully: {updated_policy.as_dict()}")
        """
        http_method = "patch".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/anomaly-policy/{policy_id}")

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AnomalyPolicy)
        if error:
            return (None, response, error)

        try:
            result = AnomalyPolicy(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_anomaly_policy(self, id: str, policy_id: str) -> APIResult[None]:
        """
        Delete an Anomaly Policy.

        Args:
            id (str): Path parameter.
            policy_id (str): Path parameter.
        Returns:
            tuple: (None, Response, error)

        Examples:
            Delete an anomaly policy::

                >>> _, _, error = client.zcell.anomaly_policy.delete_anomaly_policy(
                ...     id='gi754cvqb07r0',
                ...     policy_id=added_policy.id,
                ... )
                >>> if error:
                ...     print(f"Error deleting anomaly policy: {error}")
                ...     return
        """
        http_method = "delete".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/anomaly-policy/{policy_id}")

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)

    def list_anomaly_policy_logs(self, id: str, policy_id: str, query_params=None) -> APIResult[List[AnomalyPolicyLogContent]]:
        """
        Get Past Anomaly Policy Logs.

        Args:
            id (str): Path parameter.
            policy_id (str): Path parameter.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.page]`` {int}
                ``[query_params.size]`` {int}

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            List the past logs for an anomaly policy::

                >>> audit_log, _, err = client.zcell.anomaly_policy.list_anomaly_policy_logs(
                ...     id='gi754cvqb07r0',
                ...     policy_id='208',
                ... )
                >>> if err:
                ...     print(f"Error listing anomaly policy logs: {err}")
                ...     return
                >>> print(f"Total anomaly policy logs found: {len(audit_log)}")
                >>> for entry in audit_log:
                ...     print(entry.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/anomaly-policy/{policy_id}/logs")

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
                result.append(AnomalyPolicyLogContent(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_anomaly_policy_status(self, id: str, policy_id: str, enabled: bool) -> APIResult:
        """
        Update Anomaly Policy Status (Enable/Disable).

        Args:
            id (str): Path parameter. The customer ID.
            policy_id (str): Path parameter. The anomaly policy ID.
            enabled (bool): Required query parameter. ``True`` enables the policy,
                ``False`` disables it.

        Returns:
            tuple: (result, Response, error)

        Examples:
            Enable an anomaly policy::

                >>> _, response, error = client.zcell.anomaly_policy.update_anomaly_policy_status(
                ...     id='gi754cvqb07r0',
                ...     policy_id='208',
                ...     enabled=True,
                ... )
                >>> if error:
                ...     print(f"Error updating anomaly policy status: {error}")
                ...     return

            Disable an anomaly policy::

                >>> _, response, error = client.zcell.anomaly_policy.update_anomaly_policy_status(
                ...     id='gi754cvqb07r0',
                ...     policy_id='208',
                ...     enabled=False,
                ... )
        """
        http_method = "patch".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/anomaly-policy/{policy_id}/status")

        query_params = {"enabled": str(enabled).lower()}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (response, response, None)

    @zcell_params
    def list_anomaly_policy_violations(
        self, id: str, policy_id: str, start_date_time: int = None, end_date_time: int = None, query_params=None
    ) -> APIResult:
        """
        Get ICCIDs with violations for an anomaly policy.

        Args:
            id (str): Path parameter.
            policy_id (str): Path parameter.
            days (int): Convenience shorthand — sets a [now - days, now] start_date_time/end_date_time epoch-seconds window.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.start_date_time]`` {int}: Required
                ``[query_params.end_date_time]`` {int}: Required
                ``[query_params.page]`` {int}: Page number (0-based)
                ``[query_params.size]`` {int}: Page size (1-100)
                ``[query_params.sort_by]`` {str}: Accepted but ignored on this endpoint
                ``[query_params.sort_dir]`` {str}: Accepted but ignored on this endpoint

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            List the ICCIDs with violations for an anomaly policy (``days``
            shorthand sets the required start/end window)::

                >>> violations, _, err = client.zcell.anomaly_policy.list_anomaly_policy_violations(
                ...     id='gi754cvqb07r0',
                ...     policy_id='208',
                ...     days=14,
                ... )
                >>> if err:
                ...     print(f"Error listing anomaly policy violations: {err}")
                ...     return
                >>> print(f"Total violations found: {len(violations)}")
                >>> for violation in violations:
                ...     print(violation.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/anomaly-policy/{policy_id}/violations")

        query_params = query_params or {}
        if start_date_time is not None:
            query_params["start_date_time"] = start_date_time
        if end_date_time is not None:
            query_params["end_date_time"] = end_date_time

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
                result.append(AnomalyPolicy(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @zcell_params
    def get_anomaly_policy_violations(
        self, id: str, policy_id: str, iccid: str, query_params=None
    ) -> APIResult[List[GetViolationDetails]]:
        """
        Get violations for a specific ICCID.

        Args:
            id (str): Path parameter.
            policy_id (str): Path parameter.
            iccid (str): Path parameter.
            days (int): Convenience shorthand — sets a [now - days, now] start_date_time/end_date_time epoch-seconds window.
            query_params (dict): Map of query parameters for the request.
                ``[query_params.start_date_time]`` {int}: Required
                ``[query_params.end_date_time]`` {int}: Required
                ``[query_params.page]`` {int}: Page number (0-based)
                ``[query_params.size]`` {int}: Page size (1-100)
                ``[query_params.sort_by]`` {str}: Field to sort by. Default: timestamp. Sortable fields: policyId,
                  policyType, timestamp
                ``[query_params.sort_dir]`` {str}: ASC or DESC. Default: DESC

        Returns:
            tuple: (result, Response, error)

        The returned response supports ``resp.search(<jmespath>)`` for client-side filtering/projection of the current page.

        Examples:
            Get the violations for a specific ICCID under an anomaly policy::

                >>> fetched_iccid, _, error = client.zcell.anomaly_policy.get_anomaly_policy_violations(
                ...     id='gi754cvqb07r0',
                ...     policy_id='208',
                ...     iccid='89852350525020079331',
                ...     days=14,
                ... )
                >>> if error:
                ...     print(f"Error fetching ICCID violations: {error}")
                ...     return
                >>> print(f"Total ICCID violations found: {len(fetched_iccid)}")
                >>> for violation in fetched_iccid:
                ...     print(violation.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(f"{self._zcell_base_endpoint_customer}/{id}/anomaly-policy/{policy_id}/violations/{iccid}")

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
                result.append(GetViolationDetails(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
