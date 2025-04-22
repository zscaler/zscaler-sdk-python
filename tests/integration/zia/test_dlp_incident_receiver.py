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


@pytest.fixture
def fs():
    yield


class TestDLPIncidentReceiver:
    """
    Integration Tests for the DLP Incident Receiver
    """

    def test_dlp_incident_receiver(self, fs):
        client = MockZIAClient(fs)
        errors = []

        try:
            receivers, _, error = client.zia.dlp_resources.list_dlp_incident_receiver()
            assert error is None, f"List Incident Receivers Error: {error}"
            assert isinstance(receivers, list), "Expected a list of receivers"

            if receivers:
                first_receiver = receivers[0]
                receiver_id = first_receiver.id

                try:
                    fetched_receiver, _, error = client.zia.dlp_resources.get_dlp_incident_receiver(receiver_id)
                    assert error is None, f"Get Incident Receiver Error: {error}"
                    assert fetched_receiver is not None
                    assert fetched_receiver.id == receiver_id, "Mismatch in receiver ID"
                except Exception as exc:
                    errors.append(f"Fetching receiver by ID failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing receivers failed: {exc}")

        # Final assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
