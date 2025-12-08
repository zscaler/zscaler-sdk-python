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
from pprint import pprint
from tests.integration.zeasm.conftest import MockZEASMClient


@pytest.fixture
def fs():
    yield


class TestOrganizations:
    """
    Integration Tests for the ZEASM organizations
    """

    @pytest.mark.vcr()
    def test_list_organizations(self, fs, zeasm_client):
        client = zeasm_client
        errors = []

        try:
            orgs = client.zeasm.organizations.list_organizations()
            if orgs:
                print(f"Total organizations found: {orgs.total_results}")
                pprint(orgs.as_dict())
                for org in orgs.results:
                    pprint(org.as_dict())
            else:
                print("No organizations found")
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
