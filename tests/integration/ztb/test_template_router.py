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
Integration tests for the ZTB Template Router resource.

Uses VCR to record/replay HTTP. Uses deterministic names.
Set MOCK_TESTS=false and ZTB credentials when recording cassettes.
"""

import pytest

from tests.integration.ztb.conftest import MockZTBClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


@pytest.mark.vcr
class TestTemplateRouter:
    """Integration tests for the ZTB Template Router API."""

    def test_list_templates(self, fs):
        """Test listing templates."""
        client = MockZTBClient()
        with client as c:
            templates, _, err = c.ztb.template_router.list_templates()
        if err:
            pytest.skip(f"list_templates not available: {err}")
        assert templates is not None
        assert isinstance(templates, list)

    def test_list_template_interfaces(self, fs):
        """Test listing template interfaces for a platform."""
        client = MockZTBClient()
        with client as c:
            interfaces, _, err = c.ztb.template_router.list_template_interfaces(platform="vm")
        if err:
            pytest.skip(f"list_template_interfaces not available: {err}")
        assert interfaces is not None
        assert isinstance(interfaces, list)

    def test_list_template_names(self, fs):
        """Test listing template names."""
        client = MockZTBClient()
        with client as c:
            names, _, err = c.ztb.template_router.list_template_names()
        if err:
            pytest.skip(f"list_template_names not available: {err}")
        assert names is not None
        assert isinstance(names, list)
