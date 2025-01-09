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

        # Certificate names to attempt retrieval
        cert_names = ["Root", "Client", "Connector", "Service Edge"]

        # Search for each certificate by name using query_params
        for cert_name in cert_names:
            try:
                # Perform search with the query_params
                certs, response, error = client.zpa.enrollment_certificates.list_enrolment(
                    query_params={"search": cert_name}
                )
                
                # Validate response
                assert error is None, f"Error occurred when searching for '{cert_name}': {error}"
                assert isinstance(certs, list), f"Expected a list when searching for '{cert_name}'"
                assert any(cert.name == cert_name for cert in certs), f"Certificate '{cert_name}' not found in the list"
                
            except Exception as exc:
                errors.append(f"Searching for enrolment certificate '{cert_name}' failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during enrolment certificate operations test: {errors}"
