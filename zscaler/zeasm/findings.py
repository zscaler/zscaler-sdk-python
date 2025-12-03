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

from typing import Dict, List, Optional, Any, Union
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zeasm.models.findings import CommonFindings, Findings, FindingDetails
from zscaler.utils import format_url
from zscaler.types import APIResult


class FindingsAPI(APIClient):
    """
    A Client object for the ZEASM Findings resource.

    This class provides methods to interact with ZEASM findings,
    allowing you to retrieve findings identified and tracked for an
    organization's internet-facing assets scanned by EASM.
    """

    _zeasm_base_endpoint = "/easm/easm-ui/v1"

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_findings(self, org_id: str) -> APIResult[Findings]:
        """
        Retrieves the list of findings identified and tracked for an organization's
        internet-facing assets scanned by EASM.

        Args:
            org_id (str): The unique identifier for the organization.

        Returns:
            tuple: A tuple containing:
                - Findings: Object containing results list and total_results count
                - Response: The raw API response object
                - error: Any error that occurred, or None if successful

        Examples:
            List all findings for an organization::

                >>> findings, _, err = client.zeasm.findings.list_findings(
                ...     org_id="3f61a446-1a0d-11f0-94e8-8a5f4d45e80c"
                ... )
                >>> if err:
                ...     print(f"Error: {err}")
                ...     return
                >>> print(f"Total findings: {findings.total_results}")
                >>> for finding in findings.results:
                ...     print(f"  ID: {finding.id}, Category: {finding.category}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zeasm_base_endpoint}
            /organizations/{org_id}/findings
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = Findings(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_finding_details(self, org_id: str, finding_id: str) -> APIResult[FindingDetails]:
        """
        Retrieves details for a finding based on the specified ID.

        Args:
            org_id (str): The unique identifier for the organization.
            finding_id (str): The unique identifier for the finding.

        Returns:
            tuple: A tuple containing:
                - FindingDetails: Object containing the finding details
                - Response: The raw API response object
                - error: Any error that occurred, or None if successful

        Examples:
            Get details for a specific finding::

                >>> finding, _, err = client.zeasm.findings.get_finding_details(
                ...     org_id="3f61a446-1a0d-11f0-94e8-8a5f4d45e80c",
                ...     finding_id="8abfc6a2b3058cb75de44c4c65ca4641"
                ... )
                >>> if err:
                ...     print(f"Error: {err}")
                ...     return
                >>> print(finding.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zeasm_base_endpoint}
            /organizations/{org_id}/findings/{finding_id}/details
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, FindingDetails)
        if error:
            return (None, response, error)

        try:
            result = FindingDetails(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_finding_evidence(self, org_id: str, finding_id: str) -> APIResult[CommonFindings]:
        """
        Retrieves scan evidence details for a finding based on the specified ID.

        This is a subset of the scan output obtained for the associated asset
        that can be attributed to the finding.

        Args:
            org_id (str): The unique identifier for the organization.
            finding_id (str): The unique identifier for the finding.

        Returns:
            tuple: A tuple containing:
                - CommonFindings: Object containing the evidence content and source_type
                - Response: The raw API response object
                - error: Any error that occurred, or None if successful

        Examples:
            Get evidence for a specific finding::

                >>> evidence, _, err = client.zeasm.findings.get_finding_evidence(
                ...     org_id="3f61a446-1a0d-11f0-94e8-8a5f4d45e80c",
                ...     finding_id="8abfc6a2b3058cb75de44c4c65ca4641"
                ... )
                >>> if err:
                ...     print(f"Error: {err}")
                ...     return
                >>> if evidence:
                >>>     print(evidence.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zeasm_base_endpoint}
            /organizations/{org_id}/findings/{finding_id}/evidence
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CommonFindings)
        if error:
            return (None, response, error)

        try:
            result = CommonFindings(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_finding_scan_output(self, org_id: str, finding_id: str) -> APIResult[CommonFindings]:
        """
        Retrieves the complete scan output for a finding based on the specified ID.

        Args:
            org_id (str): The unique identifier for the organization.
            finding_id (str): The unique identifier for the finding.

        Returns:
            tuple: A tuple containing:
                - CommonFindings: Object containing the scan output content and source_type
                - Response: The raw API response object
                - error: Any error that occurred, or None if successful

        Examples:
            Get complete scan output for a specific finding::

                >>> scan_output, _, err = client.zeasm.findings.get_finding_scan_output(
                ...     org_id="3f61a446-1a0d-11f0-94e8-8a5f4d45e80c",
                ...     finding_id="8abfc6a2b3058cb75de44c4c65ca4641"
                ... )
                >>> if err:
                ...     print(f"Error: {err}")
                ...     return
                >>> if finding:
                >>>     print(finding.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zeasm_base_endpoint}
            /organizations/{org_id}/findings/{finding_id}/scan-output
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CommonFindings)
        if error:
            return (None, response, error)

        try:
            result = CommonFindings(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
