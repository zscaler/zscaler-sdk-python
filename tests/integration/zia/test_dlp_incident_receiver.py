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


class TestDLPIncidentReceiver:
    """
    Integration Tests for the DLP Incident Receiver
    """

    def test_dlp_incident_receiver(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        try:
            # List all receivers
            receivers = client.dlp.list_dlp_incident_receiver()
            assert isinstance(receivers, list), "Expected a list of receivers"
            if receivers:  # If there are any receivers
                # Select the first receiver for further testing
                first_receiver = receivers[0]
                receiver_id = first_receiver.get("id")

                # Fetch the selected receiver by its ID
                try:
                    fetched_receiver = client.dlp.get_dlp_incident_receiver(receiver_id)
                    assert fetched_receiver is not None, "Expected a valid receiver object"
                    assert fetched_receiver.get("id") == receiver_id, "Mismatch in receiver ID"
                except Exception as exc:
                    errors.append(f"Fetching receiver by ID failed: {exc}")

                # Attempt to retrieve the receiver by name
                try:
                    receiver_name = first_receiver.get("name")  # Corrected this line
                    receiver_by_name = client.dlp.get_dlp_incident_receiver_by_name(receiver_name)
                    assert receiver_by_name is not None, "Expected a valid receiver object when searching by name"
                    assert receiver_by_name.get("id") == receiver_id, "Mismatch in receiver ID when searching by name"
                except Exception as exc:
                    errors.append(f"Fetching receiver by name failed: {exc}")

        except Exception as exc:
            errors.append(f"Listing receivers failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during receivers test: {errors}"
