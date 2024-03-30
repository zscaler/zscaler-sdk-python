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


import responses
from box import Box
from responses import matchers


@responses.activate
def test_ssl_inspection_get_csr(zia):
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/sslSettings/downloadcsr",
        body="test",
        status=200,
    )
    resp = zia.ssl.get_csr()

    assert isinstance(resp, str)
    assert resp == "test"


@responses.activate
def test_ssl_inspection_get_intermediate_ca(zia):
    intermediate_cert = {
        "cert_name": "test.pem",
        "city": "Test",
        "comm_name": "example.com",
        "country": "COUNTRY_TEST",
        "dept_name": "Test",
        "exp_date": "31-Feb-2029",
        "key_size": 2048,
        "org_name": "example.com",
        "sha1fingerprint": "XX YY ZZ",
        "signature_algorithm": "SHA_256",
        "state": "TEST",
    }
    responses.add(
        method="GET",
        url="https://zsapi.zscaler.net/api/v1/sslSettings/showcert",
        json=intermediate_cert,
        status=200,
    )
    resp = zia.ssl.get_intermediate_ca()
    assert isinstance(resp, Box)
    assert resp.cert_name == "test.pem"


@responses.activate
def test_ssl_inspection_generate_csr(zia):
    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/sslSettings/generatecsr",
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "certName": "test",
                    "commName": "test",
                    "orgName": "test",
                    "deptName": "test",
                    "city": "test",
                    "state": "test",
                    "country": "test",
                    "signatureAlgorithm": "test",
                }
            )
        ],
    )
    resp = zia.ssl.generate_csr(
        cert_name="test",
        cn="test",
        org="test",
        dept="test",
        city="test",
        state="test",
        country="test",
        signature="test",
    )

    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_ssl_inspection_upload_int_ca_cert(zia):
    req_file = str.encode("test")

    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/sslSettings/uploadcert/text",
        match=[matchers.multipart_matcher({"fileUpload": req_file})],
        status=200,
    )
    resp = zia.ssl.upload_int_ca_cert(req_file)
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_ssl_inspection_upload_int_ca_chain(zia):
    req_file = str.encode("test")

    responses.add(
        method="POST",
        url="https://zsapi.zscaler.net/api/v1/sslSettings/uploadcertchain/text",
        match=[matchers.multipart_matcher({"fileUpload": req_file})],
        status=200,
    )
    resp = zia.ssl.upload_int_ca_chain(req_file)
    assert isinstance(resp, int)
    assert resp == 200


@responses.activate
def test_ssl_inspection_delete_int_chain(zia):
    responses.add(
        method="DELETE",
        url="https://zsapi.zscaler.net/api/v1/sslSettings/certchain",
        status=204,
    )
    resp = zia.ssl.delete_int_chain()
    assert isinstance(resp, int)
    assert resp == 204
