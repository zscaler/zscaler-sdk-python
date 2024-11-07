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
from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestLSSConfigList:
    """
    Integration Tests for the LSS Config Lists
    """

    def test_get_client_types(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        client_types_to_validate = [
            "web_browser",
            "machine_tunnel",
            "zia_service_edge",
            "cloud_connector",
            "zia_inspection",
            "client_connector",
            "zpa_lss",
            "client_connector_partner",
            "branch_connector",
        ]

        try:
            # Test without specifying client_type to get all client types
            all_client_types = client.lss.get_client_types()
            assert len(all_client_types) > 0, "No client types returned"
            print("All Client Types:", all_client_types)

            # Test each specific client_type
            for client_type in client_types_to_validate:
                specific_client_type = client.lss.get_client_types(client_type)
                if specific_client_type:
                    print(f"Specific Client Type for {client_type}:", specific_client_type)
                else:
                    errors.append(f"Client type '{client_type}' not returned correctly")
        except Exception as exc:
            errors.append(f"Failed to get client types: {exc}")

        assert not errors, f"Errors occurred: {errors}"

    def test_get_log_formats(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        log_formats_to_validate = [
            "zpn_ast_comprehensive_stats",
            "zpn_auth_log_1id",
            "zpn_auth_log",
            "zpn_pbroker_comprehensive_stats",
            "zpn_ast_auth_log",
            "zpn_audit_log",
            "zpn_trans_log",
            "zpn_sys_auth_log",
            "zpn_waf_http_exchanges_log",
            "zpn_http_trans_log",
        ]
        try:
            # Test without specifying log_type to get all formats
            all_log_formats = client.lss.get_log_formats()
            assert len(all_log_formats) > 0, "No log formats returned"
            print("All Log Formats:", all_log_formats)

            # Test each specific log_type
            for log_type in log_formats_to_validate:
                specific_log_format = client.lss.get_log_formats(log_type)
                if specific_log_format:
                    print(f"Specific Log Format for {log_type}:", specific_log_format)
                else:
                    errors.append(f"Log format '{log_type}' not returned correctly or is missing")
        except Exception as exc:
            errors.append(f"Failed to get log formats: {exc}")

        assert not errors, f"Errors occurred: {errors}"

    # def test_get_status_codes(self, fs):
    #     client = MockZPAClient(fs)
    #     errors = []  # Initialize an empty list to collect errors

    #     # Define the set of expected status codes for validation
    #     expected_status_codes = {"zpn_auth_log", "zpn_ast_auth_log", "zpn_trans_log", "zpn_sys_auth_log"}

    #     try:
    #         # Test with default log_type 'all'
    #         all_status_codes = client.lss.get_status_codes()
    #         if not all_status_codes:
    #             errors.append("No status codes returned for default log_type 'all'")
    #         elif not expected_status_codes.issubset(set(all_status_codes.keys())):
    #             errors.append("Unexpected status codes returned for default log_type 'all'")
    #         print("Status Codes for 'all':", all_status_codes)
    #     except Exception as exc:
    #         errors.append(f"Failed to get status codes: {exc}")

    #     assert not errors, f"Errors occurred during the test: {'; '.join(errors)}"
