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

from tests.integration.zia.conftest import MockZIAClient, TestNameGenerator


@pytest.fixture
def fs():
    yield


class TestBandwidthClasses:
    """
    Integration Tests for the Bandwidth Classes
    """

    @pytest.mark.vcr()
    def test_bandwidth_class(self, fs):
        client = MockZIAClient(fs)
        errors = []
        class_id = None
        update_class = None
        
        # Use deterministic names for VCR
        names = TestNameGenerator("bandwidth-class")

        try:
            # Test: Add Bandwidth Class
            try:
                create_class, _, error = client.zia.bandwidth_classes.add_class(
                    name=names.name,
                    web_applications=["ACADEMICGPT", "AD_CREATIVES"],
                    urls=["test1.acme.com", "test2.acme.com"],
                    url_categories=["AI_ML_APPS", "GENERAL_AI_ML"],
                )
                assert error is None, f"Add Class Error: {error}"
                assert create_class is not None, "Class creation failed."
                class_id = create_class.id
            except Exception as e:
                errors.append(f"Exception during add_class: {str(e)}")

            # Test: Update Bandwidth Class
            try:
                if class_id:
                    update_class, _, error = client.zia.bandwidth_classes.update_class(
                        class_id=class_id,
                        name=names.updated_name,
                        web_applications=["ACADEMICGPT", "AD_CREATIVES"],
                        urls=["test1.acme.com", "test2.acme.com", "test3.acme.com"],
                        url_categories=["AI_ML_APPS", "GENERAL_AI_ML", "PROFESSIONAL_SERVICES"],
                    )
                    assert error is None, f"Update class Error: {error}"
                    assert update_class is not None, "class update returned None."
            except Exception as e:
                errors.append(f"Exception during update_class: {str(e)}")

            # Test: Get Bandwidth Class
            try:
                if update_class:
                    bdw_class, _, error = client.zia.bandwidth_classes.get_class(update_class.id)
                    assert error is None, f"Get class Error: {error}"
                    assert bdw_class.id == class_id, "Retrieved class ID mismatch."
            except Exception as e:
                errors.append(f"Exception during get_class: {str(e)}")

            # Test: List Bandwidth Classes
            try:
                if update_class:
                    classes, _, error = client.zia.bandwidth_classes.list_classes(query_params={"search": update_class.name})
                    assert error is None, f"List Classes Error: {error}"
                    assert classes is not None and isinstance(classes, list), "No Classes found or invalid format."
            except Exception as e:
                errors.append(f"Exception during list_classes: {str(e)}")

        finally:
            # Ensure class cleanup
            try:
                if update_class:
                    _, _, error = client.zia.bandwidth_classes.delete_class(update_class.id)
                    assert error is None, f"Delete Class Error: {error}"
            except Exception as e:
                errors.append(f"Exception during delete_class: {str(e)}")

        # Final Assertion
        if errors:
            raise AssertionError(f"Integration Test Errors:\n{chr(10).join(errors)}")
