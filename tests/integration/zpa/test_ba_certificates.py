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


import cryptography.hazmat.backends as crypto_backends
import cryptography.hazmat.primitives.asymmetric.rsa as rsa
import cryptography.hazmat.primitives.serialization as serialization
from cryptography.hazmat.primitives import hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
import pytest
from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestBACertificates:
    """
    Integration Tests for the BA Certificate
    """

    def generate_root_certificate(self, name):
        # Generate private key for root certificate
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=crypto_backends.default_backend())

        # Build the certificate
        subject = issuer = x509.Name(
            [
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "San Jose"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "BD-RedHat"),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "IT Department"),
                x509.NameAttribute(NameOID.COMMON_NAME, "bd-redhat.com"),
            ]
        )
        certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))  # Valid for 10 years
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(private_key, hashes.SHA256(), crypto_backends.default_backend())
        )

        # Convert to PEM format
        pem = certificate.public_bytes(serialization.Encoding.PEM)
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

        return pem + key_pem  # Combine both PEMs into one to simulate merged key and cert

    def test_ba_certificate(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        cert_id = None  # Initialize cert_id

        cert_name = "tests-" + generate_random_string()

        try:
            # # Generate a root certificate
            cert_blob = self.generate_root_certificate(cert_name)

            # # Create a new certificate
            try:
                created_cert, _, err = client.zpa.certificates.add_certificate(
                    name=cert_name, cert_blob=cert_blob.decode("utf-8")
                )
                assert err is None, f"Certificate creation error: {err}"
                assert created_cert and created_cert.id, "Failed to create certificate: No ID returned"
                cert_id = created_cert.id
            except Exception as exc:
                errors.append(f"Certificate creation failed: {str(exc)}")

            # Retrieve the specific certificate
            try:
                retrieved_cert, _, err = client.zpa.certificates.get_certificate(cert_id)
                assert err is None, f"Certificate retrieval error: {err}"
                assert retrieved_cert, "Failed to retrieve certificate: Response is None"
                assert retrieved_cert.id == cert_id, "Retrieved certificate ID mismatch"
                assert retrieved_cert.name == cert_name, "Certificate name mismatch"
            except Exception as exc:
                errors.append(f"Retrieving certificate failed: {str(exc)}")

            # List all issued certificates and verify the created certificate is listed
            try:
                cert_list, _, err = client.zpa.certificates.list_issued_certificates()
                assert err is None, f"Certificate listing error: {err}"
                assert any(cert.id == cert_id for cert in cert_list), "Created certificate not found in the list"
            except Exception as exc:
                errors.append(f"Listing issued certificates failed: {str(exc)}")

        finally:
            # Cleanup: Delete the segment group if it was created
            if cert_id:
                try:
                    delete_response, _, err = client.zpa.certificates.delete_certificate(cert_id)
                    assert err is None, f"Error deleting Certificate: {err}"
                    # Since a 204 No Content response returns None, we assert that delete_response is None
                    assert delete_response is None, f"Expected None for 204 No Content, got {delete_response}"
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed for Certificate ID {cert_id}: {cleanup_exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the Certificate lifecycle test: {errors}"
