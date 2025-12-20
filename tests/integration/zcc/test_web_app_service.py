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


class TestWebAppService:
    """
    Integration Tests for the ZCC Web App Service API
    """

    @pytest.mark.vcr()
    def test_list_web_app_services(self, fs):
        """Test listing web app services by company"""
        client = MockZCCClient(fs)
        errors = []

        try:
            services, response, err = client.zcc.web_app_service.list_by_company()
            assert err is None, f"Error listing web app services: {err}"
            assert isinstance(services, list), "Expected a list of web app services"
            
            # Verify response structure if we have services
            if services:
                service = services[0]
                assert hasattr(service, 'as_dict'), "Web app service should have as_dict method"
        except Exception as exc:
            errors.append(f"Listing web app services failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the web app service test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_web_app_services_with_pagination(self, fs):
        """Test listing web app services with pagination"""
        client = MockZCCClient(fs)
        errors = []

        try:
            services, response, err = client.zcc.web_app_service.list_by_company(
                query_params={"page": 1, "page_size": 10}
            )
            assert err is None, f"Error listing web app services with pagination: {err}"
            assert isinstance(services, list), "Expected a list of web app services"
        except Exception as exc:
            errors.append(f"Listing web app services with pagination failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the paginated web app service test:\n{chr(10).join(errors)}"

    @pytest.mark.vcr()
    def test_list_web_app_services_with_search(self, fs):
        """Test listing web app services with search filter"""
        client = MockZCCClient(fs)
        errors = []

        try:
            services, response, err = client.zcc.web_app_service.list_by_company(
                query_params={"search": "test"}
            )
            assert err is None, f"Error listing web app services with search: {err}"
            assert isinstance(services, list), "Expected a list of web app services"
        except Exception as exc:
            errors.append(f"Listing web app services with search failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during the search web app service test:\n{chr(10).join(errors)}"

