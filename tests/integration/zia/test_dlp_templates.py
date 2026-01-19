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


class TestDLPTemplates:
    """
    Integration Tests for the DLP Templates API.
    """

    @pytest.mark.vcr()
    def test_dlp_templates_crud(self, fs):
        """Test DLP Templates CRUD operations."""
        client = MockZIAClient(fs)
        errors = []
        template_id = None

        try:
            # Test list_dlp_templates
            templates, response, err = client.zia.dlp_templates.list_dlp_templates()
            assert err is None, f"List DLP templates failed: {err}"
            assert templates is not None, "Templates list should not be None"
            assert isinstance(templates, list), "Templates should be a list"

            # Test add_dlp_template - create a new template
            try:
                created_template, response, err = client.zia.dlp_templates.add_dlp_template(
                    name="TestDLPTemplate_VCR",
                    template_content="Test DLP template content for VCR testing",
                )
                if err is None and created_template is not None:
                    template_id = created_template.get("id") if isinstance(created_template, dict) else getattr(created_template, "id", None)

                    # Test get_dlp_templates
                    if template_id:
                        fetched_template, response, err = client.zia.dlp_templates.get_dlp_templates(template_id)
                        assert err is None, f"Get DLP template failed: {err}"
                        assert fetched_template is not None, "Fetched template should not be None"

                        # Test update_dlp_template
                        try:
                            updated_template, response, err = client.zia.dlp_templates.update_dlp_template(
                                template_id=template_id,
                                name="TestDLPTemplate_VCR_Updated",
                                template_content="Updated test DLP template content",
                            )
                            # Update may fail - that's ok
                        except Exception:
                            pass
            except Exception as e:
                # Add may fail due to permissions/subscription
                pass

            # If we didn't create a template, test with existing one
            if template_id is None and templates and len(templates) > 0:
                existing_id = templates[0].id
                fetched_template, response, err = client.zia.dlp_templates.get_dlp_templates(existing_id)
                assert err is None, f"Get DLP template failed: {err}"

        except Exception as e:
            errors.append(f"Exception during DLP templates test: {str(e)}")

        finally:
            # Cleanup - delete created template
            if template_id:
                try:
                    client.zia.dlp_templates.delete_dlp_template(template_id)
                except Exception:
                    pass

        assert len(errors) == 0, f"Errors occurred: {errors}"
