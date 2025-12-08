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
from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zpa.models.emergency_access import EmergencyAccessUser
from zscaler.utils import format_url


class EmergencyAccessAPI(APIClient):
    """
    A Client object for the Emergency Access Users resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def list_users(self, query_params: Optional[dict] = None) -> List[EmergencyAccessUser]:
        """
        Enumerates emergency access users in your organization.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[EmergencyAccessUser]: A list of EmergencyAccessUser instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     users = client.zpa.emergency_access.list_users()
            ...     for user in users:
            ...         print(user.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/emergencyAccess/users")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params=query_params)
        response = self._request_executor.execute(request, EmergencyAccessUser)

        return [EmergencyAccessUser(self.form_response_body(item)) for item in response.get_results()]

    def get_user(self, user_id: str, query_params: Optional[dict] = None) -> EmergencyAccessUser:
        """
        Returns information on the specified emergency access user.

        Args:
            user_id (str): The unique identifier for the emergency access user.
            query_params (dict, optional): Map of query parameters.

        Returns:
            EmergencyAccessUser: The emergency access user object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     user = client.zpa.emergency_access.get_user('999999')
            ...     print(user.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/emergencyAccess/user/{user_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, EmergencyAccessUser)

        return EmergencyAccessUser(self.form_response_body(response.get_body()))

    def add_user(self, activate_now=True, **kwargs) -> EmergencyAccessUser:
        """
        Add an emergency access user.

        Args:
            activate_now (bool): Activate the user upon creation.
            email_id (str): The email address.
            first_name (str): The first name.
            last_name (str): The last name.
            user_id (str): The user identifier.

        Returns:
            EmergencyAccessUser: The newly created user.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     user = client.zpa.emergency_access.add_user(
            ...         email_id="user1@acme.com",
            ...         first_name="User1",
            ...         last_name="Smith"
            ...     )
            ...     print(user.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/emergencyAccess/user")

        body = kwargs

        microtenant_id = kwargs.get("microtenant_id")
        query_params = {"microtenantId": microtenant_id} if microtenant_id else {}
        query_params["activateNow"] = "true" if activate_now else "false"

        request = self._request_executor.create_request(http_method, api_url, body=body, params=query_params)
        response = self._request_executor.execute(request, EmergencyAccessUser)

        return EmergencyAccessUser(self.form_response_body(response.get_body()))

    def update_user(self, user_id: str, activate_now=True, **kwargs) -> EmergencyAccessUser:
        """
        Updates the specified emergency access user.

        Args:
            user_id (str): The unique identifier of the user.
            activate_now (bool): Whether to activate now.
            **kwargs: Fields to update.

        Returns:
            EmergencyAccessUser: The updated user.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     user = client.zpa.emergency_access.update_user(
            ...         '999999',
            ...         first_name="UpdatedName"
            ...     )
            ...     print(user.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/emergencyAccess/user/{user_id}")

        body = dict(kwargs)

        microtenant_id = kwargs.get("microtenant_id")
        query_params = {"microtenantId": microtenant_id} if microtenant_id else {}
        query_params["activateNow"] = "true" if activate_now else "false"

        request = self._request_executor.create_request(http_method, api_url, body=body, params=query_params)
        response = self._request_executor.execute(request, EmergencyAccessUser)

        if response is None:
            return EmergencyAccessUser({"id": user_id})

        return EmergencyAccessUser(self.form_response_body(response.get_body()))

    def activate_user(self, user_id: str, send_email: bool = False, **kwargs) -> Optional[EmergencyAccessUser]:
        """
        Activates the emergency access user.

        Args:
            user_id (str): The unique identifier of the user.
            send_email (bool): Whether to send an email.

        Returns:
            Optional[EmergencyAccessUser]: The activated user or None.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     user = client.zpa.emergency_access.activate_user('999999')
            ...     print("User activated")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/emergencyAccess/user/{user_id}/activate")

        query_params = {"sendEmail": "true"} if send_email else {}
        if microtenant_id := kwargs.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, {}, query_params)
        response = self._request_executor.execute(request)

        if response is None:
            return None

        return EmergencyAccessUser(self.form_response_body(response.get_body()))

    def deactivate_user(self, user_id: str, **kwargs) -> None:
        """
        Deactivates the emergency access user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.emergency_access.deactivate_user('999999')
            ...     print("User deactivated")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/emergencyAccess/user/{user_id}/deactivate")

        microtenant_id = kwargs.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
