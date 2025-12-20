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
from tests.integration.zcc.conftest import MockZCCClient


@pytest.fixture
def fs():
    yield


class TestWebPrivacy:
    """
    Integration Tests for the ZCC Web Privacy API
    """

    @pytest.mark.vcr()
    def test_get_web_privacy(self, fs):
        """Test getting web privacy information"""
        client = MockZCCClient(fs)
        errors = []

        try:
            web_privacy = client.zcc.web_privacy.get_web_privacy()
            # Note: get_web_privacy returns the result directly, not a tuple
            assert web_privacy is not None, "Web privacy info should not be None"
        except Exception as exc:
            errors.append(f"Getting web privacy info failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the web privacy test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_set_web_privacy_info(self, fs):
        """Test setting web privacy information"""
        client = MockZCCClient(fs)
        errors = []

        try:
            # First, get current privacy settings
            current_privacy = client.zcc.web_privacy.get_web_privacy()
            
            if current_privacy:
                # Update with the same values to test the API call
                privacy_info, response, err = client.zcc.web_privacy.set_web_privacy_info(
                    active="1",
                    collect_user_info="1",
                    collect_machine_hostname="1",
                )
                
                if err is None:
                    assert privacy_info is not None, "Updated privacy info should not be None"
                    assert hasattr(privacy_info, 'as_dict'), "Privacy info should have as_dict method"
        except Exception as exc:
            errors.append(f"Setting web privacy info failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the set web privacy test:\n{chr(10).join(errors)}"

