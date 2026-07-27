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

from zscaler.aiguard.models.policies import Policies
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.types import APIResult
from zscaler.utils import format_url


class PoliciesAPI(APIClient):
    """
    A Client object for the AI Guard Detection Policies resource.
    """

    _aiguard_base_endpoint = "/aiguard/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_policies(self, query_params: Optional[dict] = None) -> APIResult[List[Policies]]:
        """
        Lists the detection policies configured in your organization.

        Args:
            query_params {dict}: Map of query parameters for the request.

        Returns:
            tuple: A tuple containing (list of Policies instances, Response, error)

        Examples:
            List detection policies:

            >>> policy_list, _, error = client.aiguard.policies.list_policies()
            >>> if error:
            ...     print(f"Error listing detection policies: {error}")
            ...     return
            ... print(f"Total detection policies found: {len(policy_list)}")
            ... for policy in policy_list:
            ...     print(policy.as_dict())

            Client-side filtering with JMESPath:

            The response object supports client-side filtering and
            projection via ``resp.search(expression)``.  See the
            `JMESPath documentation <https://jmespath.org/>`_ for
            expression syntax.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policies
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
                result.append(Policies(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_policy(self, policy_id: int) -> APIResult[Policies]:
        """
        Fetches a specific detection policy by ID.

        Args:
            policy_id (int): The unique identifier for the detection policy.

        Returns:
            tuple: A tuple containing (Policies instance, Response, error).

        Examples:
            Print a specific detection policy:

            >>> fetched_policy, _, error = client.aiguard.policies.get_policy(1013)
            >>> if error:
            ...     print(f"Error fetching detection policy by ID: {error}")
            ...     return
            ... print(f"Fetched detection policy by ID: {fetched_policy.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policies/{policy_id}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Policies)
        if error:
            return (None, response, error)

        try:
            result = Policies(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_policy_by_name(self, name: str) -> APIResult[Policies]:
        """
        Fetches a specific detection policy by name.

        Args:
            name (str): The name of the detection policy.

        Returns:
            tuple: A tuple containing (Policies instance, Response, error).

        Examples:
            Print a specific detection policy by name:

            >>> fetched_policy, _, error = client.aiguard.policies.get_policy_by_name('Policy01')
            >>> if error:
            ...     print(f"Error fetching detection policy by name: {error}")
            ...     return
            ... print(f"Fetched detection policy by name: {fetched_policy.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policies/name/{name}
        """)

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Policies)
        if error:
            return (None, response, error)

        try:
            result = Policies(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_policy(self, **kwargs) -> APIResult[Policies]:
        """
        Creates a new detection policy.

        Args:
            name (str): The name of the detection policy.
            **kwargs: Optional keyword args.

        Keyword Args:
            version (str): The version for this detection policy.
            description (str): Additional information about the detection policy.
            input_detector_policies (str): The input detector policies for this detection policy.
            output_detector_policies (str): The output detector policies for this detection policy.

        Returns:
            tuple: A tuple containing the newly added Policies instance, response, and error.

        Examples:
            Add a new detection policy with input and output detectors:

            >>> added_policy, _, error = client.aiguard.policies.add_policy(
            ...     name="PolicyRule01",
            ...     inputDetectorPolicies=[
            ...         {
            ...             "detector": "toxicity",
            ...             "enabled": True,
            ...             "severity": "HIGH",
            ...             "configuration": {"action": "BLOCK", "threshold": 0.87},
            ...         },
            ...         {
            ...             "detector": "prompt_injection",
            ...             "enabled": True,
            ...             "severity": "CRITICAL",
            ...             "configuration": {"action": "BLOCK", "threshold": 0.75},
            ...         },
            ...     ],
            ...     outputDetectorPolicies=[
            ...         {
            ...             "detector": "pii",
            ...             "enabled": False,
            ...             "severity": "CRITICAL",
            ...             "configuration": {
            ...                 "entities": [
            ...                     {"action": "BLOCK", "entityType": "CREDIT_CARD"},
            ...                     {"action": "BLOCK", "entityType": "US_SSN"},
            ...                     {"action": "DETECT", "entityType": "EMAIL_ADDRESS"},
            ...                 ],
            ...                 "threshold": 0.5,
            ...                 "anonymization": "NONE",
            ...                 "defaultAction": "BLOCK",
            ...                 "replaceWithMaskedContent": False,
            ...             },
            ...         },
            ...     ],
            ... )
            >>> if error:
            ...     print(f"Error adding detection policy: {error}")
            ...     return
            ... print(f"Detection policy added successfully: {added_policy.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policies
        """)

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Policies)
        if error:
            return (None, response, error)

        try:
            result = Policies(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_policy(self, policy_id: int, **kwargs) -> APIResult[Policies]:
        """
        Updates information for the specified detection policy.

        Args:
            policy_id (int): The unique identifier for the detection policy.

        Keyword Args:
            name (str): The name of the detection policy.
            version (str): The version for this detection policy.
            description (str): Additional information about the detection policy.
            input_detector_policies (str): The input detector policies for this detection policy.
            output_detector_policies (str): The output detector policies for this detection policy.

        Returns:
            tuple: A tuple containing the updated Policies instance, response, and error.

        Examples:
            Update an existing detection policy. The update replaces the policy, so the
            detector lists are sent in full:

            >>> updated_policy, _, error = client.aiguard.policies.update_policy(
            ...     policy_id=2916,
            ...     name="PolicyRule01",
            ...     inputDetectorPolicies=[
            ...         {
            ...             "detector": "toxicity",
            ...             "enabled": True,
            ...             "severity": "HIGH",
            ...             "configuration": {"action": "BLOCK", "threshold": 0.87},
            ...         },
            ...     ],
            ...     outputDetectorPolicies=[
            ...         {
            ...             "detector": "toxicity",
            ...             "enabled": True,
            ...             "severity": "CRITICAL",
            ...             "configuration": {"action": "BLOCK", "threshold": 0.87},
            ...         },
            ...     ],
            ... )
            >>> if error:
            ...     print(f"Error updating detection policy: {error}")
            ...     return
            ... print(f"Detection policy updated successfully: {updated_policy.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policies/{policy_id}
        """)
        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Policies)
        if error:
            return (None, response, error)

        try:
            result = Policies(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_policy(self, policy_id: int) -> APIResult[None]:
        """
        Deletes the specified detection policy.

        Args:
            policy_id (int): The unique identifier for the detection policy.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a detection policy:

            >>> _, _, error = client.aiguard.policies.delete_policy(1013)
            >>> if error:
            ...     print(f"Error deleting detection policy: {error}")
            ...     return
            ... print(f"Detection policy deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._aiguard_base_endpoint}
            /detections/policies/{policy_id}
        """)

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
