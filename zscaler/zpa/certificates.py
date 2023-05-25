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
from restfly.endpoint import APIEndpoint, APISession

from zscaler.utils import Iterator


class CertificatesAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.v2_url = api.v2_url

    def list_browser_access(self, **kwargs) -> BoxList:
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
            >>> for cert in zpa.certificates.list_browser_access():
            ...    print(cert)

        """
        return BoxList(Iterator(self._api, f"{self.v2_url}/clientlessCertificate/issued", **kwargs))

    def get_browser_access(self, certificate_id: str) -> Box:
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
        return self._get(f"clientlessCertificate/{certificate_id}")

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
        return self._get(f"enrollmentCert/{certificate_id}")

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
        return BoxList(Iterator(self._api, f"{self.v2_url}/enrollmentCert", **kwargs))
