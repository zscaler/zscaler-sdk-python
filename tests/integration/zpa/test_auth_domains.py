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


class TestAuthDomains:
    """
    Integration Tests for the Auth Domains.
    """

    def test_auth_domains(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # Retrieve authentication domains
            auth_domains, _, err = client.zpa.authdomains.get_auth_domains()
            assert err is None, f"Error retrieving auth domains: {err}"
            assert auth_domains is not None, "Auth domains response is None"
            assert isinstance(auth_domains, dict), "Auth domains should be a dictionary"
            assert "authDomains" in auth_domains, "Missing 'authDomains' key in response"
            assert isinstance(auth_domains["authDomains"], list), "'authDomains' should be a list"
            assert len(auth_domains["authDomains"]) > 0, "Auth domains list is empty"
        except Exception as exc:
            errors.append(exc)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the auth domains test: {errors}"
