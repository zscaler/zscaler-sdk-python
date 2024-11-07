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
            # Generate a root certificate
            cert_blob = self.generate_root_certificate(cert_name)

            # Create a new certificate
            try:
                created_cert = client.certificates.add_certificate(name=cert_name, cert_blob=cert_blob.decode("utf-8"))
                cert_id = created_cert.id if created_cert and "id" in created_cert else None
                if not cert_id:
                    errors.append("Failed to create certificate")
            except Exception as exc:
                errors.append(f"Certificate creation failed: {str(exc)}")

            # Retrieve the specific certificate
            try:
                retrieved_cert = client.certificates.get_certificate(cert_id)
                assert retrieved_cert.id == cert_id, "Retrieved certificate ID does not match"
            except Exception as exc:
                errors.append(f"Retrieving certificate failed: {str(exc)}")

            # List all issued certificates and verify the created certificate is listed
            try:
                all_certs = client.certificates.list_issued_certificates()
                assert any(cert.id == cert_id for cert in all_certs), "Certificate not found in issued list"
            except Exception as exc:
                errors.append(f"Listing issued certificates failed: {str(exc)}")

        except Exception as exc:
            errors.append(f"Error during certificate management: {str(exc)}")

        finally:
            # Attempt to delete the certificate if it was created
            if cert_id:
                try:
                    delete_response = client.certificates.delete_certificate(cert_id)
                    if delete_response != 204:
                        errors.append(f"Failed to delete certificate, expected 204 status code, received {delete_response}")
                except Exception as exc:
                    errors.append(f"Certificate deletion failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during the test: {errors}"


class TestBaListCertificate:
    """
    Integration Tests for the list certificates.
    """

    def test_ba_list_certificate(self, fs):
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
                fetched_certificate = client.certificates.get_certificate(certificate_id)
                assert fetched_certificate is not None, "Expected a valid certificate object"
                assert fetched_certificate.get("id") == certificate_id, "Mismatch in certificate ID"
            except Exception as exc:
                errors.append(f"Fetching certificate by ID failed: {str(exc)}")

            # Attempt to retrieve the certificate by name
            try:
                certificate_name = first_certificate.get("name")
                certificate_by_name = client.certificates.get_certificate_by_name(certificate_name)
                assert certificate_by_name is not None, "Expected a valid certificate object when searching by name"
                assert certificate_by_name.get("id") == certificate_id, "Mismatch in certificate ID when searching by name"
            except Exception as exc:
                errors.append(f"Fetching certificate by name failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during certificate operations test: {errors}"
