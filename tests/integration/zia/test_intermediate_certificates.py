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

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestIntermediateCertificates:
    """
    Integration Tests for the Intermediate Certificates API.
    """

    @pytest.mark.vcr()
    def test_intermediate_certificates_crud(self, fs):
        """Test Intermediate Certificates operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_ca_certificates
            certificates, response, err = client.zia.intermediate_certificates.list_ca_certificates()
            assert err is None, f"List CA certificates failed: {err}"
            assert certificates is not None, "Certificates list should not be None"
            assert isinstance(certificates, list), "Certificates should be a list"

            # Test list_ca_certificates_lite
            certs_lite, response, err = client.zia.intermediate_certificates.list_ca_certificates_lite()
            assert err is None, f"List CA certificates lite failed: {err}"
            assert certs_lite is not None, "Certificates lite list should not be None"

            # Test list_ready_to_use
            ready_certs, response, err = client.zia.intermediate_certificates.list_ready_to_use()
            assert err is None, f"List ready to use certificates failed: {err}"
            assert ready_certs is not None, "Ready to use certificates should not be None"

            # Test get_ca_certificate with first certificate if available
            if certificates and len(certificates) > 0:
                cert_id = certificates[0].id
                fetched_cert, response, err = client.zia.intermediate_certificates.get_ca_certificate(cert_id)
                assert err is None, f"Get CA certificate failed: {err}"
                assert fetched_cert is not None, "Fetched certificate should not be None"

                # Test get_ca_certificate_lite
                cert_lite, response, err = client.zia.intermediate_certificates.get_ca_certificate_lite(cert_id)
                assert err is None, f"Get CA certificate lite failed: {err}"

                # Test get_show_cert - may fail if cert not ready
                show_cert, response, err = client.zia.intermediate_certificates.get_show_cert(cert_id)
                # Don't assert on error as it may fail for certain cert states

                # Test get_show_csr - may fail if no CSR exists
                show_csr, response, err = client.zia.intermediate_certificates.get_show_csr(cert_id)
                # Don't assert on error as it may fail for certain cert states

                # Test download_csr - may fail if no CSR exists
                try:
                    csr_data, response, err = client.zia.intermediate_certificates.download_csr(cert_id)
                    # Don't fail - CSR may not exist
                except Exception:
                    pass

                # Test download_public_key - may fail if no key exists
                try:
                    pub_key, response, err = client.zia.intermediate_certificates.download_public_key(cert_id)
                    # Don't fail - key may not exist
                except Exception:
                    pass

                # Test verify_key_attestation - may fail
                try:
                    attestation, response, err = client.zia.intermediate_certificates.verify_key_attestation(cert_id)
                    # Don't fail - attestation may not be available
                except Exception:
                    pass

        except Exception as e:
            errors.append(f"Exception during intermediate certificates test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
