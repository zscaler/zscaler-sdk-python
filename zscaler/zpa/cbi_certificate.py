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
from zscaler.zpa.models.cbi_certificate import CBICertificate
from zscaler.utils import format_url


class CBICertificateAPI(APIClient):
    """
    A Client object for the Cloud Browser Isolation Banners resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._cbi_base_endpoint = f"/zpa/cbiconfig/cbi/api/customers/{customer_id}"

    def list_cbi_certificates(self) -> tuple:
        """
        Returns a list of all cloud browser isolation certificates.

        Returns:
            :obj:`Tuple`: A tuple containing a list of `CBICertificate` instances, response object, and error if any.

        Examples:
            >>> cert_list, _, err = client.zpa.cbi_certificate.list_cbi_certificates(
            ... if err:
            ...     print(f"Error listing certificates: {err}")
            ...     return
            ... print(f"Total certificates found: {len(certs_list)}")
            ... for certificate in certs_list:
            ...     print(certificate.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /certificates
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CBICertificate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_cbi_certificate(self, certificate_id: str) -> tuple:
        """
        Returns information on the specified cloud browser isolation certificate.

        Args:
            certificate_id (str): The unique identifier for the cloud browser isolation certificate.

        Returns:
            :obj:`Tuple`: A tuple containing the `CBICertificate` instance, response object, and error if any.

        Examples:
            >>> fetched_cert, _, err = client.zpa.pra_portal.get_portal(
                'a3a6b841-965c-4c75-8dd9-cefd83d740d4')
            ... if err:
            ...     print(f"Error fetching certificate by ID: {err}")
            ...     return
            ... print(f"Fetched certificate by ID: {fetched_certificate.as_dict()}")
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /certificates/{certificate_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CBICertificate)
        if error:
            return (None, response, error)

        try:
            result = CBICertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_cbi_certificate(self, **kwargs) -> tuple:
        """
        Adds a new cloud browser isolation certificate.

        Args:
            name (str): The name of the new cloud browser isolation certificate.
            pem (str): The content of the certificate in PEM format.

        Returns:
            :obj:`Tuple`: A tuple containing the `CBICertificate` instance, response object, and error if any.

        Examples:
            Creating a Cloud browser isolation with the minimum required parameters:

            >>> added_certificate, _, err = client.zpa.cbi_certificate.add_cbi_certificate(
            ...   name='new_certificate',
            ...   pem=("-----BEGIN CERTIFICATE-----\\n"
            ...              "nMIIF2DCCA8CgAwIBAgIBATANBgkqhkiG==\\n"
            ...              "-----END CERTIFICATE-----"),
            )
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /certificate
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CBICertificate)
        if error:
            return (None, response, error)

        try:
            result = CBICertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_cbi_certificate(self, certificate_id: str, **kwargs) -> tuple:
        """
        Updates an existing cloud browser isolation certificate.

        Args:
            certificate_id (str): The unique identifier for the cloud browser isolation certificate.

        Returns:
            tuple: A tuple containing the `CBICertificate` instance, response object, and error if any.

        Examples:
            Updating the name of a Cloud browser isolation:

        Examples:
            Creating a Cloud browser isolation with the minimum required parameters:

            >>> updated_certificate, _, err = client.zpa.cbi_certificate.update_cbi_certificate(
            ...     certificate_id='a3a6b841-965c-4c75-8dd9-cefd83d740d4'
            ...     name='new_certificate',
            ...     pem=("-----BEGIN CERTIFICATE-----\\n"
            ...              "nMIIF2DCCA8CgAwIBAgIBATANBgkqhkiG==\\n"
            ...              "-----END CERTIFICATE-----"),
            )
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /certificates/{certificate_id}
        """
        )

        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CBICertificate)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (CBICertificate({"id": certificate_id}), None, None)

        try:
            result = CBICertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_cbi_certificate(self, certificate_id: str) -> tuple:
        """
        Deletes the specified cloud browser isolation certificate.

        Args:
            certificate_id (str): The unique identifier for the cloud browser isolation certificate.

        Returns:
            tuple: A tuple containing the response object and error if any.

        Examples:
            >>> _, _, err = client.zpa.cbi_certificate.delete_cbi_certificate(
            ...     certificate_id='a3a6b841-965c-4c75-8dd9-cefd83d740d4'
            ... )
            ... if err:
            ...     print(f"Error deleting cbi certificate: {err}")
            ...     return
            ... print(f"CBI Certificate with ID {updated_certificate.id} deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._cbi_base_endpoint}
            /certificates/{certificate_id}
        """
        )

        request, error = self._request_executor.create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
