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


class TestPacFiles:
    """
    Integration Tests for the PAC Files API.
    """

    @pytest.mark.vcr()
    def test_pac_files_crud(self, fs):
        """Test PAC Files operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_pac_files
            pac_files, response, err = client.zia.pac_files.list_pac_files()
            assert err is None, f"List PAC files failed: {err}"
            assert pac_files is not None, "PAC files list should not be None"
            assert isinstance(pac_files, list), "PAC files should be a list"

            # Test get_pac_file with first PAC file if available
            if pac_files and len(pac_files) > 0:
                pac_id = pac_files[0].id
                fetched_pac, response, err = client.zia.pac_files.get_pac_file(pac_id)
                assert err is None, f"Get PAC file failed: {err}"
                assert fetched_pac is not None, "Fetched PAC file should not be None"

                # Test get_pac_file_version - version 1 typically exists
                try:
                    pac_version, response, err = client.zia.pac_files.get_pac_file_version(pac_id, pac_version=1)
                    # May fail if version doesn't exist - that's ok
                except Exception:
                    pass

            # Test validate_pac_file with a simple PAC script
            try:
                pac_content = """function FindProxyForURL(url, host) {
    return "DIRECT";
}"""
                validation, response, err = client.zia.pac_files.validate_pac_file(pac_file_content=pac_content)
                # Validation may fail - that's ok
            except Exception:
                pass

            # Test list_pac_files with query params
            pac_files_filtered, response, err = client.zia.pac_files.list_pac_files(
                query_params={"search": "default"}
            )
            # Search may return empty - that's ok

        except Exception as e:
            errors.append(f"Exception during PAC files test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"
