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

    def list_users(self, query_params=None, **kwargs) -> tuple:
        """
        Enumerates emergency access in your organization with pagination.
        A subset of emergency access can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page_id]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: The search string used to support search by features and fields for the API.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            :obj:`Tuple`: A tuple containing (list of Emergency Access instances, Response, error)

        Examples:
            >>> access_list, _, err = client.zpa.emergency_access.list_users(
            ... query_params={'search': 'first_name+EQ+Emily', 'page_id': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing emergency access users: {err}")
            ...     return
            ... print(f"Total emergency access users found: {len(access_list)}")
            ... for user in access_list:
            ...     print(user.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /emergencyAccess/users
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, body={}, headers={}, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EmergencyAccessUser)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(EmergencyAccessUser(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_user(self, user_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified emergency access user.

        Args:
            user_id (str): The unique identifier for the emergency access user.

        Returns:
            tuple: A tuple containing the `EmergencyAccessUser` instance, response object, and error if any.

        Examples:
            >>> fetched_user, _, err = client.zpa.emergency_access.get_user('999999')
            ... if err:
            ...     print(f"Error fetching user by ID: {err}")
            ...     return
            ... print(f"Fetched user by ID: {fetched_user.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /emergencyAccess/user/{user_id}
        """
        )

        query_params = query_params or {}

        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EmergencyAccessUser)
        if error:
            return (None, response, error)

        try:
            result = EmergencyAccessUser(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_user(self, activate_now=True, **kwargs) -> tuple:
        """
        Add an emergency access user.

        Args:
            email_id (str): The email address of the emergency access user.
            first_name (str): The first name of the emergency access user.
            last_name (str): The last name of the emergency access user.
            user_id (str): The unique identifier of the emergency access user.
            update_enabled (bool): Indicates if the emergency access user can be updated (true) or not (false).
            activate_now (bool, optional): Indicates if the emergency access user is activated upon creation. Defaults to True.

        Returns:
            :obj:`Tuple`: A tuple containing the `EmergencyAccessUser` instance, response object, and error if any.

        Examples:
            >>> added_user, _, err = client.zpa.emergency_access.add_user(
            ...     email_id=f"user1_{random.randint(1000, 10000)}@acme.com",
            ...     user_id="user1",
            ...     first_name="User1",
            ...     last_name="Smith",
            ...     activated_on="1",
            ...     allowed_activate=True,
            ...     allowed_deactivate=True,
            ... )
            ... if err:
            ...     print(f"Error creating emergency user: {err}")
            ...     return
            ... print(f"emergency user created successfully: {added_user.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /emergencyAccess/user
        """
        )

        body = kwargs

        # Check if microtenant_id is passed and set as a query parameter if present
        microtenant_id = kwargs.get("microtenant_id")
        query_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Append 'activateNow' to the URL query parameters based on the activate_now argument
        query_params = {"activateNow": "true" if activate_now else "false"}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request, EmergencyAccessUser)
        if error:
            return (None, response, error)

        try:
            result = EmergencyAccessUser(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_user(self, user_id: str, activate_now=True, **kwargs) -> tuple:
        """
        Updates the specified emergency access user.

        Args:
            user_id (str): The unique identifier of the emergency access user.

        Keyword Args:
            email_id (str): The email address of the emergency access user.
            first_name (str): The first name of the emergency access user.
            last_name (str): The last name of the emergency access user.

        Returns:
            tuple: A tuple containing the `EmergencyAccessUser` instance, response object, and error if any.

        Examples:
            >>> update_user, _, err = client.zpa.emergency_access.add_uupdate_userser(
            ...     user_id='99999'
            ...     email_id=f"user1_{random.randint(1000, 10000)}@acme.com",
            ...     user_id="user1",
            ...     first_name="User1",
            ...     last_name="Smith",
            ...     activated_on="1",
            ...     allowed_activate=True,
            ...     allowed_deactivate=True,
            ... )
            ... if err:
            ...     print(f"Error updating emergency user: {err}")
            ...     return
            ... print(f"emergency user updated successfully: {added_update_useruser.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /emergencyAccess/user/{user_id}
        """
        )

        body = {}

        body.update(kwargs)

        # Check if microtenant_id is passed and set as a query parameter if present
        microtenant_id = kwargs.get("microtenant_id")
        query_params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Append 'activateNow' to the URL query parameters based on the activate_now argument
        query_params["activateNow"] = "true" if activate_now else "false"

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EmergencyAccessUser)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            return (EmergencyAccessUser({"id": user_id}), None, None)

        try:
            result = EmergencyAccessUser(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def activate_user(self, user_id: str, send_email: bool = False, **kwargs) -> tuple:
        """
        Activates the emergency access user.

        Args:
            user_id (str): The unique identifier of the emergency access user.
            send_email (bool, optional): Whether to send an email upon activation. Defaults to False.

        Returns:
            tuple: A tuple containing the `EmergencyAccessUser` instance, response object, and error if any.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /emergencyAccess/user/{user_id}/activate
        """
        )

        # Query parameters for email notification
        query_params = {"sendEmail": "true"} if send_email else {}

        # Check if microtenant_id is passed and set as a query parameter if present
        microtenant_id = kwargs.get("microtenant_id")
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, {}, query_params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        # Handle case where no content is returned
        if response is None:
            return (None, None, None)

        try:
            # Process the response to return an EmergencyAccessUser instance
            result = EmergencyAccessUser(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def deactivate_user(self, user_id: str, **kwargs) -> tuple:
        """
        Deactivates the emergency access user.

        Args:
            user_id (str): The unique identifier of the emergency access user.

        Returns:
            tuple: A tuple containing the `EmergencyAccessUser` instance, response object, and error if any.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /emergencyAccess/user/{user_id}/deactivate
        """
        )

        # Check if microtenant_id is passed and set as a query parameter if present
        microtenant_id = kwargs.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
