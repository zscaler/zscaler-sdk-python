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
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestDLPDictionary:
    """
    Integration Tests for the DLP dictionary
    """

    def test_dlp_dictionary(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        dict_id = None  # Placeholder for the dictionary ID
        custom_phrase_match_type = "MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY"
        dictionary_type = "PATTERNS_AND_PHRASES"
        phrases = ([{"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test"}],)
        patterns = [{"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test"}]

        # Attempt to add a DLP dictionary
        try:
            dlp_dict = client.dlp.add_dict(
                name="tests-" + generate_random_string(),
                description="updated-" + generate_random_string(),
                custom_phrase_match_type=custom_phrase_match_type,
                dictionary_type=dictionary_type,
                phrases=[{"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test"}],
                patterns=[{"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test"}],
            )
            dict_id = dlp_dict.get("id")
            assert dict_id is not None, "Failed to create DLP Dictionary"
        except Exception as exc:
            errors.append(f"Adding DLP Dictionary failed: {exc}")

        # Attempt to update the DLP dictionary
        if dict_id:
            try:
                updated_name = "updated-" + generate_random_string()
                updated_dict = client.dlp.update_dict(
                    dict_id=dict_id,
                    name=updated_name,
                    description=updated_name,
                    custom_phrase_match_type=custom_phrase_match_type,
                    dictionary_type=dictionary_type,
                    phrases=[{"action": "PHRASE_COUNT_TYPE_ALL", "phrase": "test"}],
                    patterns=[{"action": "PATTERN_COUNT_TYPE_ALL", "pattern": "test"}],
                )
                assert updated_dict.get("name") == updated_name, "Failed to update DLP Dictionary"
            except Exception as exc:
                errors.append(f"Updating DLP Dictionary failed: {exc}")

        # Attempt to list DLP dictionaries
        try:
            dicts = client.dlp.list_dicts()
            assert isinstance(dicts, list), "Failed to list DLP Dictionaries"
        except Exception as exc:
            errors.append(f"Listing DLP Dictionaries failed: {exc}")

        # Attempt to get the specific DLP dictionary
        if dict_id:
            try:
                specific_dict = client.dlp.get_dict(dict_id)
                assert specific_dict.get("id") == dict_id, "Failed to retrieve specific DLP Dictionary"
            except Exception as exc:
                errors.append(f"Retrieving specific DLP Dictionary failed: {exc}")

        # Attempt to delete the DLP dictionary
        if dict_id:
            try:
                delete_response = client.dlp.delete_dict(dict_id)
                assert delete_response == 204, "Failed to delete DLP Dictionary"
            except Exception as exc:
                errors.append(f"Deleting DLP Dictionary failed: {exc}")

        # Assert no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during DLP dictionary operations test: {errors}"
