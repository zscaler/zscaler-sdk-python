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
from zscaler.zwa.models.change_history import ChangeHistory
from zscaler.zwa.models.generated_tickets import GeneratedTickets
from zscaler.zwa.models.incident_details import IncidentDLPDetails
from zscaler.zwa.models.incident_evidence import IncidentEvidence
from zscaler.zwa.models.incident_search import IncidentSearch
from zscaler.zwa.models.incident_group_search import IncidentGroupSearch
from zscaler.zwa.models.incident_trigger import IncidentTrigger
from zscaler.utils import format_url


class DLPIncidentsAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zwa_base_endpoint = "/zwa/dlp/v1"

    def get_incident_transactions(self, transaction_id: str, query_params=None) -> tuple:
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

            >>> transactions, _, err = client.zwa.dlp_incidents.get_incident_transactions('SVDP-17410643229970491392')
            ... if err:
            ...     print(f"Error listing transactions: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [IncidentDLPDetails(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_incident_details(self, incident_id: str, query_params=None) -> tuple:
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

            >>> incident, _, err = client.zwa.dlp_incidents.get_incident_details('SVDP-17410643229970491392')
            ... if err:
            ...     print(f"Error listing incident: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [IncidentDLPDetails(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def change_history(self, incident_id: str, query_params=None) -> tuple:
        """
        Returns details of updates made to an incident based on the given ID and timeline.

        Args:
            incident_id (str): The ID of the incident.

        Returns:
            :obj:`Tuple`: The incident details information.

        Examples:
            Return information on the application with the ID of 1-152-DFZG-17410647793298599936:

            >>> incident, _, err = client.zwa.dlp_incidents.change_history('1-152-DFZG-17410647793298599936')
            ... if err:
            ...     print(f"Error listing incident history: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [ChangeHistory(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_incident_triggers(
        self,
        incident_id: str,
    ) -> tuple:
        """
        Returns information DLP incident details based on the incident ID.

        Args:
            incident_id (str): The ID of the incident.

        Returns:
            :obj:`Tuple`: The incident details information.

        Examples:
            Return information on the application with the ID of 1-152-UEES-17410707180862789632:

            >>> triggers, _, err = client.zwa.dlp_incidents.get_incident_triggers('1-152-UEES-17410707180862789632')
            ... if err:
            ...      print(f"Error listing application: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = IncidentTrigger(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_generated_tickets(
        self,
        incident_id: str,
    ) -> tuple:
        """
        Returns details of of the ticket generated for the incident.
        For example, ticket type, ticket ID, ticket status, etc.

        Args:
            incident_id (str): The ID of the incident.

        Returns:
            :obj:`Tuple`: The information of the ticket generated.

        Examples:
            Return information on the application with the ID of 1-152-LJTC-17410768107888539648:

            >>> tickets, _, err = client.zwa.dlp_incidents.get_generated_tickets('1-152-LJTC-17410768107888539648')
            ... if err:
            ...     print(f"Error listing tickets: {err}")
            ...     return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [GeneratedTickets(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def get_incident_evidence(
        self,
        incident_id: str,
    ) -> tuple:
        """
        Gets the evidence URL of the incident.
        The evidence link can be used to view and download the XML file with the actual
        data that triggered the incident.

        Args:
            incident_id (str): The ID of the incident.

        Returns:
            :obj:`Tuple`: The incident details information.

        Examples:
            >>> evidence, _, err = client.zwa.dlp_incidents.get_incident_evidence(
            ... '1-152-UEES-17410707180862789632')
            ... if err:
            ...      print(f"Error listing evidence: {err}")
            ...      return
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

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = IncidentEvidence(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def dlp_incident_search(self, query_params=None, fields=None, time_range=None, **kwargs) -> tuple:
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
            tuple: The incident search results.

        Examples:
            Perform an incident search with a severity filter:

            .. code-block:: python

                search, _, error = client.zwa.incident_search.dlp_incident_search(
                    fields=[{"name": "severity", "value": ["high"]}],
                    time_range={"startTime": "2025-03-03T18:04:52.074Z", "endTime": "2025-03-03T18:04:52.074Z"}
                )

            If an error occurs:

            .. code-block:: python

                if error:
                    print(f"Error fetching incidents: {error}")
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
        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            params=query_params,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IncidentSearch)
        if error:
            return (None, response, error)

        try:
            result = IncidentSearch(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def incident_group_search(self, incident_id: str, incident_group_ids: list = None) -> tuple:
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
        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, body=body)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, IncidentGroupSearch)
        if error:
            return (None, response, error)

        try:
            result = IncidentGroupSearch(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def assign_labels(self, incident_id: str, labels: list = None) -> tuple:
        """
        Assigns labels (name-value pairs) to a DLP incident.

        Args:
            incident_id (str): The ID of the incident.
            labels (list, optional): A list of dictionaries containing `key` and `value` pairs.

        Returns:
            :obj:`Tuple`: The updated incident details.

        Examples:
            Assign labels to an incident:

            >>> incident, _, err = client.zwa.incidents.assign_labels(
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
        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, body=body)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, IncidentDLPDetails)
        if error:
            return (None, response, error)

        try:
            result = IncidentDLPDetails(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def incident_notes(self, incident_id: str, notes: str = None) -> tuple:
        """
        Adds notes to a DLP incident.

        Args:
            incident_id (str): The ID of the incident.
            notes (str, optional): The note content to be added to the incident.

        Returns:
            :obj:`Tuple`: The updated incident details.

        Examples:
            Add a note to an incident:

            >>> incident, _, err = client.zwa.incidents.incident_notes(
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
        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, body=body)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, IncidentDLPDetails)
        if error:
            return (None, response, error)

        try:
            result = IncidentDLPDetails(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def incident_close(
        self, incident_id: str, resolution_label: dict = None, resolution_code: str = None, notes: str = None
    ) -> tuple:
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

            >>> closed_incident, _, err = client.zwa.dlp_incidents.incident_close(
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
        request, error = self._request_executor.create_request(method=http_method, endpoint=api_url, body=body)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, IncidentDLPDetails)
        if error:
            return (None, response, error)

        try:
            result = IncidentDLPDetails(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
