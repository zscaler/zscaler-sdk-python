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
from zscaler.zpa.models.enrollment_certificates import EnrollmentCertificate
from zscaler.utils import format_url, validate_and_convert_times


class EnrollmentCertificateAPI(APIClient):
    """
    A Client object for the Enrollment Certificates resource.
    """

    def __init__(self, request_executor, config):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        customer_id = config["client"].get("customerId")
        self._zpa_base_endpoint = f"/zpa/mgmtconfig/v1/admin/customers/{customer_id}"
        self._zpa_base_endpoint_v2 = f"/zpa/mgmtconfig/v2/admin/customers/{customer_id}"

    def list_enrolment(self, query_params: Optional[dict] = None) -> List[EnrollmentCertificate]:
        """
        Enumerates Enrollment Certificates in your organization.

        Args:
            query_params (dict): Map of query parameters for the request.

        Returns:
            List[EnrollmentCertificate]: A list of EnrollmentCertificate instances.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     certs = client.zpa.enrollment_certificates.list_enrolment()
            ...     for cert in certs:
            ...         print(cert.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint_v2}/enrollmentCert")

        query_params = query_params or {}

        request = self._request_executor.create_request(http_method, api_url, {}, {}, params=query_params)
        response = self._request_executor.execute(request, EnrollmentCertificate)

        return [EnrollmentCertificate(self.form_response_body(item)) for item in response.get_results()]

    def get_enrolment(self, certificate_id: str) -> EnrollmentCertificate:
        """
        Returns information on the specified enrollment certificate.

        Args:
            certificate_id (str): The unique ID of the enrollment certificate.

        Returns:
            EnrollmentCertificate: The enrollment certificate object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     cert = client.zpa.enrollment_certificates.get_enrolment('999999')
            ...     print(cert.id)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "GET"
        api_url = format_url(f"{self._zpa_base_endpoint}/enrollmentCert/{certificate_id}")

        request = self._request_executor.create_request(http_method, api_url, {}, {})
        response = self._request_executor.execute(request, EnrollmentCertificate)

        return EnrollmentCertificate(self.form_response_body(response.get_body()))

    def add_enrollment_cert(self, **kwargs) -> EnrollmentCertificate:
        """
        Creates a new Enrollment Certificate.

        Args:
            name (str): The name of the new Enrollment certificate.
            description (str): The description of the certificate.
            client_cert_type (str): The client type ('ZAPP_CLIENT', 'ISOLATION_CLIENT').
            valid_from (str): Start date/time in RFC1123 format.
            valid_to (str): End date/time in RFC1123 format.
            time_zone (str): The time zone in IANA format.
            parent_cert_id (str): The ID of the root certificate.

        Returns:
            EnrollmentCertificate: The created certificate.

        Raises:
            ZscalerAPIException: If the API request fails.
            Exception: If time validation fails.

        Examples:
            >>> try:
            ...     cert = client.zpa.enrollment_certificates.add_enrollment_cert(
            ...         name="NewCert",
            ...         client_cert_type="ZAPP_CLIENT",
            ...         valid_from="Mon, 12 May 2025 16:00:00",
            ...         valid_to="Mon, 12 May 2026 13:30:00",
            ...         time_zone="America/Los_Angeles"
            ...     )
            ...     print(cert.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/enrollmentCert")

        body = kwargs

        if "valid_from" in kwargs and "valid_to" in kwargs and "time_zone" in kwargs:
            from_epoch, to_epoch = validate_and_convert_times(
                kwargs["valid_from"],
                kwargs["valid_to"],
                kwargs["time_zone"]
            )
            kwargs["valid_from_in_epoch_sec"] = str(from_epoch)
            kwargs["valid_to_in_epoch_sec"] = str(to_epoch)

        for key in ("valid_from", "valid_to", "time_zone"):
            kwargs.pop(key, None)

        request = self._request_executor.create_request(http_method, api_url, body=body)
        response = self._request_executor.execute(request, EnrollmentCertificate)

        return EnrollmentCertificate(self.form_response_body(response.get_body()))

    def update_enrollment(self, cert_id: str, **kwargs) -> EnrollmentCertificate:
        """
        Updates the specified enrollment certificate.

        Args:
            cert_id (str): The unique identifier for the certificate.
            **kwargs: Fields to update.

        Returns:
            EnrollmentCertificate: The updated certificate.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     cert = client.zpa.enrollment_certificates.update_enrollment(
            ...         '999999',
            ...         name="UpdatedCert"
            ...     )
            ...     print(cert.as_dict())
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "PUT"
        api_url = format_url(f"{self._zpa_base_endpoint}/enrollmentCert/{cert_id}")

        body = dict(kwargs)

        if "valid_from" in kwargs and "valid_to" in kwargs and "time_zone" in kwargs:
            from_epoch, to_epoch = validate_and_convert_times(
                kwargs["valid_from"],
                kwargs["valid_to"],
                kwargs["time_zone"]
            )
            kwargs["valid_from_in_epoch_sec"] = str(from_epoch)
            kwargs["valid_to_in_epoch_sec"] = str(to_epoch)

        for key in ("valid_from", "valid_to", "time_zone"):
            kwargs.pop(key, None)

        request = self._request_executor.create_request(http_method, api_url, body, {}, {})
        response = self._request_executor.execute(request, EnrollmentCertificate)

        if response is None:
            return EnrollmentCertificate({"id": cert_id})

        return EnrollmentCertificate(self.form_response_body(response.get_body()))

    def delete_enrollment_certificate(self, cert_id: str, dry_run: bool = None) -> None:
        """
        Deletes the specified enrollment certificate.

        Args:
            cert_id (str): The unique identifier for the certificate.
            dry_run (bool, optional): If true, simulates the deletion.

        Returns:
            None

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     client.zpa.enrollment_certificates.delete_enrollment_certificate('8569')
            ...     print("Certificate deleted successfully")
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "DELETE"
        api_url = format_url(f"{self._zpa_base_endpoint}/enrollmentCert/{cert_id}")

        params = {"dryRun": dry_run} if dry_run else {}

        request = self._request_executor.create_request(http_method, api_url, params=params)
        self._request_executor.execute(request)

    def generate_csr(self, **kwargs) -> EnrollmentCertificate:
        """
        Generates a new CSR.

        Args:
            name (str): The name of the Enrollment CSR.
            description (str): The description of the CSR.

        Returns:
            EnrollmentCertificate: The created CSR object.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     csr = client.zpa.enrollment_certificates.generate_csr(
            ...         name="NewCSR",
            ...         description="CSR description"
            ...     )
            ...     print(csr.csr)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/enrollmentCert/csr/generate")

        body = kwargs

        request = self._request_executor.create_request(http_method, api_url, body=body)
        response = self._request_executor.execute(request, EnrollmentCertificate)

        return EnrollmentCertificate(self.form_response_body(response.get_body()))

    def generate_self_signed(self, **kwargs) -> EnrollmentCertificate:
        """
        Generates a new self-signed certificate.

        Args:
            name (str): The name of the certificate.
            description (str): The description.
            client_cert_type (str): The client type.
            valid_from (str): Start date/time in RFC1123 format.
            valid_to (str): End date/time in RFC1123 format.
            time_zone (str): The time zone in IANA format.
            root_certificate_id (str, optional): The root certificate ID.

        Returns:
            EnrollmentCertificate: The created self-signed certificate.

        Raises:
            ZscalerAPIException: If the API request fails.

        Examples:
            >>> try:
            ...     cert = client.zpa.enrollment_certificates.generate_self_signed(
            ...         name="SelfSignedCert",
            ...         client_cert_type="ZAPP_CLIENT",
            ...         valid_from="Mon, 12 May 2025 16:00:00",
            ...         valid_to="Mon, 12 May 2026 13:30:00",
            ...         time_zone="America/Los_Angeles"
            ...     )
            ...     print(cert.zrsaencryptedprivatekey)
            ... except ZscalerAPIException as e:
            ...     print(f"Error: {e}")
        """
        http_method = "POST"
        api_url = format_url(f"{self._zpa_base_endpoint}/enrollmentCert/selfsigned/generate")

        body = kwargs

        if "valid_from" in kwargs and "valid_to" in kwargs and "time_zone" in kwargs:
            from_epoch, to_epoch = validate_and_convert_times(
                kwargs["valid_from"],
                kwargs["valid_to"],
                kwargs["time_zone"]
            )
            kwargs["valid_from_in_epoch_sec"] = str(from_epoch)
            kwargs["valid_to_in_epoch_sec"] = str(to_epoch)

        for key in ("valid_from", "valid_to", "time_zone"):
            kwargs.pop(key, None)

        request = self._request_executor.create_request(http_method, api_url, body=body)
        response = self._request_executor.execute(request, EnrollmentCertificate)

        return EnrollmentCertificate(self.form_response_body(response.get_body()))
