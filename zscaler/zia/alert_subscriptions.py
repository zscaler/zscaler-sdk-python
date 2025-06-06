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
from zscaler.zia.models.alert_subscriptions import AlertSubscriptions
from zscaler.utils import format_url


class AlertSubscriptionsAPI(APIClient):
    """
    A Client object for the Alert Subscriptions resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_alert_subscriptions(self) -> tuple:
        """
        Retrieves a list of all alert subscriptions.

        This method makes a GET request to the ZIA Admin API and returns detailed alert subscriptions,
        including various bypass rules, DNS optimization configurations, and traffic control settings.

        Returns:
            tuple: A tuple containing:
                - AlertSubscriptions: The current alert subscriptions object.
                - Response: The raw HTTP response returned by the API.
                - error: An error message if the request failed; otherwise, `None`.

        Examples:
            Retrieve and print the current alert subscriptions:

            >>> alert_list, _, error = client.zia.alert_subscriptions.list_alert_subscriptions()
            >>> if error:
            ...     print(f"Error listing alert subscription: {error}")
            ...     return
            ... print(f"Alert Subscription added successfully: {alert_list.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /alertSubscriptions
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            results = [AlertSubscriptions(item) for item in response.get_body()]
            return (results, response, None)
        except Exception as ex:
            return (None, response, ex)

    def get_alert_subscription(self, subscription_id: int) -> tuple:
        """
        Retrieves the alert subscription information based on the specified ID

        Args:
            subscription_id (int): The unique identifier for the Alert Subscription.

        Returns:
            tuple: A tuple containing Alert Subscription instance, Response, error).

        Examples:
            Retrieve and print specific alert subscription:

            >>> fetched_alert, _, error = client.zia.alert_subscriptions.get_alert_subscription(updated_alert.id)
            >>> if error:
            ...     print(f"Error fetching alert subscription by ID: {error}")
            ...     return
            ... print(f"Fetched alert subscription by ID: {fetched_alert.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /alertSubscriptions/{subscription_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertSubscriptions)
        if error:
            return (None, response, error)

        try:
            result = AlertSubscriptions(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_alert_subscription(self, **kwargs) -> tuple:
        """
        Adds a new alert subscription.

        Args:

        Returns:
            tuple:
                - **AlertSubscriptions**: The updated alert subscription object.
                - **Response**: The raw HTTP response returned by the API.
                - **error**: An error message if the update failed; otherwise, `None`.

        Examples:
            Add a new alert subscription:

            >>> added_alert, _, err = client.zia.alert_subscriptions.update_alert_subscription(
            ...     description = 'Zscaler Subscription Alert',
            ...     email = 'alert@acme.com',
            ...     pt0_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     secure_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     manage_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     comply_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     system_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     deleted = False
            ... )
            >>> if err:
            ...     print(f"Error adding alert subscription: {err}")
            ...     return
            ... print(f"Alert Subscription added successfully: {added_alert.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /alertSubscriptions
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(
            method=http_method,
            endpoint=api_url,
            body=body,
        )

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertSubscriptions)
        if error:
            return (None, response, error)

        try:
            result = AlertSubscriptions(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_alert_subscription(self, subscription_id: int, **kwargs) -> tuple:
        """
        Updates an existing alert subscription based on the specified ID

        Args:
            settings (:obj:`AlertSubscriptions`):
                An instance of `AlertSubscriptions` containing the updated configuration.

            Supported attributes:
                - description (str): Additional comments or information about the alert subscription
                - email (str): The email address of the alert recipient
                - pt0_severities (list[str]): Lists the severity levels of the Patient 0 Alert
                    class information that the recipient receives
                    Supported Values: `CRITICAL`, `MAJOR`, `MINOR`, `INFO`, `DEBUG`
                - secure_severities (list[str]): Lists the severity levels of the Secure
                    Alert class information that the recipient receives
                    Supported Values: `CRITICAL`, `MAJOR`, `MINOR`, `INFO`, `DEBUG`
                - manage_severities (list[str]): Supported Values: `CRITICAL`, `MAJOR`, `MINOR`, `INFO`, `DEBUG`
                - comply_severities (list[str]): Supported Values: `CRITICAL`, `MAJOR`, `MINOR`, `INFO`, `DEBUG`
                - system_severities (list[str]): Lists the severity levels of the System Alerts
                    class information that the recipient receives
                    Supported Values: `CRITICAL`, `MAJOR`, `MINOR`, `INFO`, `DEBUG`
                - deleted (bool): Deletes an existing alert subscription

        Returns:
            tuple:
                - **AlertSubscriptions**: The updated alert subscription object.
                - **Response**: The raw HTTP response returned by the API.
                - **error**: An error message if the update failed; otherwise, `None`.

        Examples:
            Add a new alert subscription:

            >>> updated_alert, _, err = client.zia.alert_subscriptions.update_alert_subscription(
            ...     description = 'Zscaler Subscription Alert',
            ...     email = 'alert@acme.com',
            ...     pt0_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     secure_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     manage_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     comply_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     system_severities = ["CRITICAL", "MAJOR", "INFO", "MINOR", "DEBUG"],
            ...     deleted = False
            ... )
            >>> if err:
            ...     print(f"Error updating alert subscription: {err}")
            ...     return
            ... print(f"Alert Subscription updated successfully: {updated_alert.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /alertSubscriptions/{subscription_id}
            """
        )

        body = kwargs
        body["id"] = subscription_id

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, AlertSubscriptions)
        if error:
            return (None, response, error)

        try:
            if response and hasattr(response, "get_body") and response.get_body():
                result = AlertSubscriptions(self.form_response_body(response.get_body()))
            else:
                result = AlertSubscriptions()
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    def delete_alert_subscription(self, subscription_id: int) -> tuple:
        """
        Deletes the specified Alert Subscription

        Args:
            subscription_id (str): The unique identifier of the Alert Subscription.

        Returns:
            tuple: A tuple containing the response object and error (if any).

        Examples:
            Delete a Alert Subscription:

            >>> _, _, error = client.zia.alert_subscriptions.delete_alert_subscription('73459')
            >>> if error:
            ...     print(f"Error deleting Alert Subscription: {error}")
            ...     return
            ... print(f"Alert Subscription with ID {'73459' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /alertSubscriptions/{subscription_id}
        """
        )

        params = {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)
        return (None, response, None)
