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
from box import Box, BoxList

from tests.integration.zia.conftest import MockZIAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestURLCategories:
    """
    Integration Tests for the URL Categories
    """

    # def test_url_categories(self, fs):
    #     client = MockZIAClient(fs)
    #     errors = []

    #     category_name = "tests-" + generate_random_string()
    #     category_description = "tests-" + generate_random_string()
    #     category_id = None

    #     try:
    #         # Step 1: Create a new URL category
    #         try:
    #             created_category, _, error = client.zia.url_categories.add_url_category(
    #                 configured_name=category_name,
    #                 description=category_description,
    #                 super_category="BUSINESS_AND_ECONOMY",
    #                 keywords=["microsoft"],
    #                 custom_category=True,
    #                 db_categorized_urls=[".creditkarma.com", ".youku.com"],
    #                 type="URL_CATEGORY",
    #                 urls=[".coupons.com"],
    #                 ip_ranges=["3.217.228.0/25", "3.235.112.0/24"],
    #                 ip_ranges_retaining_parent_category=["13.107.6.152/31"],
    #             )
    #             assert error is None, f"Error creating URL category: {error}"
    #             category_id = created_category.id
    #             assert created_category.configured_name == category_name
    #             assert created_category.description == category_description
    #         except Exception as exc:
    #             errors.append(f"Failed to add URL category: {exc}")

    #         # Step 2: Retrieve the created URL category
    #         try:
    #             retrieved_category, _, error = client.zia.url_categories.get_category(category_id)
    #             assert error is None, f"Error retrieving category: {error}"
    #             assert retrieved_category.id == category_id
    #             assert retrieved_category.configured_name == category_name
    #         except Exception as exc:
    #             errors.append(f"Failed to retrieve URL category: {exc}")

    #         # Step 3: Update the URL category
    #         try:
    #             updated_name = category_name + "-Updated"
    #             update_category, _, error = client.zia.url_categories.update_url_category(
    #                 category_id=category_id,
    #                 configured_name=updated_name,
    #                 description=category_description,
    #                 super_category="BUSINESS_AND_ECONOMY",
    #                 keywords=["microsoft"],
    #                 custom_category=True,
    #                 db_categorized_urls=[".creditkarma.com", ".youku.com"],
    #                 urls=[".coupons.com"],
    #                 ip_ranges=["3.217.228.0/25", "3.235.112.0/24"],
    #                 ip_ranges_retaining_parent_category=["13.107.6.152/31"],
    #                 type="URL_CATEGORY"
    #             )
    #             assert error is None, f"Error updating URL category: {error}"
    #             assert update_category.configured_name == updated_name
    #         except Exception as exc:
    #             errors.append(f"Failed to update URL category: {exc}")

    #         # Step 4: List categories and validate presence
    #         try:
    #             category_list, _, error = client.zia.url_categories.list_categories(
    #                 query_params={"search": updated_name}
    #             )
    #             assert error is None, f"Error listing categories: {error}"
    #             assert any(c.id == category_id for c in category_list), "Updated category not found in list"
    #         except Exception as exc:
    #             errors.append(f"Failed to list URL categories: {exc}")

    #     finally:
    #         # Step 5: Cleanup
    #         if category_id:
    #             try:
    #                 _, _, error = client.zia.url_categories.delete_category(category_id)
    #                 assert error is None, f"Error deleting category: {error}"
    #             except Exception as exc:
    #                 errors.append(f"Cleanup failed: {exc}")

    #     # Final assertion
    #     assert len(errors) == 0, f"Errors occurred during the URL category lifecycle test:\n{chr(10).join(errors)}"

    # def test_lookup(self, fs):
    #     client = MockZIAClient(fs)
    #     errors = []

    #     # Define a test-safe list of common domains
    #     urls = [
    #         "google.com",
    #         "youtube.com",
    #         "facebook.com",
    #         "baidu.com",
    #         "wikipedia.org",
    #         "yahoo.com",
    #         "reddit.com",
    #         "google.co.in",
    #         "qq.com",
    #         "taobao.com",
    #         "amazon.com",
    #         "tmall.com",
    #         "twitter.com",
    #         "google.co.jp",
    #         "sohu.com",
    #         "live.com",
    #         "vk.com",
    #         "instagram.com",
    #         "sina.com",
    #         "360.cn",
    #         "google.de",
    #         "jd.com",
    #         "google.co.uk",
    #         "linkedin.com",
    #         "weibo.com",
    #         "google.fr",
    #         "google.ru",
    #         "yahoo.co.jp",
    #         "yandex.ru",
    #         "netflix.com",
    #         "t.co",
    #         "hao123.com",
    #         "imgur.com",
    #         "google.it",
    #         "ebay.com",
    #         "pornhub.com",
    #         "google.es",
    #         "detail.tmall.com",
    #         "WordPress.com",
    #         "msn.com",
    #         "aliexpress.com",
    #         "bing.com",
    #         "tumblr.com",
    #         "google.ca",
    #         "livejasmin.com",
    #         "microsoft.com",
    #         "stackoverflow.com",
    #         "twitch.tv",
    #         "Soso.com",
    #         "blogspot.com",
    #         "ok.ru",
    #         "apple.com",
    #         "Naver.com",
    #         "mail.ru",
    #         "imdb.com",
    #         "popads.net",
    #         "tianya.cn",
    #         "office.com",
    #         "google.co.kr",
    #         "github.com",
    #         "pinterest.com",
    #         "paypal.com",
    #         "diply.com",
    #         "amazon.de",
    #         "microsoftonline.com",
    #         "onclckds.com",
    #         "amazon.co.uk",
    #         "txxx.com",
    #         "adobe.com",
    #         "wikia.com",
    #         "cnzz.com",
    #         "xhamster.com",
    #         "coccoc.com",
    #         "bongacams.com",
    #         "fc2.com",
    #         "pixnet.net",
    #         "google.pl",
    #         "dropbox.com",
    #         "googleusercontent.com",
    #         "gmw.cn",
    #         "whatsapp.com",
    #         "google.co.th",
    #         "soundcloud.com",
    #         "google.nl",
    #         "xvideos.com",
    #         "booking.com",
    #         "rakuten.co.jp",
    #         "nytimes.com",
    #         "alibaba.com",
    #         "bet365.com",
    #         "ebay.co.uk",
    #         "quora.com",
    #         "avito.ru",
    #         "dailymail.co.uk",
    #         "globo.com",
    #         "uol.com",
    #         "nicovideo.jp",
    #         "walmart.com",
    #         "redtube.com",
    #         "go2cloud.org",
    #     ]

    #     try:
    #         results = client.zia.url_categories.lookup(urls)
    #         assert isinstance(results, list), "Expected results to be a list"
    #         assert len(results) > 0, "Expected at least one result from lookup"

    #         for result in results:
    #             assert "url" in result, f"Missing 'url' in result: {result}"
    #             assert "urlClassifications" in result or "customCategory" in result, \
    #                 f"No classification found for: {result.get('url', 'Unknown')}"

    #     except Exception as exc:
    #         errors.append(f"URL lookup failed: {exc}")

    #     # Final assertion
    #     assert len(errors) == 0, f"Errors occurred during URL lookup test:\n{chr(10).join(errors)}"

    def test_get_quota(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            quota_info = client.zia.url_categories.get_quota()

            assert isinstance(quota_info, dict), "Quota information should be a dictionary"

            # ✅ Validate expected keys from real API response
            assert "remainingUrlsQuota" in quota_info, "Missing 'remainingUrlsQuota' in quota data"
            assert "uniqueUrlsProvisioned" in quota_info, "Missing 'uniqueUrlsProvisioned' in quota data"

        except Exception as exc:
            errors.append(f"Getting URL category quota failed: {exc}")

        assert len(errors) == 0, f"Errors occurred during quota retrieval test:\n{chr(10).join(errors)}"