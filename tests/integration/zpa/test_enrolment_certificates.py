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
    Integration Tests for the enrolment certificates.
    """

    def test_enrolment_certificate(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        # Attempt to list all enrolment certificates
        try:
            certs = client.certificates.list_enrolment()
            assert isinstance(certs, list), "Expected a list of enrolment certificates"
        except Exception as exc:
            errors.append(f"Listing enrolment certificates failed: {str(exc)}")

        # Certificate names to attempt retrieval
        cert_names = ["Root", "Client", "Connector", "Service Edge"]

        for name in cert_names:
            # Attempt to retrieve each enrolment certificate by name
            try:
                certificate_by_name = client.certificates.get_enrolment_cert_by_name(name)
                if certificate_by_name is not None:
                    assert certificate_by_name.get("name") == name, f"Mismatch in certificate name for '{name}'"
                else:
                    errors.append(f"Certificate named '{name}' not found")
            except Exception as exc:
                errors.append(f"Retrieving certificate by name '{name}' failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during enrolment certificate operations test: {errors}"
