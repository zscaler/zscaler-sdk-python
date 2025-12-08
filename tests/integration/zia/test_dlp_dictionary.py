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

from tests.integration.zia.conftest import MockZIAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestDLPDictionary:
    """
    Integration Tests for the DLP dictionary
    """

    @pytest.mark.vcr()
    def test_dlp_dictionary(self, fs):
        client = MockZIAClient(fs)
        errors = []
        dict_id = None

        dict_name = f"tests-{generate_random_string()}"
        dict_description = f"tests-{generate_random_string()}"

        try:
            phrases = [("PHRASE_COUNT_TYPE_ALL", "YourPhrase")]
            patterns = [("PATTERN_COUNT_TYPE_UNIQUE", "YourPattern")]

            dlp_dict = client.zia.dlp_dictionary.add_dict(
                name=dict_name,
                description=dict_description,
                custom_phrase_match_type="MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY",
                dictionary_type="PATTERNS_AND_PHRASES",
                phrases=phrases,
                patterns=patterns,
            )
            assert dlp_dict is not None, "DLP Dictionary creation failed."
            assert dlp_dict.name == dict_name
            assert dlp_dict.description == dict_description
            dict_id = dlp_dict.id
        except Exception as e:
            errors.append(f"Exception during add_dlp_engine: {str(e)}")

        try:
            if dict_id:
                updated_name = "updated-" + generate_random_string()
                updated_dict = client.zia.dlp_dictionary.update_dict(
                    dict_id=dict_id,
                    name=updated_name,
                    description=updated_name,
                    custom_phrase_match_type="MATCH_ALL_CUSTOM_PHRASE_PATTERN_DICTIONARY",
                    dictionary_type="PATTERNS_AND_PHRASES",
                    phrases=[("PHRASE_COUNT_TYPE_ALL", "YourUpdatedPhrase")],
                    patterns=[("PATTERN_COUNT_TYPE_UNIQUE", "YourUpdatedPattern")],
                )
                assert updated_dict.name == updated_name
        except Exception as e:
            errors.append(f"Updating DLP Dictionary failed: {str(e)}")

        try:
            dict_list = client.zia.dlp_dictionary.list_dicts()
            assert any(dictionary.id == dict_id for dictionary in dict_list), "Dictionary not found in list."
        except Exception as e:
            errors.append(f"Exception during list_dicts: {str(e)}")

        try:
            if dict_id:
                retrieved_dict = client.zia.dlp_dictionary.get_dict(dict_id)
                assert retrieved_dict is not None
                assert retrieved_dict.id == dict_id
        except Exception as e:
            errors.append(f"Exception during get_dict: {str(e)}")

        try:
            if dict_id:
                _ = client.zia.dlp_dictionary.delete_dict(dict_id)
        except Exception as e:
            errors.append(f"Deleting DLP Dictionary failed: {str(e)}")

        if errors:
            pytest.fail(f"Test failed with errors: {errors}")
