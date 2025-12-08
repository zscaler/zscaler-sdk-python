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
from zscaler.zwa.models.change_history import ChangeHistory
from zscaler.zwa.models.generated_tickets import GeneratedTickets
from zscaler.zwa.models.incident_details import IncidentDLPDetails
from zscaler.zwa.models.incident_evidence import IncidentEvidence
from zscaler.zwa.models.incident_search import IncidentSearch
from zscaler.zwa.models.incident_group_search import IncidentGroupSearch
from zscaler.zwa.models.incident_trigger import IncidentTrigger
from zscaler.utils import format_url


class DLPIncidentsAPI(APIClient):

    def __init__(self, request_executor: "RequestExecutor") -> None:
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zwa_base_endpoint = "/zwa/dlp/v1"

    def get_incident_transactions(self, transaction_id: str, query_params: Optional[dict] = None) -> Any:
        """
        Returns information DLP incident details based on the incident ID.

        Args:
            incident_id (str): The ID of the incident.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.fields]`` {list}: The fields associated with the DLP incident.
                    For example, sourceActions, contentInfo, status, resolution, etc.

        Returns:
            :obj:`Tuple`: The incident details information.

        Examples:
            Return information on the application with the ID of SVDP-17410643229970491392:

            >>> try:
            ...     transactions = client.zwa.dlp_incidents.get_incident_transactions('SVDP-17410643229970491392')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... for incident in transactions:
            ...    print(incident.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zwa_base_endpoint}
            /incidents/transactions/{transaction_id}
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        response = self._request_executor.execute(request)
        result = [IncidentDLPDetails(self.form_response_body(response.get_body()))]
        return result

    def get_incident_details(self, incident_id: str, query_params: Optional[dict] = None) -> Any:
        """
        Returns information DLP incident details based on the incident ID.

        Args:
            incident_id (str): The ID of the incident.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.fields]`` {list}: The fields associated with the DLP incident.
                    For example, sourceActions, contentInfo, status, resolution, etc.

        Returns:
            :obj:`Tuple`: The incident details information.

        Examples:
            Return information on the application with the ID of SVDP-17410643229970491392:

            >>> try:
            ...     incident = client.zwa.dlp_incidents.get_incident_details('SVDP-17410643229970491392')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... for inc in incident:
            ...    print(inc.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zwa_base_endpoint}
            /incidents/{incident_id}
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        response = self._request_executor.execute(request)
        result = [IncidentDLPDetails(self.form_response_body(response.get_body()))]
        return result

    def change_history(self, incident_id: str, query_params: Optional[dict] = None) -> Any:
        """
        Returns details of updates made to an incident based on the given ID and timeline.

        Args:
            incident_id (str): The ID of the incident.

        Returns:
            :obj:`Tuple`: The incident details information.

        Examples:
            Return information on the application with the ID of 1-152-DFZG-17410647793298599936:

            >>> try:
            ...     incident = client.zwa.dlp_incidents.change_history('1-152-DFZG-17410647793298599936')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... for inc in incident:
            ...     print(inc.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zwa_base_endpoint}
            /incidents/{incident_id}/change-history
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        response = self._request_executor.execute(request)
        result = [ChangeHistory(self.form_response_body(response.get_body()))]
        return result

    def get_incident_triggers(
        self,
        incident_id: str,
    ) -> IncidentTrigger:
        """
        Returns information DLP incident details based on the incident ID.

        Args:
            incident_id (str): The ID of the incident.

        Returns:
            :obj:`Tuple`: The incident details information.

        Examples:
            Return information on the application with the ID of 1-152-UEES-17410707180862789632:

            >>> try:
            ...     triggers = client.zwa.dlp_incidents.get_incident_triggers('1-152-UEES-17410707180862789632')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... for trigger in triggers:
            ...     print(trigger.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zwa_base_endpoint}
            /incidents/{incident_id}/triggers
        """
        )

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = IncidentTrigger(self.form_response_body(response.get_body()))
        return result

    def get_generated_tickets(
        self,
        incident_id: str,
    ) -> Any:
        """
        Returns details of of the ticket generated for the incident.
        For example, ticket type, ticket ID, ticket status, etc.

        Args:
            incident_id (str): The ID of the incident.

        Returns:
            :obj:`Tuple`: The information of the ticket generated.

        Examples:
            Return information on the application with the ID of 1-152-LJTC-17410768107888539648:

            >>> try:
            ...     tickets = client.zwa.dlp_incidents.get_generated_tickets('1-152-LJTC-17410768107888539648')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print("Incident Ticket Data:")
            ... if not tickets:
            ...     print("No tickets found.")
            ...     return
            ... for ticket in tickets:
            ...     print(ticket.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zwa_base_endpoint}
            /incidents/{incident_id}/tickets
        """
        )

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = [GeneratedTickets(self.form_response_body(response.get_body()))]
        return result

    def get_incident_evidence(
        self,
        incident_id: str,
    ) -> IncidentEvidence:
        """
        Gets the evidence URL of the incident.
        The evidence link can be used to view and download the XML file with the actual
        data that triggered the incident.

        Args:
            incident_id (str): The ID of the incident.

        Returns:
            :obj:`Tuple`: The incident details information.

        Examples:
            >>> try:
            ...     evidence = client.zwa.dlp_incidents.get_incident_evidence(
            ... '1-152-UEES-17410707180862789632')
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
            ... print(evidence.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zwa_base_endpoint}
            /incidents/{incident_id}/evidence
        """
        )

        body = {}
        headers = {}

        request = self._request_executor.create_request(http_method, api_url, body, headers)

        response = self._request_executor.execute(request)
        result = IncidentEvidence(self.form_response_body(response.get_body()))
        return result

    def dlp_incident_search(
        self,
        query_params: Optional[dict] = None,
        fields=None,
        time_range=None,
        **kwargs
    ) -> IncidentSearch:
        """
        Filters DLP incidents based on the given time range and field values.

        The supported field values are:

        - ``Severity``
        - ``Priority``
        - ``Transaction ID``
        - ``Status``
        - ``Source``
        - ``Source DLP Type``
        - ``Labels``
        - ``Incident Group``
        - ``Engine``

        .. note:: Ensure field values match API-supported parameters.

        The supported time range values are:

        - ``Start date and time``
        - ``End date and time``

        Args:
            query_params (dict, optional): Map of query parameters for the request.

                - ``page`` (int, optional): Specifies the page number of the incident in a multi-paginated response.
                        This field is not required if ``page_id`` is used.

                - ``page_size`` (int, optional): Specifies the page size (i.e., number of incidents per page). Max: 100.

                - ``page_id`` (str, optional): Specifies the page ID of the incident in a multi-paginated response.
                        The page ID can be used instead of the page number.

            fields (list, optional): A list of field filters.

                **Example:**

                .. code-block:: python

                    fields = [
                        {"name": "severity", "value": ["high"]},
                        {"name": "status", "value": ["open", "resolved"]}
                    ]

            time_range (dict, optional): Time range for filtering incidents.

                **Example:**

                .. code-block:: python

                    time_range = {
                        "startTime": "2025-03-03T18:04:52.074Z",
                        "endTime": "2025-03-03T18:04:52.074Z"
                    }

        Returns:

        Examples:
            Perform an incident search with a severity filter:

            .. code-block:: python

                search, _, error = client.zwa.incident_search.dlp_incident_search(
                    fields=[{"name": "severity", "value": ["high"]}],
                    time_range={"startTime": "2025-03-03T18:04:52.074Z", "endTime": "2025-03-03T18:04:52.074Z"}
                )

            If an error occurs:

            .. code-block:: python

                else:
                    for incident in search:
                        print(incident.as_dict())
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zwa_base_endpoint}/incidents/search")

        query_params = query_params or {}

        body = {"fields": fields or [], "timeRange": time_range or {}}

        body.update(kwargs)

        # Create the request
        request = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            params=query_params,
            body=body,
        )

        response = self._request_executor.execute(request, IncidentSearch)
        result = IncidentSearch(self.form_response_body(response.get_body()))
        return result

    def incident_group_search(self, incident_id: str, incident_group_ids: list = None) -> IncidentGroupSearch:
        """
        Filters a list of DLP incident groups to which the specified incident ID belongs.

        Args:
            incident_id (str): The ID of the incident.
            incident_group_ids (list, optional): The list of incident group search IDs.

        Returns:
            :obj:`Tuple`: The list of incident group search information.

        Examples:
            Perform a search for an incident group:
            >>> search, _, error = client.zwa.incident_group_search.incident_group_search(
            ... incident_id="123456789",
            ... incident_group_ids=["16786743992009003"]
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zwa_base_endpoint}/incidents/{incident_id}/incident-groups/search")

        # Construct the request body with incident_group_ids
        body = {"incidentGroupIds": incident_group_ids or []}

        # Create the request
        request = self._request_executor.create_request(method=http_method, endpoint=api_url, body=body)

        # Execute the request
        response = self._request_executor.execute(request, IncidentGroupSearch)
        result = IncidentGroupSearch(self.form_response_body(response.get_body()))
        return result

    def assign_labels(self, incident_id: str, labels: list = None) -> IncidentDLPDetails:
        """
        Assigns labels (name-value pairs) to a DLP incident.

        Args:
            incident_id (str): The ID of the incident.
            labels (list, optional): A list of dictionaries containing `key` and `value` pairs.

        Returns:
            :obj:`Tuple`: The updated incident details.

        Examples:
            Assign labels to an incident:

            >>> try:
            ...     incident = client.zwa.incidents.assign_labels(
            ... incident_id="123456789",
            ... labels=[{"key": "Confidential", "value": "Yes"}]
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zwa_base_endpoint}
            /incidents/{incident_id}/labels
        """
        )

        # Construct the request body
        body = {"labels": labels} if labels else {}

        # Create the request
        request = self._request_executor.create_request(method=http_method, endpoint=api_url, body=body)

        # Execute the request
        response = self._request_executor.execute(request, IncidentDLPDetails)
        result = IncidentDLPDetails(self.form_response_body(response.get_body()))
        return result

    def incident_notes(self, incident_id: str, notes: str = None) -> IncidentDLPDetails:
        """
        Adds notes to a DLP incident.

        Args:
            incident_id (str): The ID of the incident.
            notes (str, optional): The note content to be added to the incident.

        Returns:
            :obj:`Tuple`: The updated incident details.

        Examples:
            Add a note to an incident:

            >>> try:
            ...     incident = client.zwa.incidents.incident_notes(
            ... incident_id="123456789",
            ... notes="Investigation in progress."
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zwa_base_endpoint}
            /incidents/{incident_id}/notes
        """
        )

        # Construct the request body
        body = {"notes": notes} if notes else {}

        # Create the request
        request = self._request_executor.create_request(method=http_method, endpoint=api_url, body=body)

        # Execute the request
        response = self._request_executor.execute(request, IncidentDLPDetails)
        result = IncidentDLPDetails(self.form_response_body(response.get_body()))
        return result

    def incident_close(
        self, incident_id: str, resolution_label: dict = None, resolution_code: str = None, notes: str = None
    ) -> IncidentDLPDetails:
        """
        Updates the status of the incident to resolved and closes the incident with a resolution label and a resolution code.

        Args:
            incident_id (str): The ID of the incident.
            resolution_label (dict, optional): Assigns labels (a label name and its associated value) to DLP incidents.
                - `key` (str): The name of the resolution label.
                - `value` (str): The value of the resolution label.

            resolution_code (str, optional): The resolution code.
                Supported values: `"FALSE_POSITIVE"`

            notes (str, optional): Additional notes related to the resolution.

        Returns:
            :obj:`Tuple`: The closed incident information.

        Examples:
            Close an incident with a resolution label:

            >>> try:
            ...     closed_incident = client.zwa.dlp_incidents.incident_close(
            ... incident_id="123456789",
            ... resolution_label={"key": "Review", "value": "Completed"},
            ... resolution_code="FALSE_POSITIVE",
            ... notes="Incident reviewed and closed."
            ... )
        """
        http_method = "post".upper()
        api_url = format_url(f"{self._zwa_base_endpoint}/incidents/{incident_id}/close")

        # Construct the request body with required fields
        body = {
            "resolutionLabel": resolution_label if resolution_label else {},
            "resolutionCode": resolution_code,
            "notes": notes,
        }

        # Remove empty values to prevent sending them as null
        body = {k: v for k, v in body.items() if v}

        # Create the request
        request = self._request_executor.create_request(method=http_method, endpoint=api_url, body=body)

        # Execute the request
        response = self._request_executor.execute(request, IncidentDLPDetails)
        result = IncidentDLPDetails(self.form_response_body(response.get_body()))
        return result
