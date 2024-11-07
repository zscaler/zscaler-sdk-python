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


class TestCBICertificates:
    """
    Integration Tests for the Cloud Browser Isolation Certificate
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
            .not_valid_after(
                # Valid for 10 years
                datetime.datetime.utcnow()
                + datetime.timedelta(days=3650)
            )
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=None),
                critical=True,
            )
            .sign(private_key, hashes.SHA256(), crypto_backends.default_backend())
        )

        # Convert to PEM format
        pem = certificate.public_bytes(serialization.Encoding.PEM)
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

        return pem, key_pem

    def test_cbi_certificate(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        cert_id = None  # Initialize cert_id

        cert_name = "tests-" + generate_random_string()

        try:
            # Generate a root certificate
            pem, _ = self.generate_root_certificate(cert_name)

            try:
                # Create a new certificate
                created_cert = client.isolation.add_certificate(name=cert_name, pem=pem.decode("utf-8"))
                cert_id = created_cert.id if created_cert and "id" in created_cert else None
                if not cert_id:
                    errors.append("Failed to create certificate")
            except Exception as exc:
                errors.append(f"Certificate creation failed: {str(exc)}")

            if cert_id:
                try:
                    # Update the certificate
                    updated_name = cert_name + " Updated"
                    client.isolation.update_certificate(cert_id, name=updated_name)
                    updated_cert = client.isolation.get_certificate(cert_id)
                    if updated_cert.name != updated_name:
                        errors.append("Failed to update certificate name")
                except Exception as exc:
                    errors.append(f"Certificate update failed: {str(exc)}")

                try:
                    # Verify the certificate by listing
                    certs = client.isolation.list_certificates()
                    if cert_id not in [cert.id for cert in certs]:
                        errors.append("Certificate not found in list")
                except Exception as exc:
                    errors.append(f"Listing certificates failed: {str(exc)}")

        except Exception as exc:
            errors.append(f"Error during certificate management: {str(exc)}")

        finally:
            # Attempt to delete the certificate if it was created
            if cert_id:
                try:
                    # Delete the certificate
                    delete_response_code = client.isolation.delete_certificate(cert_id)
                    if str(delete_response_code) != "200":
                        errors.append(f"Failed to delete certificate, status code {delete_response_code}")
                except Exception as exc:
                    errors.append(f"Certificate deletion failed: {str(exc)}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred during the test: {errors}"
