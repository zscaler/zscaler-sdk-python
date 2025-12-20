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


class TestCompanyInfo:
    """
    Integration Tests for the ZCC Company Info API
    """

    @pytest.mark.vcr()
    def test_get_company_info(self, fs):
        """Test getting company information"""
        client = MockZCCClient(fs)
        errors = []

        try:
            company_info, response, err = client.zcc.company.get_company_info()
            assert err is None, f"Error getting company info: {err}"
            assert company_info is not None, "Company info should not be None"
            assert isinstance(company_info, list), "Expected a list of company info"
            
            # Verify response structure if we have company info
            if company_info:
                info = company_info[0]
                assert hasattr(info, 'as_dict'), "Company info should have as_dict method"
        except Exception as exc:
            errors.append(f"Getting company info failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the company info test:\n{chr(10).join(errors)}"

