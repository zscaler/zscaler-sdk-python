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
                ``[query_params.page_size]`` {str}: Specifies the page size. If not provided, the default page size is 20. The max page size is 500.
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

        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers, params=query_params)
        if error:
            return (None, None, error)

        response, error = self._request_executor\
            .execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(EnrollmentCertificate(
                    self.form_response_body(item))
                )
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

        # Prepare request body, headers, and form (if needed)
        body = {}
        headers = {}

        # Create the request
        request, error = self._request_executor\
            .create_request(http_method, api_url, body, headers)

        if error:
            return (None, None, error)

        # Execute the request
        response, error = self._request_executor\
            .execute(request, EnrollmentCertificate)

        if error:
            return (None, response, error)

        try:
            result = EnrollmentCertificate(
                self.form_response_body(response.get_body())
            )
        except Exception as error:
            return (None, response, error)
        return (result, response, None)
