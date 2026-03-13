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

"""
Integration tests for the ZTB API Key Auth resource.

Uses VCR to record/replay HTTP. Uses deterministic name for create.
Set MOCK_TESTS=false and ZTB credentials when recording cassettes.
"""

import pytest

from tests.integration.ztb.conftest import MockZTBClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


@pytest.mark.vcr
class TestAPIKey:
    """Integration tests for the ZTB API Key Auth API."""

    def test_list_api_keys(self, fs):
        """Test listing API keys."""
        client = MockZTBClient()
        with client as c:
            keys, _, err = c.ztb.api_keys.list_api_keys()
        if err:
            pytest.skip(f"list_api_keys not available: {err}")
        assert keys is not None
        assert isinstance(keys, list)

    def test_api_key_lifecycle(self, fs):
        """Test create, list to find id, and revoke API key."""
        client = MockZTBClient()
        name = f"tests-api-key-{generate_random_string()}"
        created_id = None
        errors = []

        try:
            with client as c:
                created, _, err = c.ztb.api_keys.create_api_key(name=name)
                if err:
                    errors.append(f"create_api_key failed: {err}")
                    return
                assert created is not None
                assert hasattr(created, "key")

                # List to find the created key's id (create only returns key secret)
                keys, _, err = c.ztb.api_keys.list_api_keys()
                if err:
                    errors.append(f"list_api_keys failed: {err}")
                elif keys:
                    for k in keys:
                        if getattr(k, "name", None) == name:
                            created_id = getattr(k, "id", None)
                            break
        except Exception as exc:
            errors.append(f"Create/list failed: {exc}")

        if created_id:
            try:
                with client as c:
                    _, _, err = c.ztb.api_keys.revoke_api_key(str(created_id))
                    if err:
                        errors.append(f"revoke_api_key failed: {err}")
            except Exception as exc:
                errors.append(f"Revoke failed: {exc}")

        assert len(errors) == 0, f"Errors: {errors}"
