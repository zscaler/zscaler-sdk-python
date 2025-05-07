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

    def list_certificates(self, query_params=None) -> tuple:
        """
        Fetches a list of all certificates with pagination support.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            list: A list of `Certificate` instances.

        Examples:
            Retrieve browser certificates with pagination parameters:

            >>> cert_list, _, err = client.zpa.certificates.list_certificates(
            ... query_params={'search': 'certificate01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing certificates: {err}")
            ...     return
            ... print(f"Total certificates found: {len(cert_list)}")
            ... for cert in cert_list:
            ...     print(cert.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /certificate
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Certificate)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(Certificate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_issued_certificates(self, query_params=None) -> tuple:
        """
        Fetches a list of all issued certificates with pagination support.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.
                ``[query_params.microtenant_id]`` {str}: The unique identifier of the microtenant of ZPA tenant.

        Returns:
            list: A list of `IssuedCertificate` instances.

        Examples:
            Retrieve browser certificates with pagination parameters:

            >>> cert_list, _, err = client.zpa.certificates.list_issued_certificates(
            ... query_params={'search': 'certificate01', 'page': '1', 'page_size': '100'})
            ... if err:
            ...     print(f"Error listing certificates: {err}")
            ...     return
            ... print(f"Total certificates found: {len(cert_list)}")
            ... for cert in cert_list:
            ...     print(cert.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint_v2}
            /clientlessCertificate/issued
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Certificate)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(Certificate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_certificate(self, certificate_id: str, query_params=None) -> tuple:
        """
        Fetches a specific certificate by ID.

        Args:
            group_id (str): The unique identifier for the connector group.
            query_params (dict, optional): Map of query parameters for the request.
                ``[query_params.microtenant_id]`` {str}: The microtenant ID, if applicable.

        Returns:
            tuple: A tuple containing (Certificate instance, Response, error).

        Examples:
            >>> fetched_cert, _, err = client.zpa.certificates.get_certificate('999999')
            ... if err:
            ...     print(f"Error fetching certificate by ID: {err}")
            ...     return
            ... print(fetched_cert.id)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /certificate/{certificate_id}
        """
        )

        query_params = query_params or {}
        microtenant_id = query_params.get("microtenant_id", None)
        if microtenant_id:
            query_params["microtenantId"] = microtenant_id

        request, error = self._request_executor.create_request(http_method, api_url, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Certificate)

        if error:
            return (None, response, error)

        try:
            result = Certificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_certificate(self, **kwargs) -> tuple:
        """
        Adds a new certificate.

        Args:
            certificate_data (dict): Data for the certificate to be added.

        Returns:
            :obj:`Tuple`: The newly created certificate object.

        Examples:
            Creating a Cloud browser isolation with the minimum required parameters:

            >>> added_certificate, _, err = client.zpa.certificates.add_certificate(
            ...   name='new_certificate',
            ...   pem=("-----BEGIN CERTIFICATE-----\\n"
            ...              "nMIIF2DCCA8CgAwIBAgIBATANBgkqhkiG==\\n"
            ...              "-----END CERTIFICATE-----"),
            ... )
            ... if err:
            ...     print(f"Error adding ba certificate: {err}")
            ...     return
            ... print(f"BA Certificate added successfully: {added_certificate.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /certificate
        """
        )

        body = kwargs

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body=body, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Certificate)
        if error:
            return (None, response, error)

        try:
            result = Certificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_certificate(self, certificate_id: str, **kwargs) -> tuple:
        """
        Updates a specific certificate.

        Args:
            certificate_id (str): The ID of the certificate to update.
            certificate_data (dict): The new data for the certificate.

        Returns:
            :obj:`Tuple`: The updated certificate object.

        Examples:
            Creating a Cloud browser isolation with the minimum required parameters:

            >>> updated_certificate, _, err = client.zpa.certificates.update_certificate(
            ...   name='new_certificate',
            ...   pem=("-----BEGIN CERTIFICATE-----\\n"
            ...              "nMIIF2DCCA8CgAwIBAgIBATANBgkqhkiG==\\n"
            ...              "-----END CERTIFICATE-----"),
            ... )
            ... if err:
            ...     print(f"Error adding ba certificate: {err}")
            ...     return
            ... print(f"BA Certificate added successfully: {updated_certificate.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /certificate/{certificate_id}
        """
        )

        body = {}

        body.update(kwargs)

        microtenant_id = body.get("microtenant_id", None)
        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, Certificate)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (Certificate({"id": certificate_id}), None, None)

        try:
            result = Certificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_certificate(self, certificate_id, microtenant_id: str = None) -> tuple:
        """
        Deletes a certificate by its ID.

        Args:
            certificate_id (str): The ID of the certificate to delete.

        Returns:
            Response: The response object for the delete operation.

        Examples:
            >>> _, _, err = client.zpa.certificates.delete_certificate(
            ...     certificate_id='999999'
            ... )
            ... if err:
            ...     print(f"Error deleting ba certificate: {err}")
            ...     return
            ... print(f"BA Certificate with ID {'999999'} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /certificate/{certificate_id}
        """
        )

        params = {"microtenantId": microtenant_id} if microtenant_id else {}

        # Create the request
        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        return (None, response, error)
