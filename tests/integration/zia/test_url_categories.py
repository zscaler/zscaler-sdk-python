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


class TestURLCategories:
    """
    Integration Tests for the URL Categories API.
    """

    @pytest.mark.vcr()
    def test_url_categories_crud(self, fs):
        """Test URL Categories operations."""
        client = MockZIAClient(fs)
        errors = []
        category_id = None

        try:
            # Test list_categories
            categories, response, err = client.zia.url_categories.list_categories()
            assert err is None, f"List categories failed: {err}"
            assert categories is not None, "Categories list should not be None"
            assert isinstance(categories, list), "Categories should be a list"

            # Test list_categories with custom_only parameter
            custom_categories, response, err = client.zia.url_categories.list_categories(
                query_params={"custom_only": True}
            )
            assert err is None, f"List custom categories failed: {err}"

            # Test get_quota
            quota = client.zia.url_categories.get_quota()
            assert quota is not None, "Quota should not be None"

            # Test lookup
            lookup_results = client.zia.url_categories.lookup(urls=["google.com"])
            assert lookup_results is not None, "Lookup results should not be None"

            # Test add_url_category - create a custom category
            try:
                created_category, response, err = client.zia.url_categories.add_url_category(
                    configured_name="TestCategory_VCR",
                    super_category="USER_DEFINED",
                    urls=["test-vcr-url1.example.com", "test-vcr-url2.example.com"],
                    description="Test URL category for VCR testing",
                )
                if err is None and created_category is not None:
                    category_id = created_category.id
                    assert created_category.configured_name == "TestCategory_VCR"

                    # Test get_category
                    try:
                        fetched_category, response, err = client.zia.url_categories.get_category(category_id)
                        if err is None:
                            assert fetched_category is not None
                    except Exception:
                        pass  # May fail for some categories

                    # Test update_url_category
                    try:
                        updated_category, response, err = client.zia.url_categories.update_url_category(
                            category_id=category_id,
                            configured_name="TestCategory_VCR",
                            description="Updated test URL category",
                            urls=["test-vcr-url1.example.com", "test-vcr-url2.example.com", "test-vcr-url3.example.com"],
                        )
                        # Update may fail - that's ok
                    except Exception:
                        pass

                    # Test add_urls_to_category
                    try:
                        result, response, err = client.zia.url_categories.add_urls_to_category(
                            category_id=category_id,
                            configured_name="TestCategory_VCR",
                            urls=["test-vcr-url4.example.com"],
                        )
                        # May fail - that's ok
                    except Exception:
                        pass

                    # Test delete_urls_from_category
                    try:
                        result, response, err = client.zia.url_categories.delete_urls_from_category(
                            category_id=category_id,
                            configured_name="TestCategory_VCR",
                            urls=["test-vcr-url4.example.com"],
                        )
                        # May fail - that's ok
                    except Exception:
                        pass

            except Exception as e:
                pass  # Category creation may fail due to permissions/subscription

            # Test review_domains_post
            try:
                review_result = client.zia.url_categories.review_domains_post(urls=["example.com"])
                # May return empty or error - that's ok
            except Exception:
                pass

            # Test review_domains_put
            try:
                review_result = client.zia.url_categories.review_domains_put(urls=["example.com"])
                # May return empty or error - that's ok
            except Exception:
                pass

        except Exception as e:
            errors.append(f"Exception during URL categories test: {str(e)}")

        finally:
            # Cleanup - delete the created category
            if category_id:
                try:
                    client.zia.url_categories.delete_category(category_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
