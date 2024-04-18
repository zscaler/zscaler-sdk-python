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


import pytest

from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestBaCertificate:
    """
    Integration Tests for the certificates.
    """

    @pytest.mark.asyncio
    async def test_ba_certificate(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        certificate_id = None

        # List all certificates
        try:
            certs = client.certificates.list_issued_certificates()
            assert isinstance(certs, list), "Expected a list of certificates"
            if certs:  # If there are any certificates, proceed with further operations
                first_certificate = certs[0]
                certificate_id = first_certificate.get("id")
        except Exception as exc:
            errors.append(f"Listing certificates failed: {str(exc)}")

        if certificate_id:
            # Fetch the selected certificate by its ID
            try:
                fetched_certificate = client.certificates.get_certificate(
                    certificate_id
                )
                assert (
                    fetched_certificate is not None
                ), "Expected a valid certificate object"
                assert (
                    fetched_certificate.get("id") == certificate_id
                ), "Mismatch in certificate ID"
            except Exception as exc:
                errors.append(f"Fetching certificate by ID failed: {str(exc)}")

            # Attempt to retrieve the certificate by name
            try:
                certificate_name = first_certificate.get("name")
                certificate_by_name = client.certificates.get_certificate_by_name(
                    certificate_name
                )
                assert (
                    certificate_by_name is not None
                ), "Expected a valid certificate object when searching by name"
                assert (
                    certificate_by_name.get("id") == certificate_id
                ), "Mismatch in certificate ID when searching by name"
            except Exception as exc:
                errors.append(f"Fetching certificate by name failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert (
            len(errors) == 0
        ), f"Errors occurred during certificate operations test: {errors}"
