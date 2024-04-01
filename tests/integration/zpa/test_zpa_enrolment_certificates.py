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

class TestEnrolmentCertificate:
    """
    Integration Tests for the enrolment certificates
    """

    @pytest.mark.asyncio
    async def test_enrolment_certificate(self, fs): 
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all certificatess
            certs = client.certificates.list_enrolment()
            assert isinstance(certs, list), "Expected a list of certificates"
            if certs:  # If there are any certificatess
                # Select the first certificates for further testing
                first_certificate = certs[0]
                certificate_id = first_certificate.get('id')
                
                # Fetch the selected certificates by its ID
                fetched_certificate = client.certificates.get_enrolment(certificate_id)
                assert fetched_certificate is not None, "Expected a valid certificates object"
                assert fetched_certificate.get('id') == certificate_id, "Mismatch in certificates ID"

                # Attempt to retrieve the certificates by name
                certificate_name = first_certificate.get('name')
                certificate_by_name= client.certificates.get_enrolment_cert_by_name(certificate_name)
                assert certificate_by_name is not None, "Expected a valid certificates object when searching by name"
                assert certificate_by_name.get('id') == certificate_id, "Mismatch in certificates ID when searching by name"
        except Exception as exc:
            errors.append(exc)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during certificates operations test: {errors}"



