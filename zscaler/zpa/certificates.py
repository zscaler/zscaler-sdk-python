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
from zscaler.zpa.models.certificates import Certificate
from zscaler.utils import format_url


class CertificatesAPI(APIClient):
    """
    A Client object for the Certificates resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_certificates(self, query_params: Optional[dict] = None) -> List[Certificate]:
        """
        Fetches a list of all certificates with pagination support.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[Certificate]: A list of Certificate instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     certs = client.zpa.certificates.list_certificates()
            ...     for cert in certs:
            ...         print(cert.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/certificate")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, Certificate)

        return [Certificate(self.form_response_body(item)) for item in response.get_results()]

    def list_issued_certificates(self, query_params: Optional[dict] = None) -> List[Certificate]:
        """
        Fetches a list of all issued certificates with pagination support.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[Certificate]: A list of Certificate instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     certs = client.zpa.certificates.list_issued_certificates()
            ...     for cert in certs:
            ...         print(cert.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_v2}/clientlessCertificate/issued")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        response = self._request_executor.execute(request, Certificate)

        return [Certificate(self.form_response_body(item)) for item in response.get_results()]

    def get_certificate(self, certificate_id: str, query_params: Optional[dict] = None) -> Certificate:
        """
        Fetches a specific certificate by ID.

        Args:
            certificate_id (str): The unique identifier for the certificate.
            query_params (dict, optional): Map of query parameters.

        Returns:
            Certificate: The certificate object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     cert = client.zpa.certificates.get_certificate('999999')
            ...     print(cert.id)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/certificate/{certificate_id}")

        query_params = query_params or {}
        if microtenant_id := query_params.get("microtenant_id"):
            query_params["microtenantId"] = microtenant_id

        request = self._request_executor.create_request(http_method, api_url, params=query_params)
        response = self._request_executor.execute(request, Certificate)

        return Certificate(self.form_response_body(response.get_body()))

    def add_certificate(self, **kwargs) -> Certificate:
        """
        Adds a new certificate.

        Args:
            name (str): Name of the certificate.
            pem (str): The certificate in PEM format.

        Returns:
            Certificate: The newly created certificate object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     cert = client.zpa.certificates.add_certificate(
            ...         name='new_certificate',
            ...         pem="-----BEGIN CERTIFICATE-----\\n...\\n-----END CERTIFICATE-----"
            ...     )
            ...     print(cert.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/certificate")

        body = kwargs
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        response = self._request_executor.execute(request, Certificate)

        return Certificate(self.form_response_body(response.get_body()))

    def update_certificate(self, certificate_id: str, **kwargs) -> Certificate:
        """
        Updates a specific certificate.

        Args:
            certificate_id (str): The ID of the certificate to update.
            **kwargs: Fields to update.

        Returns:
            Certificate: The updated certificate object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     cert = client.zpa.certificates.update_certificate(
            ...         '999999',
            ...         name='updated_certificate'
            ...     )
            ...     print(cert.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/certificate/{certificate_id}")

        body = dict(kwargs)
        microtenant_id = body.get("microtenant_id")
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, body, {}, params)
        response = self._request_executor.execute(request, Certificate)

        if response is None:
            return Certificate({"id": certificate_id})

        return Certificate(self.form_response_body(response.get_body()))

    def delete_certificate(self, certificate_id: str, microtenant_id: str = None) -> None:
        """
        Deletes a certificate by its ID.

        Args:
            certificate_id (str): The ID of the certificate to delete.
            microtenant_id (str, optional): The microtenant ID.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.certificates.delete_certificate('999999')
            ...     print("Certificate deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/certificate/{certificate_id}")

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)
