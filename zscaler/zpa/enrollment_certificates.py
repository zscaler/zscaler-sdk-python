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

    def list_enrolment(self, query_params=None) -> tuple:
        """
        Enumerates Enrollment Certificates in your organization with pagination.
        A subset of Enrollment Certificates can be returned that match a supported
        filter expression or query.

        Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.page]`` {str}: Specifies the page number.

                ``[query_params.page_size]`` {str}: Specifies the page size.
                    If not provided, the default page size is 20. The max page size is 500.

                ``[query_params.search]`` {str}: Search string for filtering results.

        Returns:
            :obj:`Tuple`: A tuple containing (list of EnrollmentCertificate instances, Response, error)

        Examples:
            Retrieve enrollment certificates with pagination parameters:

            >>> cert_list, _, err = client.zpa.enrollment_certificates.list_enrolment(
            ... query_params={'search': 'Connector', 'page': '1', 'page_size': '100'})
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
            /enrollmentCert
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EnrollmentCertificate)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(EnrollmentCertificate(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def get_enrolment(self, certificate_id: str) -> tuple:
        """
        Returns information on the specified enrollment certificate.

        Args:
            certificate_id (str): The unique ID of the enrollment certificate.

        Returns:
            :obj:`Tuple`: A tuple containing the `EnrollmentCertificate` instance, response object, and error if any.

        Examples:
            >>> fetched_cert, _, err = client.zpa.certificates.get_enrolment('999999')
            ... if err:
            ...     print(f"Error fetching certificate by ID: {err}")
            ...     return
            ... print(fetched_cert.id)
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /enrollmentCert/{certificate_id}
        """
        )

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EnrollmentCertificate)

        if error:
            return (None, response, error)

        try:
            result = EnrollmentCertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def add_enrollment_cert(self, **kwargs) -> tuple:
        """
        Creates a new Enrollment Certificate.

        Args:
            name (str): The name of the new Enrollment certificate
            description (str): The description of the new Enrollment certificate
            client_cert_type (str): The client of the enrollment certificate. Values: `ZAPP_CLIENT`, `ISOLATION_CLIENT`
            valid_from (str): The start date/time of the enrollment certificate in RFC1123 format. Mon, 12 May 2025 16:00:00
            valid_to (str): The end date/time of the enrollment certificate in RFC1123 format. `Mon, 12 May 2026 16:00:00`
            time_zone (str): The time zone in IANA format Time `America/Los_Angeles`
            parent_cert_id (str): The unique identifier of the root certifi

        Returns:
            :obj:`Tuple`: EnrollmentCertificate: The created Enrollment Certificate object.

        Example:
            Add a new enrollment certificate

            >>> added_cert, _, err = client.zpa.enrollment_certificates.add_enrollment_cert(
            ...     name=f"NewCertZAPP_CLIENT_{random.randint(1000, 10000)}",
            ...     description=f"NewCertZAPP_CLIENT_{random.randint(1000, 10000)}",
            ...     parent_cert_id='8965'
            ...     client_cert_type="ZAPP_CLIENT"
            ...     valid_from="Mon, 12 May 2025 16:00:00",
            ...     valid_to="Mon, 12 May 2026 13:30:00",
            ...     time_zone="America/Los_Angeles"
            ... )
            >>> if err:
            ...     print(f"Error creating self signed certificate: {err}")
            ...     return
            ... print(f"Self signed certificate added successfully: {added_cert.as_dict()}")
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /enrollmentCert
        """
        )

        body = kwargs

        if "valid_from" in kwargs and "valid_to" in kwargs and "time_zone" in kwargs:
            try:
                from_epoch, to_epoch = validate_and_convert_times(
                    kwargs["valid_from"],
                    kwargs["valid_to"],
                    kwargs["time_zone"]
                )
                kwargs["valid_from_in_epoch_sec"] = str(from_epoch)
                kwargs["valid_to_in_epoch_sec"] = str(to_epoch)
            except Exception as e:
                return (None, None, e)

        for key in ("valid_from", "valid_to", "time_zone"):
            kwargs.pop(key, None)

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EnrollmentCertificate)
        if error:
            return (None, response, error)

        try:
            result = EnrollmentCertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def update_enrollment(self, cert_id: str, **kwargs) -> tuple:
        """
        Updates the specified enrollment certificate.

        Args:
            cert_id (str): The unique identifier for the enrollment certificate being updated.

        Returns:
            :obj:`Tuple`: SegmentGroup: The updated enrollment certificate object.

        Example:
            Add a new enrollment certificate

            >>> added_cert, _, err = client.zpa.enrollment_certificates.add_enrollment_cert(
            ...     name=f"NewCertZAPP_CLIENT_{random.randint(1000, 10000)}",
            ...     description=f"NewCertZAPP_CLIENT_{random.randint(1000, 10000)}",
            ...     parent_cert_id='8965'
            ...     client_cert_type="ZAPP_CLIENT"
            ...     valid_from="Mon, 12 May 2025 16:00:00",
            ...     valid_to="Mon, 12 May 2026 13:30:00",
            ...     time_zone="America/Los_Angeles"
            ... )
            >>> if err:
            ...     print(f"Error creating self signed certificate: {err}")
            ...     return
            ... print(f"Self signed certificate added successfully: {added_cert.as_dict()}")
        """
        http_method = "put".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /enrollmentCert/{cert_id}
        """
        )

        body = {}

        body.update(kwargs)

        if "valid_from" in kwargs and "valid_to" in kwargs and "time_zone" in kwargs:
            try:
                from_epoch, to_epoch = validate_and_convert_times(
                    kwargs["valid_from"],
                    kwargs["valid_to"],
                    kwargs["time_zone"]
                )
                kwargs["valid_from_in_epoch_sec"] = str(from_epoch)
                kwargs["valid_to_in_epoch_sec"] = str(to_epoch)
            except Exception as e:
                return (None, None, e)

        for key in ("valid_from", "valid_to", "time_zone"):
            kwargs.pop(key, None)

        request, error = self._request_executor.create_request(http_method, api_url, body, {}, {})
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EnrollmentCertificate)
        if error:
            return (None, response, error)

        if response is None:
            return (EnrollmentCertificate({"id": cert_id}), None, None)

        try:
            result = EnrollmentCertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def delete_enrollment_certificate(self, cert_id: str, dry_run: bool = None) -> tuple:
        """
        Deletes the specified enrollment certificate.

        Args:
            cert_id (str): The unique identifier for the enrollment certificate to be deleted.
            dry_run (bool): Supported values `true` or `false`

        Returns:
            int: Status code of the delete operation.

        Example:
            Delete enrollment certificate by ID

            >>> _, _, err = client.zpa.enrollment_certificates.delete_enrollment_certificate('8569')
            ... if err:
            ...     print(f"Error deleting certificate: {err}")
            ...     return
            ... print(f"Certificate with ID '8569' deleted successfully.")
        """
        http_method = "delete".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /enrollmentCert/{cert_id}
        """
        )

        params = {"dryRun": dry_run} if dry_run else {}

        request, error = self._request_executor.create_request(http_method, api_url, params=params)
        if error:
            return (None, error)

        response, error = self._request_executor.execute(request)

        if error:
            return (None, response, error)
        return (None, response, error)

    def generate_csr(self, **kwargs) -> tuple:
        """
        Generates a new csr.

        Args:
            name (str): The name of the Enrollment CSR
            description (str): The description of the Enrollment CSR

        Returns:
            :obj:`Tuple`: The created Enrollment CSR object.

        Example:
            Basic example: Add a new Enrollment CSR

            >>> added_csr, _, err = client.zpa.enrollment_certificates.generate_csr(
            ...     name=f"NewEnrollementCertCSR_{random.randint(1000, 10000)}",
            ...     description=f"NewEnrollementCertCSR_{random.randint(1000, 10000)}",
            ... )
            >>> if err:
            ...     print(f"Error enrollment certificate csr: {err}")
            ...     return
            ... print(f"Enrollment certificate csr added successfully: {added_csr.as_dict()}")
            ... print(added_csr.csr)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /enrollmentCert/csr/generate
        """
        )

        body = kwargs

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EnrollmentCertificate)
        if error:
            return (None, response, error)

        try:
            result = EnrollmentCertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    def generate_self_signed(self, **kwargs) -> tuple:
        """
        Generates a new csr.

        Args:
            name (str): The name of the self signed Enrollment certificate
            description (str): The description of the signed Enrollment certificate
            client_cert_type (str): The client of the enrollment certificate. Values: `ZAPP_CLIENT`, `ISOLATION_CLIENT`
            valid_from (str): The start date/time of the enrollment certificate in RFC1123 format. `Mon, 12 May 2025 16:00:00`
            valid_to (str): The end date/time of the enrollment certificate in RFC1123 format. `Mon, 12 May 2026 16:00:00`
            time_zone (str): The time zone in IANA format Time `America/Los_Angeles`
            root_certificate_id (str): The unique identifier of the root certificate.

        Returns:
            :obj:`Tuple`: The created Self Signed certificate object.

        Example:
            Add a new Self Signed certificate

            >>> added_cert, _, err = client.zpa.enrollment_certificates.generate_self_signed(
            ...     name=f"NewCertZAPP_CLIENT_{random.randint(1000, 10000)}",
            ...     description=f"NewCertZAPP_CLIENT_{random.randint(1000, 10000)}",
            ...     client_cert_type="ZAPP_CLIENT"
            ...     valid_from="Mon, 12 May 2025 16:00:00",
            ...     valid_to="Mon, 12 May 2026 13:30:00",
            ...     time_zone="America/Los_Angeles"
            ... )
            >>> if err:
            ...     print(f"Error creating self signed certificate: {err}")
            ...     return
            ... print(f"Self signed certificate added successfully: {added_cert.as_dict()}")
            ... print(added_cert.zrsaencryptedprivatekey)

            Add a new Self Signed certificate with Root Certificate ID

            >>> added_cert, _, err = client.zpa.enrollment_certificates.generate_self_signed(
            ...     name=f"NewCertZAPP_CLIENT_{random.randint(1000, 10000)}",
            ...     description=f"NewCertZAPP_CLIENT_{random.randint(1000, 10000)}",
            ...     client_cert_type="ZAPP_CLIENT"
            ...     root_certificate_id='2519',
            ...     valid_from="Mon, 12 May 2025 16:00:00",
            ...     valid_to="Mon, 12 May 2026 13:30:00",
            ...     time_zone="America/Los_Angeles"
            ... )
            >>> if err:
            ...     print(f"Error creating self signed certificate: {err}")
            ...     return
            ... print(f"Self signed certificate added successfully: {added_cert.as_dict()}")
            ... print(added_cert.zrsaencryptedprivatekey)
        """
        http_method = "post".upper()
        api_url = format_url(
            f"""
            {self._zpa_base_endpoint}
            /enrollmentCert/selfsigned/generate
        """
        )

        body = kwargs

        if "valid_from" in kwargs and "valid_to" in kwargs and "time_zone" in kwargs:
            try:
                from_epoch, to_epoch = validate_and_convert_times(
                    kwargs["valid_from"],
                    kwargs["valid_to"],
                    kwargs["time_zone"]
                )
                kwargs["valid_from_in_epoch_sec"] = str(from_epoch)
                kwargs["valid_to_in_epoch_sec"] = str(to_epoch)
            except Exception as e:
                return (None, None, e)

        for key in ("valid_from", "valid_to", "time_zone"):
            kwargs.pop(key, None)

        request, error = self._request_executor.create_request(http_method, api_url, body=body)
        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request, EnrollmentCertificate)
        if error:
            return (None, response, error)

        try:
            result = EnrollmentCertificate(self.form_response_body(response.get_body()))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
