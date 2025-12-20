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
import time

from tests.integration.zia.conftest import MockZIAClient


@pytest.fixture
def fs():
    yield


class TestAuditLogs:
    """
    Integration Tests for the Audit Logs API.
    """

    @pytest.mark.vcr()
    def test_audit_logs_operations(self, fs):
        client = MockZIAClient(fs)
        errors = []

        # Use epoch timestamps for the last 24 hours
        current_time_ms = int(time.time() * 1000)
        one_day_ago_ms = current_time_ms - (24 * 60 * 60 * 1000)

        # Step 1: Get audit log report status
        try:
            status = client.zia.audit_logs.get_status()
            # Status can be None if no report is pending
        except Exception as exc:
            errors.append(f"Failed to get audit log status: {exc}")

        # Step 2: Create an audit log report request
        try:
            result = client.zia.audit_logs.create(
                start_time=str(one_day_ago_ms),
                end_time=str(current_time_ms)
            )
            # Result can be None or status code
        except Exception as exc:
            errors.append(f"Failed to create audit log report: {exc}")

        # Step 3: Get status again after creating report
        try:
            status_after_create = client.zia.audit_logs.get_status()
            # Status should show pending or complete
        except Exception as exc:
            errors.append(f"Failed to get audit log status after create: {exc}")

        # Step 4: Get the audit log report
        try:
            report = client.zia.audit_logs.get_report()
            # Report can be None if not ready yet
        except Exception as exc:
            errors.append(f"Failed to get audit log report: {exc}")

        # Step 5: Cancel the audit log report request
        try:
            cancel_result = client.zia.audit_logs.cancel()
            # Cancel result should be status code
        except Exception as exc:
            errors.append(f"Failed to cancel audit log report: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")

