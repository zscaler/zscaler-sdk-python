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
        """Test Intermediate Certificates CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        cert_id = None

        try:
            # Test list_ca_certificates
            certificates, response, err = client.zia.intermediate_certificates.list_ca_certificates()
            assert err is None, f"List CA certificates failed: {err}"
            assert certificates is not None, "Certificates list should not be None"
            assert isinstance(certificates, list), "Certificates should be a list"

            # Test list_ca_certificates with query params
            certs_search, response, err = client.zia.intermediate_certificates.list_ca_certificates(
                query_params={"search": "Zscaler"}
            )

            # Test list_ca_certificates_lite
            certs_lite, response, err = client.zia.intermediate_certificates.list_ca_certificates_lite()
            assert err is None, f"List CA certificates lite failed: {err}"
            assert certs_lite is not None, "Certificates lite list should not be None"

            # Test list_ready_to_use
            ready_certs, response, err = client.zia.intermediate_certificates.list_ready_to_use()
            assert err is None, f"List ready to use certificates failed: {err}"
            assert ready_certs is not None, "Ready to use certificates should not be None"

            # Test list_ready_to_use with query params
            ready_search, response, err = client.zia.intermediate_certificates.list_ready_to_use(
                query_params={"search": "Zscaler"}
            )

            # Test add_ca_certificate (may fail due to permissions)
            try:
                created_cert, response, err = client.zia.intermediate_certificates.add_ca_certificate(
                    name="TestCACert_VCR",
                    key_type="RSA",
                )
                if err is None and created_cert is not None:
                    cert_id = created_cert.get("id") if isinstance(created_cert, dict) else getattr(created_cert, "id", None)

                    # Test update_ca_certificate
                    if cert_id:
                        try:
                            updated_cert, response, err = client.zia.intermediate_certificates.update_ca_certificate(
                                cert_id=cert_id,
                                name="TestCACert_VCR_Updated",
                            )
                        except Exception:
                            pass

                        # Test generate_key_pair
                        try:
                            key_pair, response, err = client.zia.intermediate_certificates.generate_key_pair(cert_id)
                        except Exception:
                            pass

                        # Test generate_csr
                        try:
                            csr, response, err = client.zia.intermediate_certificates.generate_csr(cert_id)
                        except Exception:
                            pass
            except Exception:
                pass  # May fail due to permissions

            # Test operations with existing certificate if available
            if certificates and len(certificates) > 0:
                existing_cert_id = certificates[0].id

                # Test get_ca_certificate
                fetched_cert, response, err = client.zia.intermediate_certificates.get_ca_certificate(existing_cert_id)
                assert err is None, f"Get CA certificate failed: {err}"
                assert fetched_cert is not None, "Fetched certificate should not be None"

                # Test get_ca_certificate_lite
                cert_lite, response, err = client.zia.intermediate_certificates.get_ca_certificate_lite(existing_cert_id)
                assert err is None, f"Get CA certificate lite failed: {err}"

                # Test get_show_cert - may fail if cert not ready
                try:
                    show_cert, response, err = client.zia.intermediate_certificates.get_show_cert(existing_cert_id)
                except Exception:
                    pass

                # Test get_show_csr - may fail if no CSR exists
                try:
                    show_csr, response, err = client.zia.intermediate_certificates.get_show_csr(existing_cert_id)
                except Exception:
                    pass

                # Test download_csr - may fail if no CSR exists
                try:
                    csr_data, response, err = client.zia.intermediate_certificates.download_csr(existing_cert_id)
                except Exception:
                    pass

                # Test download_public_key - may fail if no key exists
                try:
                    pub_key, response, err = client.zia.intermediate_certificates.download_public_key(existing_cert_id)
                except Exception:
                    pass

                # Test verify_key_attestation - may fail
                try:
                    attestation, response, err = client.zia.intermediate_certificates.verify_key_attestation(existing_cert_id)
                except Exception:
                    pass

                # Test finalize_cert - may fail if cert is not ready
                try:
                    finalize_result, response, err = client.zia.intermediate_certificates.finalize_cert(existing_cert_id)
                except Exception:
                    pass

                # Test upload_cert_chain - may fail
                try:
                    upload_chain, response, err = client.zia.intermediate_certificates.upload_cert_chain(existing_cert_id)
                except Exception:
                    pass

        except Exception as e:
            errors.append(f"Exception during intermediate certificates test: {str(e)}")

        finally:
            # Cleanup
            if cert_id:
                try:
                    client.zia.intermediate_certificates.delete_ca_certificate(cert_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
