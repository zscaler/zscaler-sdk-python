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


class TestLookALikeDomains:
    """
    Integration Tests for the ZEASM lookalike domains
    """

    def _get_org_id(self, client):
        """Helper to get the first organization ID."""
        orgs = client.zeasm.organizations.list_organizations()
        if not orgs or not orgs.results:
            raise Exception("No organizations found")
        return orgs.results[0].id

    @pytest.mark.vcr()
    def test_list_lookalike_domains(self, fs, zeasm_client):
        client = zeasm_client
        errors = []

        try:
            org_id = self._get_org_id(client)
            print(f"Using org_id: {org_id}")

            domains = client.zeasm.lookalike_domains.list_lookalike_domains(
                org_id=org_id
            )
            if domains:
                print(f"Total lookalike domains found: {domains.total_results}")
                pprint(domains.as_dict())
            else:
                print("No lookalike domains found")
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    @pytest.mark.vcr()
    def test_get_lookalike_domain(self, fs, zeasm_client):
        client = zeasm_client
        errors = []

        try:
            org_id = self._get_org_id(client)
            print(f"Using org_id: {org_id}")

            # First get the list of lookalike domains to get a lookalike_raw
            domains = client.zeasm.lookalike_domains.list_lookalike_domains(
                org_id=org_id
            )

            if not domains or not domains.results:
                print("No lookalike domains found to get details for")
                return

            lookalike_raw = domains.results[0].lookalike_raw
            print(f"Using lookalike_raw: {lookalike_raw}")

            domain_details = client.zeasm.lookalike_domains.get_lookalike_domain(
                org_id=org_id,
                lookalike_raw=lookalike_raw
            )
            if domain_details:
                print("Lookalike domain details retrieved successfully:")
                pprint(domain_details.as_dict())
            else:
                print("No lookalike domain details found")
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
