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

from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection


class URLCategory(ZscalerObject):
    """
    A class representing the URL Category in Zscaler.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.configured_name = config["configuredName"] if "configuredName" in config else None
            self.super_category = config["superCategory"] if "superCategory" in config else None

            self.keywords = ZscalerCollection.form_list(config["keywords"] if "keywords" in config else [], str)

            self.keywords_retaining_parent_category = ZscalerCollection.form_list(
                config["keywordsRetainingParentCategory"] if "keywordsRetainingParentCategory" in config else [], str
            )

            self.urls = ZscalerCollection.form_list(config["urls"] if "urls" in config else [], str)

            self.db_categorized_urls = ZscalerCollection.form_list(
                config["dbCategorizedUrls"] if "dbCategorizedUrls" in config else [], str
            )

            self.ip_ranges = ZscalerCollection.form_list(config["ipRanges"] if "ipRanges" in config else [], str)

            self.ip_ranges_retaining_parent_category = ZscalerCollection.form_list(
                config["ipRangesRetainingParentCategory"] if "ipRangesRetainingParentCategory" in config else [], str
            )

            self.custom_category = config["customCategory"] if "customCategory" in config else False

            # Handle scopes with nested lists
            self.scopes = []
            if "scopes" in config:
                for scope in config["scopes"]:
                    scope_group = {
                        "scopeGroupMemberEntities": ZscalerCollection.form_list(
                            scope.get("scopeGroupMemberEntities", []), dict
                        ),
                        "Type": scope["Type"] if "Type" in scope else None,
                        "ScopeEntities": ZscalerCollection.form_list(scope.get("ScopeEntities", []), dict),
                    }
                    self.scopes.append(scope_group)

            self.editable = config["editable"] if "editable" in config else False
            self.description = config["description"] if "description" in config else None
            self.type = config["type"] if "type" in config else None

            # Handle nested dictionary for urlKeywordCounts
            # Handle nested dictionary for urlKeywordCounts
            self.url_keyword_counts = (
                {
                    "totalUrlCount": (
                        config["urlKeywordCounts"]["totalUrlCount"]
                        if "urlKeywordCounts" in config and "totalUrlCount" in config["urlKeywordCounts"]
                        else 0
                    ),
                    "retainParentUrlCount": (
                        config["urlKeywordCounts"]["retainParentUrlCount"]
                        if "urlKeywordCounts" in config and "retainParentUrlCount" in config["urlKeywordCounts"]
                        else 0
                    ),
                    "totalKeywordCount": (
                        config["urlKeywordCounts"]["totalKeywordCount"]
                        if "urlKeywordCounts" in config and "totalKeywordCount" in config["urlKeywordCounts"]
                        else 0
                    ),
                    "retainParentKeywordCount": (
                        config["urlKeywordCounts"]["retainParentKeywordCount"]
                        if "urlKeywordCounts" in config and "retainParentKeywordCount" in config["urlKeywordCounts"]
                        else 0
                    ),
                }
                if "urlKeywordCounts" in config
                else None
            )

            self.custom_urls_count = config["customUrlsCount"] if "customUrlsCount" in config else 0
            self.urls_retaining_parent_category_count = (
                config["urlsRetainingParentCategoryCount"] if "urlsRetainingParentCategoryCount" in config else 0
            )
            self.custom_ip_ranges_count = config["customIpRangesCount"] if "customIpRangesCount" in config else 0
            self.ip_ranges_retaining_parent_category_count = (
                config["ipRangesRetainingParentCategoryCount"] if "ipRangesRetainingParentCategoryCount" in config else 0
            )
        else:
            # Defaults when config is None
            self.id = None
            self.configured_name = None
            self.super_category = None
            self.keywords = []
            self.keywords_retaining_parent_category = []
            self.urls = []
            self.db_categorized_urls = []
            self.ip_ranges = []
            self.ip_ranges_retaining_parent_category = []
            self.custom_category = False
            self.scopes = []
            self.editable = False
            self.description = None
            self.type = None
            self.url_keyword_counts = None
            self.custom_urls_count = 0
            self.urls_retaining_parent_category_count = 0
            self.custom_ip_ranges_count = 0
            self.ip_ranges_retaining_parent_category_count = 0

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "configuredName": self.configured_name,
            "superCategory": self.super_category,
            "keywords": self.keywords,
            "keywordsRetainingParentCategory": self.keywords_retaining_parent_category,
            "urls": self.urls,
            "dbCategorizedUrls": self.db_categorized_urls,
            "ipRanges": self.ip_ranges,
            "ipRangesRetainingParentCategory": self.ip_ranges_retaining_parent_category,
            "customCategory": self.custom_category,
            "scopes": self.scopes,
            "editable": self.editable,
            "description": self.description,
            "type": self.type,
            "urlKeywordCounts": self.url_keyword_counts,
            "customUrlsCount": self.custom_urls_count,
            "urlsRetainingParentCategoryCount": self.urls_retaining_parent_category_count,
            "customIpRangesCount": self.custom_ip_ranges_count,
            "ipRangesRetainingParentCategoryCount": self.ip_ranges_retaining_parent_category_count,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class UrlDomainReview(ZscalerObject):
    """
    A class representing a URL Domain Review in Zscaler.
    """

    def __init__(self, config=None):
        super().__init__(config)

        if config:
            self.url = config["url"] if "url" in config else None
            self.domain_type = config["domainType"] if "domainType" in config else None

            # Handling matches list of objects
            self.matches = ZscalerCollection.form_list(config["matches"] if "matches" in config else [], dict)
        else:
            # Defaults when config is None
            self.url = None
            self.domain_type = None
            self.matches = []

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {"url": self.url, "domainType": self.domain_type, "matches": self.matches}
        parent_req_format.update(current_obj_format)
        return parent_req_format
