# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from box import Box, BoxList
from requests import Response

from zscaler.utils import snake_to_camel
from zscaler.zpa.client import ZPAClient


class CertificatesAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_issued_certificates(self, **kwargs) -> BoxList:
        """
        Returns a list of all Browser Access certificates.

        Args:
            **kwargs: Optional keyword args.

        Keyword Args:
            max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            pagesize (int, optional):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: List of all Browser Access certificates.

        Examples:
            >>> for cert in zpa.certificates.list_browser_access():
            ...    print(cert)

        """
        list, _ = self.rest.get_paginated_data(
            path="/clientlessCertificate/issued",
            **kwargs,
            api_version="v2",
        )
        return list

    def list_all_certificates(self, **kwargs) -> BoxList:
        """
        Returns a list of all Browser Access certificates.

        Args:
            **kwargs: Optional keyword args.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int, optional):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: List of all Browser Access certificates.

        Examples:
            >>> for cert in zpa.certificates.list_all_certificates():
            ...    print(cert)

        """
        list, _ = self.rest.get_paginated_data(path="/certificate", **kwargs, api_version="v1")
        return list

    def get_certificate_by_name(self, name):
        certs = self.list_all_certificates()
        for cert in certs:
            if cert.get("name") == name:
                return cert
        return None

    def add_certificate(self, name: str, cert_blob: str, **kwargs) -> Box:
        """
        Add a new Certificate.

        Args:
            name (str): The name of the certificate.
            cert_blob (str): The content of the certificate. Must include the certificate and private key (in PEM format).
            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): The description of the certificate.

        Returns:
            :obj:`Box`: The resource record for the newly created server.

        Examples:
            Create a certificate with minimum required parameters:

            >>> zpa.servers.add_server(
            ...   name='myserver.example',
            ...   cert_blob=("-----BEGIN CERTIFICATE-----\\n"
            ...              "MIIFNzCCBIHNIHIO==\\n"
            ...              "-----END CERTIFICATE-----"),
            )

        """
        payload = {"name": name, "certBlob": cert_blob}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("/certificate", json=payload)
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code > 299:
                return None
        return self.get_certificate(response.get("id"))

    def get_certificate(self, certificate_id: str) -> Box:
        """
        Returns information on a specified Browser Access certificate.

        Args:
            certificate_id (str):
                The unique identifier for the Browser Access certificate.

        Returns:
            :obj:`Box`:
                The Browser Access certificate resource record.

        Examples:
            >>> ba_certificate = zpa.certificates.get_browser_access('99999')

        """
        response = self.rest.get("/clientlessCertificate/%s" % (certificate_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def delete_certificate(self, certificate_id: str) -> Box:
        """
        Returns information on a specified Browser Access certificate.

        Args:
            certificate_id (str):
                The unique identifier for the Browser Access certificate.

        Returns:
            :obj:`Box`:
                The Browser Access certificate resource record.

        Examples:
            >>> ba_certificate = zpa.certificates.get_certificate('99999')

        """
        return self.rest.get(f"certificate/{certificate_id}")

    def get_enrolment(self, certificate_id: str) -> Box:
        """
        Returns information on the specified enrollment certificate.

        Args:
            certificate_id (str): The unique id of the enrollment certificate.

        Returns:
            :obj:`Box`: The enrollment certificate resource record.

        Examples:
            enrolment_cert = zpa.certificates.get_enrolment('99999999')

        """
        response = self.rest.get("/enrollmentCert/%s" % (certificate_id))
        if isinstance(response, Response):
            status_code = response.status_code
            if status_code != 200:
                return None
        return response

    def list_enrolment(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured enrollment certificates.

        Args:
            **kwargs: Optional keyword args.

        Keyword Args:
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int, optional):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: List of all enrollment certificates.

        Examples:
            >>> for cert in zpa.certificates.list_enrolment():
            ...    print(cert)

        """
        list, _ = self.rest.get_paginated_data(path="/enrollmentCert", **kwargs, api_version="v2")
        return list

    def get_enrolment_cert_by_name(self, name):
        certs = self.list_enrolment()
        for cert in certs:
            if cert.get("name") == name:
                return cert
        return None
