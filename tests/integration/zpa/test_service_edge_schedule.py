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
from pprint import pprint
from tests.integration.zpa.conftest import MockZPAClient


@pytest.fixture
def fs():
    yield


class TestServiceEdgeSchedule:
    """
    Integration Tests for the Service Edge Schedule
    """

    def test_service_edge_schedule(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors
        scheduler_id = None

        try:
            # Step 1: Get the existing Service Edge Schedule
            schedule = client.service_edges.get_service_edge_schedule()
            assert schedule is not None, "Failed to retrieve Service Edge Schedule"
            pprint(schedule)

            # Extract scheduler_id from the retrieved schedule
            scheduler_id = schedule.id

        except Exception as exc:
            errors.append(f"Error during get_service_edge_schedule: {exc}")

        try:
            # Step 2: Add a new Service Edge Schedule
            new_schedule = client.service_edges.add_service_edge_schedule(
                frequency="days",
                interval="5",
                disabled=False,
                enabled=True,
            )
            if new_schedule is not None:
                pprint(new_schedule)
            else:
                print("Schedule is already enabled.")

        except Exception as exc:
            if "resource.already.exist" not in str(exc):
                errors.append(f"Error during add_service_edge_schedule: {exc}")
            else:
                print("The schedule is already enabled, continuing with the test.")

        try:
            # Step 3: Update the Service Edge Schedule
            assert scheduler_id is not None, "Scheduler ID is None"
            updated_schedule = client.service_edges.update_service_edge_schedule(
                scheduler_id=scheduler_id,
                frequency="days",
                interval="7",
                disabled=True,
                enabled=False,
            )
            assert updated_schedule is not None, "Failed to update Service Edge Schedule"
            pprint(updated_schedule)

        except Exception as exc:
            errors.append(f"Error during update_service_edge_schedule: {exc}")

        assert not errors, f"Errors occurred: {errors}"
