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


class TestDLPEngines:
    """
    Integration Tests for the DLP Engines
    """

    def test_dlp_engines(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        engine_name = "tests-" + generate_random_string()
        engine_description = "tests-" + generate_random_string()
        engine_id = None

        try:
            # Attempt to create a new dlp engine
            try:
                created_engine = client.dlp.add_dlp_engine(
                    name=engine_name,
                    description=engine_description,
                    engine_expression="((D63.S > 1))",
                    custom_dlp_engine=True,
                )
                assert created_engine is not None, "DLP engine creation returned None"
                assert created_engine.name == engine_name, "DLP engine name mismatch"
                assert created_engine.description == engine_description, "DLP engine description mismatch"
                engine_id = created_engine.id
            except Exception as exc:
                errors.append(f"Failed to add DLP engine: {exc}")

            # Attempt to retrieve the created dlp engine by ID
            if engine_id:
                try:
                    retrieved_engine = client.dlp.get_dlp_engines(engine_id)
                    assert retrieved_engine.id == engine_id, "Retrieved DLP engine ID mismatch"
                    assert retrieved_engine.name == engine_name, "Retrieved DLP engine name mismatch"
                except Exception as exc:
                    errors.append(f"Failed to retrieve DLP engine: {exc}")

            # Attempt to update the dlp engine
            if engine_id:
                try:
                    updated_name = engine_name + " Updated"
                    client.dlp.update_dlp_engine(engine_id, name=updated_name)
                    updated_engine = client.dlp.get_dlp_engines(engine_id)
                    assert updated_engine.name == updated_name, "Failed to update DLP engine name"
                except Exception as exc:
                    errors.append(f"Failed to update DLP engine: {exc}")

            # Attempt to list dlp engines and check if the updated engine is in the list
            try:
                engines_list = client.dlp.list_dlp_engines()
                assert any(engine.id == engine_id for engine in engines_list), "Updated DLP engine not found in list"
            except Exception as exc:
                errors.append(f"Failed to list DLP engines: {exc}")

            # Attempt to search for the dlp engine by name
            if engine_id:
                try:
                    search_result = client.dlp.get_dlp_engine_by_name(updated_name)
                    assert search_result is not None, "Search returned None"
                    assert search_result.id == engine_id, "Search result ID mismatch"
                except Exception as exc:
                    errors.append(f"Failed to search DLP engine by name: {exc}")

        finally:
            # Cleanup: Attempt to delete the dlp engine
            if engine_id:
                try:
                    delete_response_code = client.dlp.delete_dlp_engine(engine_id)
                    assert str(delete_response_code) == "204", "Failed to delete DLP engine"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the DLP engine lifecycle test: {errors}"
