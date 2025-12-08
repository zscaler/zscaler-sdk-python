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


class TestDLPEngines:
    """
    Integration Tests for the DLP Engines
    """

    @pytest.mark.vcr()
    def test_dlp_engines(self, fs):
        client = MockZIAClient(fs)
        errors = []

        engine_id = None
        created_engine = None
        updated_engine = None
        updated_name = None

        engine_name = f"tests-{generate_random_string()}"
        engine_description = f"tests-{generate_random_string()}"

        try:
            # Step 1: Create DLP engine
            try:
                created_engine = client.zia.dlp_engine.add_dlp_engine(
                    name=engine_name,
                    description=engine_description,
                    engine_expression="((D63.S > 1))",
                    custom_dlp_engine=True,
                )
                assert created_engine is not None, "DLP engine creation failed."
                assert created_engine.name == engine_name
                assert created_engine.description == engine_description
                engine_id = created_engine.id
            except Exception as e:
                errors.append(f"Exception during add_dlp_engine: {str(e)}")

            # Step 2: Retrieve the DLP engine
            try:
                if engine_id:
                    retrieved_engine = client.zia.dlp_engine.get_dlp_engines(engine_id)
                    assert retrieved_engine is not None
                    assert retrieved_engine.id == engine_id
                    assert retrieved_engine.name == engine_name
            except Exception as e:
                errors.append(f"Exception during get_dlp_engine: {str(e)}")

            # Step 3: Update the DLP engine
            try:
                if engine_id:
                    updated_name = f"{engine_name}_Updated"
                    updated_engine = client.zia.dlp_engine.update_dlp_engine(
                        engine_id=engine_id,
                        name=updated_name,
                        description=engine_description,
                        engine_expression="((D63.S > 1))",
                        custom_dlp_engine=True,
                    )
                    assert updated_engine.name == updated_name, "Updated name mismatch."
            except Exception as e:
                errors.append(f"Exception during update_dlp_engine: {str(e)}")

            # Step 4: List DLP engines
            try:
                engines_list = client.zia.dlp_engine.list_dlp_engines()
                assert any(engine.id == engine_id for engine in engines_list), "Engine not found in list."
            except Exception as e:
                errors.append(f"Exception during list_dlp_engines: {str(e)}")

        finally:
            # Step 6: Cleanup
            try:
                if engine_id:
                    _ = client.zia.dlp_engine.delete_dlp_engine(updated_engine.id)
            except Exception as e:
                errors.append(f"Exception during delete_dlp_engine: {str(e)}")

        # Final Assertion
        if errors:
            pytest.fail(f"Test failed with errors: {errors}")
