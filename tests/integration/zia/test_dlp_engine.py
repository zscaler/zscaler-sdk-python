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


class TestDLPEngine:
    """
    Integration Tests for the DLP Engine API.
    """

    @pytest.mark.vcr()
    def test_dlp_engine_operations(self, fs):
        """Test DLP Engine operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_dlp_engines
            engines, response, err = client.zia.dlp_engine.list_dlp_engines()
            assert err is None, f"List DLP engines failed: {err}"
            assert engines is not None, "Engines should not be None"
            assert isinstance(engines, list), "Engines should be a list"

            # Test list_dlp_engines_lite
            engines_lite, response, err = client.zia.dlp_engine.list_dlp_engines_lite()
            assert err is None, f"List DLP engines lite failed: {err}"

            # Test get_dlp_engines if available
            if engines and len(engines) > 0:
                engine_id = engines[0].id
                fetched_engine, response, err = client.zia.dlp_engine.get_dlp_engines(engine_id)
                assert err is None, f"Get DLP engine failed: {err}"
                assert fetched_engine is not None, "Fetched engine should not be None"

            # Test validate_dlp_expression
            valid_result, response, err = client.zia.dlp_engine.validate_dlp_expression("test")
            # May fail with invalid expression - that's ok

        except Exception as e:
            errors.append(f"Exception during DLP engine test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

