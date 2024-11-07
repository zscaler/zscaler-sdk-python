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


from box import Box

from zscaler.zia import ZIAClient


class SSLInspectionAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def get_csr(self) -> str:
        """
        Downloads a CSR after it has been generated.

        Returns:
            :obj:`str`: Base64 encoded PKCS#10 CSR text.

        Examples:
            Retrieve the CSR for use in another function.

            >>> csr = zia.ssl.get_csr()

        """
        return self.rest.get("sslSettings/downloadcsr").text

    def get_intermediate_ca(self) -> Box:
        """
        Returns information on the signed Intermediate Root CA certificate.

        Returns:
            :obj:`Box`: The Intermediate Root CA resource record.

        Examples:
            >>> pprint(zia.ssl.get_intermediate_ca())

        """
        return self.rest.get("sslSettings/showcert")

    def generate_csr(
        self,
        cert_name: str,
        cn: str,
        org: str,
        dept: str,
        city: str,
        state: str,
        country: str,
        signature: str,
    ) -> int:
        """
        Generates a Certificate Signing Request.

        Args:
            cert_name (str): Certificate Name
            cn (str): Common Name
            org (str): Organisation
            dept (str): Department
            city (str): City
            state (str): State
            country (str): Country. Must be in the two-letter country code (ISO 3166-1 alpha-2) format and prefixed by
                `COUNTRY`. E.g.::

                    United States = US = COUNTRY_US
                    Australia = AU = COUNTRY_AU

            signature  (str): Certificate signature algorithm. Accepted values are `SHA_1` and `SHA_256`.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zia.ssl.generate_csr(cert_name='Example.com Intermediate CA 2',
            ...    cn='Example.com Intermediate CA 2',
            ...    org='Example.com',
            ...    dept='IT',
            ...    city='Sydney',
            ...    state='NSW',
            ...    country='COUNTRY_AU',
            ...    signature='SHA_256')

        """
        payload = {
            "certName": cert_name,
            "commName": cn,
            "orgName": org,
            "deptName": dept,
            "city": city,
            "state": state,
            "country": country,
            "signatureAlgorithm": signature,
        }

        return self.rest.post("sslSettings/generatecsr", json=payload, box=False).status_code

    def upload_int_ca_cert(self, cert: tuple) -> int:
        """
        Uploads a signed Intermediate Root CA certificate.

        Args:
            cert (tuple): The Intermediate Root CA certificate tuple in the following format, where `int_ca_pem` is a
                ``File Object`` representation of the Intermediate Root CA certificate PEM file::

                ('filename.pem', int_ca_pem)

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            Upload an Intermediate Root CA certificate from a file:

            >>> zia.ssl.upload_int_ca_cert(('int_ca.pem', open('int_ca.pem', 'rb')))

        """

        payload = {"fileUpload": cert}

        return self.rest.post("sslSettings/uploadcert/text", files=payload, box=False).status_code

    def upload_int_ca_chain(self, cert: tuple) -> int:
        """
        Uploads the Intermediate Root CA certificate chain.

        Args:
            cert (tuple): The Intermediate Root CA chain certificate tuple in the following format, where
                `int_ca_chain_pem` is a ``File Object`` representation of the Intermediate Root CA certificate chain
                PEM file::

                ('filename.pem', int_ca_chain_pem)


        Returns:
            :obj:`int`: The status code for the operation

        Examples:
            Upload an Intermediate Root CA chain from a file:

            >>> zia.ssl.upload_int_ca_chain(('int_ca_chain.pem', open('int_ca_chain.pem', 'rb')))

        """

        payload = {"fileUpload": cert}

        return self.rest.post("sslSettings/uploadcertchain/text", files=payload, box=False).status_code

    def delete_int_chain(self) -> int:
        """
        Deletes the Intermediate Root CA certificate chain.

        Returns:
            :obj:`int`: The status code for the operation.

        """
        return self.rest.delete("sslSettings/certchain", box=False).status_code
