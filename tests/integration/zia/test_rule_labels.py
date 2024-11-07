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


class TestRuleLabels:
    """
    Integration Tests for the Rule Label
    """

    def test_rule_labels(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        label_name = "tests-" + generate_random_string()
        label_description = "tests-" + generate_random_string()
        label_id = None

        try:
            # Attempt to create a new rule label
            try:
                created_label = client.labels.add_label(
                    name=label_name,
                    description=label_description,
                )
                assert created_label is not None, "Label creation returned None"
                assert created_label.name == label_name, "Label name mismatch"
                assert created_label.description == label_description, "Label description mismatch"
                label_id = created_label.id
            except Exception as exc:
                errors.append(f"Failed to add label: {exc}")

            # Attempt to retrieve the created rule label by ID
            if label_id:
                try:
                    retrieved_label = client.labels.get_label(label_id)
                    assert retrieved_label.id == label_id, "Retrieved label ID mismatch"
                    assert retrieved_label.name == label_name, "Retrieved label name mismatch"
                except Exception as exc:
                    errors.append(f"Failed to retrieve label: {exc}")

            # Attempt to update the rule label
            if label_id:
                try:
                    updated_name = label_name + " Updated"
                    client.labels.update_label(label_id, name=updated_name)
                    updated_label = client.labels.get_label(label_id)
                    assert updated_label.name == updated_name, "Failed to update label name"
                except Exception as exc:
                    errors.append(f"Failed to update label: {exc}")

            # Attempt to list rule labels and check if the updated label is in the list
            try:
                labels_list = client.labels.list_labels()
                assert any(label.id == label_id for label in labels_list), "Updated label not found in list"
            except Exception as exc:
                errors.append(f"Failed to list labels: {exc}")

        finally:
            # Cleanup: Attempt to delete the rule label
            if label_id:
                try:
                    delete_response_code = client.labels.delete_label(label_id)
                    assert str(delete_response_code) == "204", "Failed to delete label"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the rule label lifecycle test: {errors}"
