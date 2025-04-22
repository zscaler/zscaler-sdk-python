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
from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestAppProtectionControls:
    """
    Integration Tests for the App Protection Controls
    """

    def test_list_control_action_types(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        try:
            action_types = client.zpa.app_protection.list_control_action_types()
            assert len(action_types) > 0, "No action types returned"
            print("Action Types:", action_types)
        except Exception as exc:
            errors.append(f"Failed to list control action types: {exc}")

        assert not errors, f"Errors occurred: {errors}"

    def test_list_control_severity_types(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        try:
            severity_types = client.zpa.app_protection.list_control_severity_types()
            assert len(severity_types) > 0, "No severity types returned"
            print("Severity Types:", severity_types)
        except Exception as exc:
            errors.append(f"Failed to list control severity types: {exc}")

        assert not errors, f"Errors occurred: {errors}"

    def test_list_control_types(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        try:
            control_types = client.zpa.app_protection.list_control_types()
            assert len(control_types) > 0, "No control types returned"
            print("Control Types:", control_types)
        except Exception as exc:
            errors.append(f"Failed to list control types: {exc}")

        assert not errors, f"Errors occurred: {errors}"

    def test_list_custom_http_methods(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        try:
            http_methods = client.zpa.app_protection.list_custom_http_methods()
            assert len(http_methods) > 0, "No HTTP methods returned"
            print("HTTP Methods:", http_methods)
        except Exception as exc:
            errors.append(f"Failed to list HTTP methods: {exc}")

        assert not errors, f"Errors occurred: {errors}"

    def test_list_predef_control_versions(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        try:
            versions = client.zpa.app_protection.list_predef_control_versions()
            assert len(versions) > 0, "No versions returned"
            print("Versions:", versions)
        except Exception as exc:
            errors.append(f"Failed to list versions: {exc}")

        assert not errors, f"Errors occurred: {errors}"

    def test_list_predef_controls(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        # version = "OWASP_CRS/3.3.0"  # Example version for the test

        try:
            # Fetch predefined controls without search term
            predef_controls = client.zpa.app_protection.list_predef_controls()
            assert len(predef_controls) > 0, "No predefined controls returned for version"
            print("Predefined Controls for Version:", predef_controls)

            # Fetch predefined controls with search term
            predef_controls_with_search = client.zpa.app_protection.list_predef_controls()
            assert len(predef_controls_with_search) > 0, "No predefined controls returned for search"
            print("Predefined Controls for Search Term:", predef_controls_with_search)

        except Exception as exc:
            errors.append(f"Failed to list predefined controls: {exc}")

        # Assert that no errors occurred during the test
        assert not errors, f"Errors occurred: {errors}"
