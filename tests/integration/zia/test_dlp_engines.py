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

    @pytest.mark.asyncio
    async def test_dlp_engines(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        engine_name = "tests-" + generate_random_string()
        engine_description = "tests-" + generate_random_string()

        try:
            # Create a new dlp engine
            created_engine = client.dlp.add_dlp_engine(
                name=engine_name,
                description=engine_description,
                engine_expression="((D63.S > 1))",
                custom_dlp_engine=True,
            )
            assert created_engine is not None
            assert created_engine.name == engine_name
            assert created_engine.description == engine_description

            engine_id = created_engine.id
        except Exception as exc:
            errors.append(exc)

        try:
            # Retrieve the created dlp engine by ID
            retrieved_engine = client.dlp.get_dlp_engines(engine_id)
            assert retrieved_engine.id == engine_id
            assert retrieved_engine.name == engine_name
        except Exception as exc:
            errors.append(exc)

        try:
            # Update the dlp engine
            updated_name = engine_name + " Updated"
            client.dlp.update_dlp_engine(engine_id, name=updated_name)

            updated_engine = client.dlp.get_dlp_engines(engine_id)
            assert updated_engine.name == updated_name
        except Exception as exc:
            errors.append(exc)

        try:
            # List dlp engines and ensure the updated engine is in the list
            engines_list = client.dlp.list_dlp_engines()
            assert any(engine.id == engine_id for engine in engines_list)
        except Exception as exc:
            errors.append(exc)

        try:
            # Search for the dlp engine by name
            search_result = client.dlp.get_dlp_engine_by_name(
                updated_name
            )
            assert search_result is not None
            assert search_result.id == engine_id
        except Exception as exc:
            errors.append(exc)

        try:
            # Delete the dlp engine
            delete_response_code = client.dlp.delete_dlp_engine(engine_id)
            assert str(delete_response_code) == "204"
        except Exception as exc:
            errors.append(exc)

        # Assert that no errors occurred during the test
        assert (
            len(errors) == 0
        ), f"Errors occurred during the dlp engine lifecycle test: {errors}"
