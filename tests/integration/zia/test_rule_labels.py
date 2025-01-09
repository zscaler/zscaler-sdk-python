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
        errors = []
        label_id = None

        try:
            # Test: Add Rule Label
            try:
                label_data = {"name": "Test Label", "description": "Test Description"}
                label, response, error = client.zia.rule_labels.add_label(**label_data)
                assert error is None, f"Add Label Error: {error}"
                assert label is not None, "Label creation failed."
                label_id = label.id
            except Exception as e:
                errors.append(f"Exception during add_label: {str(e)}")

            # Test: Get Rule Label
            try:
                if label_id:
                    label, response, error = client.zia.rule_labels.get_label(label_id)
                    assert error is None, f"Get Label Error: {error}"
                    assert label.id == label_id, "Retrieved label ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_label: {str(e)}")

            # Test: Update Rule Label
            try:
                if label_id:
                    updated_data = {"description": "Updated Description"}
                    label, response, error = client.zia.rule_labels.update_label(label_id, **updated_data)
                    assert error is None, f"Update Label Error: {error}"
                    assert label.description == "Updated Description", "Label update failed."
            except Exception as e:
                errors.append(f"Exception during update_label: {str(e)}")

            # Test: List Rule Labels
            try:
                labels, response, error = client.zia.rule_labels.list_labels()
                assert error is None, f"List Labels Error: {error}"
                assert labels is not None and isinstance(labels, list), "No labels found."
            except Exception as e:
                errors.append(f"Exception during list_labels: {str(e)}")

        finally:
            # Ensure label cleanup
            try:
                if label_id:
                    _, response, error = client.zia.rule_labels.delete_label(label_id)
                    assert error is None, f"Delete Label Error: {error}"
            except Exception as e:
                errors.append(f"Exception during delete_label: {str(e)}")

        # Final Assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
