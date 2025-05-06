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
from zscaler.utils import format_url


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

        response, error = self._request_executor.execute(request)
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

    # def add_enrollment_cert(self, **kwargs) -> tuple:
    #     """
    #     Creates a new Enrollment Certificate.

    #     Args:
    #         name (str): The name of the Enrollment Certificate
    #         description (str): The description of the segment group.
    #         enabled (bool): Enable the segment group. Defaults to True.

    #     Returns:
    #         :obj:`Tuple`: EnrollmentCertificate: The created Enrollment Certificate object.

    #     Example:
    #         # Basic example: Add a new Enrollment Certificate
    #         >>> added_cert, _, err = client.zpa.enrollment_certificates.add_enrollment_cert(
    #         ...     name="Example Group",
    #         ...     description="This is an example segment group.",
    #         ...     enabled=True
    #         ... )
    #     """
    #     http_method = "post".upper()
    #     api_url = format_url(
    #         f"""
    #         {self._zpa_base_endpoint}
    #         /enrollmentCert
    #     """
    #     )

    #     body = kwargs

    #     request, error = self._request_executor.create_request(http_method, api_url, body=body)
    #     if error:
    #         return (None, None, error)

    #     response, error = self._request_executor.execute(request, EnrollmentCertificate)
    #     if error:
    #         return (None, response, error)

    #     try:
    #         result = EnrollmentCertificate(self.form_response_body(response.get_body()))
    #     except Exception as error:
    #         return (None, response, error)
    #     return (result, response, None)

    # def update_enrollment(self, cert_id: str, **kwargs) -> tuple:
    #     """
    #     Updates the specified enrollment certificate.

    #     Args:
    #         group_id (str): The unique identifier for the enrollment certificate being updated.

    #     Returns:
    #         :obj:`Tuple`: SegmentGroup: The updated enrollment certificate object.

    #     Example:
    #         # Basic example: Update an existing enrollment certificate
    #         >>> group_id = "216196257331370181"
    #         >>> updated_group, _, err = zpa.enrollment_certificates.update_enrollment(
    #         ...     cert_id='2584554',
    #         ...     name="Updated Group Name",
    #         ...     description="Updated description for the enrollment certificate",
    #         ...     enabled=False
    #         ... )
    #     """
    #     http_method = "put".upper()
    #     api_url = format_url(
    #         f"""
    #         {self._zpa_base_endpoint}
    #         /enrollmentCert/{cert_id}
    #     """
    #     )

    #     body = {}

    #     body.update(kwargs)

    #     microtenant_id = body.get("microtenant_id", None)
    #     params = {"microtenantId": microtenant_id} if microtenant_id else {}

    #     request, error = self._request_executor.create_request(http_method, api_url, body, {}, params)
    #     if error:
    #         return (None, None, error)

    #     response, error = self._request_executor.execute(request, EnrollmentCertificate)
    #     if error:
    #         return (None, response, error)

    #     if response is None:
    #         return (EnrollmentCertificate({"id": cert_id}), None, None)

    #     try:
    #         result = EnrollmentCertificate(self.form_response_body(response.get_body()))
    #     except Exception as error:
    #         return (None, response, error)
    #     return (result, response, None)

    # def generate_csr(self, **kwargs) -> tuple:
    #     """
    #     Generates a new csr.

    #     Args:
    #         name (str): The name of the Enrollment CSR
    #         description (str): The description of the Enrollment CSR

    #     Returns:
    #         :obj:`Tuple`: The created Enrollment CSR object.

    #     Example:
    #         # Basic example: Add a new Enrollment CSR
    #         >>> added_cert, _, err = client.zpa.enrollment_certificates.generate_csr(
    #         ...     name="NewEnrollmentCertificate",
    #         ...     description="New enrollment certificate",
    #         ... )
    #     """
    #     http_method = "post".upper()
    #     api_url = format_url(
    #         f"""
    #         {self._zpa_base_endpoint}
    #         /enrollmentCert/csr/generate
    #     """
    #     )

    #     body = kwargs

    #     request, error = self._request_executor.create_request(http_method, api_url, body=body)
    #     if error:
    #         return (None, None, error)

    #     response, error = self._request_executor.execute(request, EnrollmentCertificate)
    #     if error:
    #         return (None, response, error)

    #     try:
    #         result = EnrollmentCertificate (self.form_response_body(response.get_body()))
    #     except Exception as error:
    #         return (None, response, error)
    #     return (result, response, None)

    # def generate_self_signed(self, **kwargs) -> tuple:
    #     """
    #     Generates a new csr.

    #     Args:
    #         name (str): The name of the self signed Enrollment certificate
    #         description (str): The description of the signed Enrollment certificate
    #         valid_from_in_epoch_sec (str): The start date of the enrollment certificate.
    #         valid_to_in_epoch_sec (str): The expiration date of the enrollment certificate.
    #         root_certificate_id (str): The unique identifier of the root certificate.

    #     Returns:
    #         :obj:`Tuple`: The created Self Signed certificate object.

    #     Example:
    #         # Basic example: Add a new Self Signed certificate
    #         >>> added_cert, _, err = client.zpa.enrollment_certificates.generate_self_signed(
    #         ...     name="NewEnrollmentCertificate",
    #         ...     description="New enrollment certificate",
    #         ... )
    #     """
    #     http_method = "post".upper()
    #     api_url = format_url(
    #         f"""
    #         {self._zpa_base_endpoint}
    #         /enrollmentCert/selfsigned/generate
    #     """
    #     )

    #     body = kwargs

    #     request, error = self._request_executor.create_request(http_method, api_url, body=body)
    #     if error:
    #         return (None, None, error)

    #     response, error = self._request_executor.execute(request, EnrollmentCertificate)
    #     if error:
    #         return (None, response, error)

    #     try:
    #         result = EnrollmentCertificate (self.form_response_body(response.get_body()))
    #     except Exception as error:
    #         return (None, response, error)
    #     return (result, response, None)
