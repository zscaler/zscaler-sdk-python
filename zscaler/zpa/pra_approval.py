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
from zscaler.zpa.models.pra_approval import PrivilegedRemoteAccessApproval
from zscaler.utils import format_url
from zscaler.utils import validate_and_convert_times


class PRAApprovalAPI(APIClient):
    """
    A Client object for the Privileged Remote Access Approval resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_approval(self, query_params=None) -> tuple:
        """
        Returns a list of all privileged remote access approvals.

        Args:
            query_params {dict}: Map of query parameters for the request.
                [query_params.pagesize] {int}: Page size for pagination.
                [query_params.search] {str}: Search string for filtering results.
                [query_params.microtenant_id] {str}: ID of the microtenant, if applicable.
                [query_params.max_items] {int}: Maximum number of items to fetch before stopping.
                [query_params.max_pages] {int}: Maximum number of pages to request before stopping.

        Returns:
            tuple: A tuple containing (list of PrivilegedRemoteAccessApproval instances, Response, error)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /approval
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor\
            .create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PrivilegedRemoteAccessApproval(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_approval(self, approval_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified pra approval.

        Args:
            approval_id (str): The unique identifier for the pra approval.
            query_params (dict, optional): Map of query parameters for the request.
                [query_params.microtenantId] {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (PrivilegedRemoteAccessApproval instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""{
            self._zpa_base_endpoint}
            /approval/{approval_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor\
            .create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, PrivilegedRemoteAccessApproval)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessApproval(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_approval(self, **kwargs) -> tuple:
        """
        Adds a privileged remote access approval.

        Args:
            email_ids (list): Email addresses of the users for the approval.
            application_ids (list): List of associated application segment ids.
            start_time (str): Start timestamp in UNIX format.
            end_time (str): End timestamp in UNIX format.
            status (str): Status of the approval. Supported: INVALID, ACTIVE, FUTURE, EXPIRED.
            working_hours (dict): Working hours configuration.

        Returns:
            PrivilegedRemoteAccessApproval: The newly created PRA approval.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /approval
        """
        )

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Convert start_time and end_time to epoch format
        start_time = body.pop("start_time", None)
        end_time = body.pop("end_time", None)
        working_hours = body.get("working_hours", {})

        if start_time and end_time:
            start_epoch, end_epoch = validate_and_convert_times(start_time, end_time, working_hours["time_zone"])
            body.update({"startTime": start_epoch, "endTime": end_epoch})

        # Add applications and working hours to the body
        body.update(
            {
                "applications": [{"id": app_id} for app_id in body.pop("application_ids", [])],
                "workingHours": {
                    "startTimeCron": working_hours.get("start_time_cron"),
                    "endTimeCron": working_hours.get("end_time_cron"),
                    "startTime": working_hours.get("start_time"),
                    "endTime": working_hours.get("end_time"),
                    "days": working_hours.get("days"),
                    "timeZone": working_hours.get("time_zone"),
                },
            }
        )

        # Merge in additional keyword arguments
        body.update(kwargs)

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, PrivilegedRemoteAccessApproval)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessApproval(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_approval(self, approval_id: str, **kwargs) -> tuple:
        """
        Updates a specified approval based on provided keyword arguments.

        Args:
            approval_id (str): The unique identifier for the approval being updated.

        Returns:
            PrivilegedRemoteAccessApproval: The updated approval resource.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /approval/{approval_id}
        """
        )

        # Start with an empty body or an existing resource's current data
        body = {}

        # Update the body with the fields passed in kwargs
        body.update(kwargs)

        # Convert start_time and end_time to epoch format
        start_time = body.pop("start_time", None)
        end_time = body.pop("end_time", None)
        working_hours = body.get("working_hours", {})

        if start_time and end_time:
            start_epoch, end_epoch = validate_and_convert_times(start_time, end_time, working_hours.get("time_zone"))
            body.update({"startTime": start_epoch, "endTime": end_epoch})

        # Add applications and working hours to the body
        body.update(
            {
                "applications": [{"id": app_id} for app_id in body.pop("application_ids", [])],
                "workingHours": {
                    "startTimeCron": working_hours.get("start_time_cron"),
                    "endTimeCron": working_hours.get("end_time_cron"),
                    "startTime": working_hours.get("start_time"),
                    "endTime": working_hours.get("end_time"),
                    "days": working_hours.get("days"),
                    "timeZone": working_hours.get("time_zone"),
                },
            }
        )

        # Merge in additional keyword arguments
        body.update(kwargs)

        # Check if microtenant_id is set in the body, and use it to set query parameter
        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, PrivilegedRemoteAccessApproval)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            return (PrivilegedRemoteAccessApproval({"id": approval_id}), None, None)

        try:
            result = PrivilegedRemoteAccessApproval(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_approval(self, approval_id: str, microtenant_id: str = None) -> tuple:
        """
        Deletes a specified privileged remote access approval.

        Args:
            approval_id (str): The unique identifier for the approval to be deleted.
            microtenant_id (str, optional): The optional ID of the microtenant if applicable.

        Returns:
            int: Status code of the delete operation.
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /approval/{approval_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)

    def expired_approval(self, microtenant_id: str = None) -> tuple:
        """
        Deletes all expired privileged approvals.

        Returns:
            int: Status code of the delete operation.
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /approval/expired
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor\
            .create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
