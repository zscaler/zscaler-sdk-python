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
            tuple: A tuple containing a list of `CBICertificate` instances, response object, and error if any.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /certificates
        """)

        request, error = self._request_executor\
            .create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(CBICertificate(
                    self.form_response_body(item))
                )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_cbi_certificate(self, certificate_id: str) -> tuple:
        """
        Returns information on the specified cloud browser isolation certificate.

        Args:
            certificate_id (str): The unique identifier for the cloud browser isolation certificate.

        Returns:
            tuple: A tuple containing the `CBICertificate` instance, response object, and error if any.
        """
        http_method = "get".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /certificates/{certificate_id}
        """)

        request, error = self._request_executor\
            .create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, CBICertificate)
        if error:
            return (None, response, error)

        try:
            result = CBICertificate(
                self.form_response_body(response.get_body())
            )
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
            tuple: A tuple containing the `CBICertificate` instance, response object, and error if any.

        Examples:
            Creating a Cloud browser isolation with the minimum required parameters:

            >>> zpa.isolation.add_certificate(
            ...   name='new_certificate',
            ...   pem=("-----BEGIN CERTIFICATE-----\\n"
            ...              "nMIIF2DCCA8CgAwIBAgIBATANBgkqhkiG==\\n"
            ...              "-----END CERTIFICATE-----"),
            )

        """
        http_method = "post".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /certificate
        """)

        # Construct the body from kwargs (as a dictionary)
        body = kwargs

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, CBICertificate)
        if error:
            return (None, response, error)

        try:
            result = CBICertificate(
                self.form_response_body(response.get_body())
            )
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

            >>> zpa.isolation.update_certificate(
            ...   name='new_certificate',
            ...   pem=("-----BEGIN CERTIFICATE-----\\n"
            ...              "MIIFNzCCBIHNIHIO==\\n"
            ...              "-----END CERTIFICATE-----"),
            )
        """
        http_method = "put".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /certificates/{certificate_id}
        """)

        # Start with an empty body or an existing resource's current data
        body = {}

        # Update the body with the fields passed in kwargs
        body.update(kwargs)

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request, CBICertificate)
        if error:
            return (None, response, error)

        # Handle case where no content is returned (204 No Content)
        if response is None:
            # Return a meaningful result to indicate success
            return (CBICertificate({"id": certificate_id}), None, None)

        try:
            result = CBICertificate(
                self.form_response_body(response.get_body())
            )
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
        """
        http_method = "delete".upper()
        api_url = format_url(f"""
            {self._cbi_base_endpoint}
            /certificates/{certificate_id}
        """)

        request, error = self._request_executor\
            .create_request(http_method, api_url)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        return (None, response, None)
