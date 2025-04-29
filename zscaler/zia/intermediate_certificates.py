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
from zscaler.zia.models.intermediate_certificates import IntermediateCACertificate
from zscaler.zia.models.intermediate_certificates import CertSigningRequest
from zscaler.utils import format_url


class IntermediateCertsAPI(APIClient):
    """
    A Client object for the SSL Inspection resource.
    """

    _zia_base_endpoint = "/zia/api/v1"

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor

    def list_ca_certificates(self, query_params=None) -> tuple:
        """
        List of intermediate CA certificates added for SSL inspection.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(IntermediateCACertificate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ca_certificate(self, cert_id: int) -> tuple:
        """
        Fetches a specific intermediate CA certificate with the specified ID.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IntermediateCACertificate)
        if error:
            return (None, response, error)

        try:
            result = IntermediateCACertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ca_certificates_lite(self, query_params=None) -> tuple:
        """
        List of intermediate CA certificates added for SSL inspection.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/lite
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(IntermediateCACertificate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_ca_certificate_lite(self, cert_id: int) -> tuple:
        """
        Fetches a specific intermediate CA certificate with the specified ID.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/lite/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IntermediateCACertificate)
        if error:
            return (None, response, error)

        try:
            result = IntermediateCACertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def list_ready_to_use(self, query_params=None) -> tuple:
        """
        List of intermediate CA certificates that are ready to use for SSL inspection.
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/readyToUse
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(IntermediateCACertificate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_show_cert(self, cert_id: int) -> tuple:
        """
        Shows information about the signed intermediate CA certificate with the specified ID.
        This operation is not applicable for the Zscaler root certificate

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/showCert/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CertSigningRequest)
        if error:
            return (None, response, error)

        try:
            result = CertSigningRequest(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_show_csr(self, cert_id: int) -> tuple:
        """
        Shows information about the Certificate Signing Request (CSR) for the specified ID.
        This operation is not applicable for the Zscaler root certificate

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/showCsr/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CertSigningRequest)
        if error:
            return (None, response, error)

        try:
            result = CertSigningRequest(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_ca_certificate(self, **kwargs) -> tuple:
        """
        Creates a custom intermediate CA certificate that can be used for SSL inspection.

        Args:
            **kwargs:
                - name (str): Name of the intermediate CA certificate.
                - description (str): Description for the intermediate CA certificate.

                - type (str): Type of the intermediate CA certificate.
                    Supported values: ZSCALER, CUSTOM_SW, CUSTOM_HSM.

                - region (str): Location of the HSM resources. Required for custom Interm.
                    CA certificates with cloud HSM protection.

                Supported values: GLOBAL, ASIA, EUROPE, US.
                - status (str): Whether the certificate is enabled or disabled for SSL inspection.
                Supported values: ENABLED, DISABLED.
                - default_certificate (bool): If true, this is the default intermediate certificate.
                - current_state (str): Current stage of the certificate in the configuration workflow.
                Supported values: GENERAL_DONE, KEYGEN_DONE, PUBKEY_DONE, ATTESTATION_DONE, ATTESTATION_VERIFY_DONE,
                CSRGEN_DONE, INTCERT_UPLOAD_DONE, CERTCHAIN_UPLOAD_DONE, CERT_READY.

        Returns:
            tuple: A tuple containing the newly added Rule Label (Box), response, and error.
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate
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

        response, error = self._request_executor.execute(request, IntermediateCACertificate)
        if error:
            return (None, response, error)

        try:
            result = IntermediateCACertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_ca_certificate(self, cert_id: int, **kwargs) -> tuple:
        """
        Updates intermediate CA certificate information for the specified ID.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing the updated intermediate CA certificate, response, and error.
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/{cert_id}
        """
        )
        body = {}

        body.update(kwargs)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, IntermediateCACertificate)
        if error:
            return (None, response, error)

        try:
            result = IntermediateCACertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_ca_certificate(self, cert_id: int) -> tuple:
        """
        Deletes the intermediate CA certificate with the specified ID.
        The default intermediate certificate cannot be deleted.

        Args:
            cert_id (str): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing the response object and error (if any).
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/{cert_id}
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

    def download_csr(self, cert_id: int) -> tuple:
        """
        Downloads a Certificate Signing Request (CSR) for the specified ID.
        To perform this operation, a CSR must have already been generated.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            //intermediateCaCertificate/downloadCsr/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def download_public_key(self, cert_id: int) -> tuple:
        """
        Downloads the public key in the HSM key pair for the intermediate CA certificate with the specified ID

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/downloadPublicKey/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def finalize_cert(self, cert_id: int) -> tuple:
        """
        Finalizes the intermediate CA certificate with the specified ID.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/finalizeCert/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def generate_csr(self, cert_id: int) -> tuple:
        """
        Generates a Certificate Signing Request (CSR) for the custom intermediate CA certificate with the specified ID.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/generateCsr/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, CertSigningRequest)
        if error:
            return (None, response, error)

        try:
            result = CertSigningRequest(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def generate_key_pair(self, cert_id: int) -> tuple:
        """
        Generates a HSM key pair for the custom intermediate CA certificate with the specified ID.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/keyPair/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def upload_cert(self, cert_id: int) -> tuple:
        """
        Uploads a custom intermediate CA certificate signed by your Certificate Authority (CA) for SSL inspection.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/uploadCert/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def upload_cert_chain(self, cert_id: int) -> tuple:
        """
        Uploads the intermediate certificate chain (PEM file).

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/uploadCertChain/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def verify_key_attestation(self, cert_id: int) -> tuple:
        """
        Verifies the attestation for the HSM keys generated for the specified ID.

        Args:
            cert_id (int): The unique identifier for the intermediate CA certificate.

        Returns:
            tuple: A tuple containing (intermediate CA certificate instance, Response, error).
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zia_base_endpoint}
            /intermediateCaCertificate/verifyKeyAttestation/{cert_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = self.form_response_body(response.get_body())
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
