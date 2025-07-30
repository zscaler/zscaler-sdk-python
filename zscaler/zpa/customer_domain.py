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
from zscaler.zpa.models.customer_domain import CustomerDomainController
from zscaler.utils import format_url


class CustomerDomainControllerAPI(APIClient):
    """
    A client object for the Customer Domain Controller resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}/v2"

    def list_domains(self, type: str, query_params=None) -> tuple:
        """
        Get all customer domains.

        Args:
            query_params {dict}: Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: ID of the microtenant, if applicable.

        Returns:
            :obj:`Tuple`: A tuple containing (list of CustomerDomainController instances, Response, error)

        Example:
            Fetch all customer domains

            >>> domain_list, _, err = client.zpa.customer_domain.list_domains()
            ... if err:
            ...     print(f"Error listing domains: {err}")
            ...     return
            ... print(f"Total domains found: {len(domain_list)}")
            ... for domain in domain_list:
            ...     print(domain.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /associationtype/{type}/domains
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CustomerDomainController)
        if error:
            return (None, response, error)

        try:
            result = CustomerDomainController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_update_domain(self, type: str, domain_list: list, microtenant_id: str = None) -> tuple:
        """
        Add or update domains for a customer.
        Association type field in request body is ignored
        and is overwritten with association type provided as part of the url

        Args:
            type (str): Association type name. Supported Values: `SHARED` and `SEARCH_SUFFIX`
            domain_list (list): List of domain objects to add/update. Each domain object should contain:
                - domain (str): The domain name
                - capture (bool): Whether to capture traffic for this domain
                - name (dict, optional): Domain name object (usually empty {})
                Pass an empty list [] to remove all domains.

        Returns:
            :obj:`Tuple`: A tuple containing (CustomerDomainController instance, Response, error)
                - CustomerDomainController: The created/updated customer domain object or success status
                - Response: HTTP response object (None for 204 No Content)
                - error: Error object if an error occurred, None otherwise

        Example:
            # Add multiple domains in a single request
            >>> added_domain, _, err = client.zpa.customer_domain.add_update_domain(
            ...     type="SEARCH_SUFFIX",
            ...     domain_list=[
            ...         {
            ...             "domain": "example1.com",
            ...             "capture": True
            ...         },
            ...         {
            ...             "domain": "example2.com",
            ...             "capture": False
            ...         }
            ...     ]
            ... )
            >>> if err:
            ...     print(f"Error adding/updating domains: {err}")
            ...     return
            ... print(f"Successfully added/updated domains: {result.as_dict()}")

            # Remove all domains
            >>> added_domain, _, err = client.zpa.customer_domain.add_update_domain(
            ...     type="SEARCH_SUFFIX",
            ...     domain_list=[]
            ... )
            >>> if err:
            ...     print(f"Error removing all domains: {err}")
            ...     return
            ... print(f"Successfully removed all domains: {result.as_dict()}")

        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /associationtype/{type}/domains
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(
            http_method,
            api_url,
            body=domain_list,
            params=params,
        )
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CustomerDomainController)
        if error:
            return (None, response, error)

        if response is None:
            return (CustomerDomainController({"status": "success", "message": "204 No Content"}), None, None)

        try:
            result = CustomerDomainController(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
