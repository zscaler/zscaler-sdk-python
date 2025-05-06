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
from zscaler.zpa.models.customer_controller import RemoteAssistance
from zscaler.utils import format_url


class CustomerControllerAPI(APIClient):
    """
    A Client object for the Customer Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"

    def get_auth_domains(self):
        """
        Returns information on authentication domains.

        Returns:
            tuple: A dictionary containing custom ZPA Inspection Control HTTP Methods.

        Example:
            >>> auth_domains, response, error = zpa.authdomains.get_auth_domains()
            >>> if error is None:
            ...     pprint(auth_domains)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /authDomains
            """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, str)

        if error:
            return (None, response, error)

        try:
            result = response.get_body()
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    # def get_remote_assistance(self) -> tuple:
    #     """
    #     Gets information on Remote Assistance configuration for a given customer

    #     Returns:
    #         :obj:`Tuple`: RemoteAssistance: The corresponding Remote Assistance object.

    #     Example:
    #         Retrieve details of Remote Assistance configuration

    #         >>> fetched_remote_assistance, _, err = client.zpa.customer_controller.get_remote_assistance()
    #         ... if err:
    #         ...     print(f"Error fetching remote assistance by ID: {err}")
    #         ...     return
    #         ... print(f"Fetched remote assistance by ID: {fetched_remote_assistance.as_dict()}")
    #     """
    #     http_method = "get".upper()
    #     api_url = format_url(
    #         f"""
    #         {self._zpa_base_endpoint}
    #         /remoteAssistance
    #     """
    #     )

    #     request, error = self._request_executor.create_request(http_method, api_url, {}, {})
    #     if error:
    #         return (None, None, error)

    #     response, error = self._request_executor.execute(request, RemoteAssistance)
    #     if error:
    #         return (None, response, error)

    #     try:
    #         result = RemoteAssistance(self.form_response_body(response.get_body()))
    #     except Exception as error:
    #         return (None, response, error)
    #     return (result, response, None)

    # def add_remote_assistance(self, **kwargs) -> tuple:
    #     """
    #     Add remote assistance configuration for a given customer

    #     Args:
    #         access_type (str): Supported values: `ALL`, `RESTRICTED`, `NONE`
    #         banner (bool): Whether to enable the cloud browser isolation banner.

    #     Returns:
    #         tuple: A tuple containing the `RemoteAssistance` instance, response object, and error if any.

    #     Examples:
    #         >>> configure_ra, _, err = client.zpa.customer_controller.add_remote_assistance(
    #         ...     access_type="ALL",
    #         ... )
    #         ... if err:
    #         ...     print(f"Error configuring remote assistance: {err}")
    #         ...     return
    #         ... print(f"Remote assistance added successfully: {configure_ra.as_dict()}")
    #     """
    #     http_method = "post".upper()
    #     api_url = format_url(
    #         f"""
    #         {self._zpa_base_endpoint}
    #         /remoteAssistance
    #     """
    #     )

    #     body = kwargs

    #     request, error = self._request_executor.create_request(http_method, api_url, body=body)
    #     if error:
    #         return (None, None, error)

    #     response, error = self._request_executor.execute(request, RemoteAssistance)
    #     if error:
    #         return (None, response, error)

    #     try:
    #         result = RemoteAssistance(self.form_response_body(response.get_body()))
    #     except Exception as error:
    #         return (None, response, error)
    #     return (result, response, None)
