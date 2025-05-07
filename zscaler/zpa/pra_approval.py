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

                ``[query_params.page]`` {str}: Specifies the page number.
                ``[query_params.page_size]`` {int}: Page size for pagination.
                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.sort_by]`` {str}: The sort string used to support sorting on the given field for the API.

                ``[query_params.sort_dir]`` {str}: Specifies the sort direction (i.e., ascending or descending order).
                    Available values : ASC, DESC

                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            tuple: A tuple containing (list of PrivilegedRemoteAccessApproval instances, Response, error)

        Examples:
        >>> approvals_list, _, err = zpa.pra_approval.list_approval()
        ... if err:
        ...     print(f"Error listing approvals: {err}")
        ...     return
        ... for approval in approvals_list:
        ...     print(approval.as_dict())
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

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessApproval)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(PrivilegedRemoteAccessApproval(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_approval(self, approval_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified pra approval.

        Args:
            approval_id (str): The unique identifier for the pra approval.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (PrivilegedRemoteAccessApproval instance, Response, error)

        Examples:
        >>> approval, _, err = client.zpa.pra_approval.get_approval(
        ... approval_id=99999
        ... )
        ... if err:
        ...     print(f"Error fetching approval by ID: {err}")
        ...     return
        ... print(f"Fetched approval by ID: {approval.as_dict()}")
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

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessApproval)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessApproval(self.form_response_body(response.get_body()))
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
            PrivilegedRemoteAccessApproval: The newly created PRA approval

        Examples:
        >>> added_approval, _, error = client.zpa.pra_approval.add_approval(
        ... email_ids=['jdoe@acme.com'],
        ... application_ids=['72058304855096641'],
        ... start_time="Tue, 19 Mar 2025 00:00:00 PST",
        ... end_time="Sat, 19 Apr 2025 00:00:00 PST",
        ... status='ACTIVE',
        ... working_hours= {
        ...     "start_time_cron": "0 0 16 ? * SUN,MON,TUE,WED,THU,FRI,SAT",
        ...     "end_time_cron": "0 0 0 ? * MON,TUE,WED,THU,FRI,SAT,SUN",
        ...     "start_time": "09:00",
        ...     "end_time": "17:00",
        ...     "days": ["FRI", "MON", "SAT", "SUN", "THU", "TUE", "WED"],
        ...     "time_zone": "America/Vancouver"
        ...     },
        ... )
        ... if error:
        ...     print(f"Error adding pra approval: {error}")
        ...     return
        ... print(f"Pra approval added successfully: {added_approval.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /approval
        """
        )

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
        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessApproval)
        if error:
            return (None, response, error)

        try:
            result = PrivilegedRemoteAccessApproval(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_approval(self, approval_id: str, **kwargs) -> tuple:
        """
        Updates a specified approval based on provided keyword arguments.

        Args:
            approval_id (str): The unique identifier for the approval being updated.

        Returns:
            PrivilegedRemoteAccessApproval: The updated approval resource

        Examples:
        >>> updated_approval, _, error = client.zpa.pra_approval.add_approval(
        ... approval_id='99999',
        ... email_ids=['jdoe@acme.com'],
        ... application_ids=['72058304855096641'],
        ... start_time="Tue, 19 Mar 2025 00:00:00 PST",
        ... end_time="Sat, 19 Apr 2025 00:00:00 PST",
        ... status='ACTIVE',
        ... working_hours= {
        ...     "start_time_cron": "0 0 16 ? * SUN,MON,TUE,WED,THU,FRI,SAT",
        ...     "end_time_cron": "0 0 0 ? * MON,TUE,WED,THU,FRI,SAT,SUN",
        ...     "start_time": "09:00",
        ...     "end_time": "17:00",
        ...     "days": ["FRI", "MON", "SAT", "SUN", "THU", "TUE", "WED"],
        ...     "time_zone": "America/Vancouver"
        ...     },
        ... )
        ... if error:
        ...     print(f"Error updating PRA approval: {error}")
        ...     return
        ... print(f"PRA approval updated successfully: {updated_approval.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /approval/{approval_id}
        """
        )

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
        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, PrivilegedRemoteAccessApproval)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            return (PrivilegedRemoteAccessApproval({"id": approval_id}), None, None)

        try:
            result = PrivilegedRemoteAccessApproval(self.form_response_body(response.get_body()))
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

        Examples:
        >>> _, _, err = client.zpa.pra_approval.delete_approval(
        ... approval_id=99999
        ... )
        ... if err:
        ...     print(f"Error deleting approval: {err}")
        ...     return
        ... print(f"PRA Approval with ID {99999} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /approval/{approval_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
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

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
