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


class TestRuleLabels:
    """
    Integration Tests for the Rule Label.

    These tests use VCR to record and replay HTTP interactions.
    - First run with MOCK_TESTS=false records cassettes
    - Subsequent runs use recorded cassettes (no API calls)
    """

    @pytest.mark.vcr()
    def test_rule_labels_lifecycle(self, fs):
        """Test complete rule label CRUD lifecycle."""
        client = MockZIAClient(fs)
        errors = []
        label_id = None
        update_label = None

        try:
            # Test: Add Rule Label (deterministic name for VCR)
            try:
                create_label = client.zia.rule_labels.add_label(
                    name="TestLabel_VCR_Integration", description="Test Description for VCR"
                )
                assert create_label is not None, "Label creation failed."
                label_id = create_label.id
            except Exception as e:
                errors.append(f"Exception during add_label: {str(e)}")

            # Test: Update Rule Label
            try:
                if label_id:
                    update_label = client.zia.rule_labels.update_label(
                        label_id=label_id,
                        name="UpdatedLabel_VCR_Integration",
                        description="Updated Description for VCR",
                    )
                    assert update_label is not None, "Label update returned None."
            except Exception as e:
                errors.append(f"Exception during update_label: {str(e)}")

            # Test: Get Rule Label
            try:
                if update_label:
                    label = client.zia.rule_labels.get_label(update_label.id)
                    assert label.id == label_id, "Retrieved label ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_label: {str(e)}")

            # Test: List Rule Labels
            try:
                if update_label:
                    labels = client.zia.rule_labels.list_labels(query_params={"search": update_label.name})
                    assert labels is not None and isinstance(labels, list), "No labels found or invalid format."
            except Exception as e:
                errors.append(f"Exception during list_labels: {str(e)}")

        finally:
            # Ensure label cleanup
            try:
                if update_label:
                    _ = client.zia.rule_labels.delete_label(update_label.id)
            except Exception as e:
                errors.append(f"Exception during delete_label: {str(e)}")

        # Final Assertion
        if errors:
            pytest.fail(f"Test failed with errors: {errors}")

    @pytest.mark.vcr()
    def test_list_rule_labels(self, fs):
        """Test listing rule labels."""
        client = MockZIAClient(fs)

        labels = client.zia.rule_labels.list_labels()
        assert labels is not None, "Labels list is None"
        assert isinstance(labels, list), "Labels is not a list"
