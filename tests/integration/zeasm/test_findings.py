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


class TestFindings:
    """
    Integration Tests for the ZEASM findings
    """

    def _get_org_id(self, client):
        """Helper to get the first organization ID."""
        orgs, _, err = client.zeasm.organizations.list_organizations()
        if err:
            raise Exception(f"Error listing organizations: {err}")
        if not orgs or not orgs.results:
            raise Exception("No organizations found")
        return orgs.results[0].id

    @pytest.mark.vcr()
    def test_list_findings(self, fs, zeasm_client):
        client = zeasm_client
        errors = []

        try:
            org_id = self._get_org_id(client)
            print(f"Using org_id: {org_id}")

            findings, _, err = client.zeasm.findings.list_findings(org_id=org_id)

            if err:
                errors.append(f"Error listing findings: {err}")
            elif findings:
                print(f"Total findings found: {findings.total_results}")
                pprint(findings.as_dict())
            else:
                print("No findings found")
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    @pytest.mark.vcr()
    def test_get_finding_details(self, fs, zeasm_client):
        client = zeasm_client
        errors = []

        try:
            org_id = self._get_org_id(client)
            print(f"Using org_id: {org_id}")

            # First get the list of findings to get a finding_id
            findings, _, err = client.zeasm.findings.list_findings(org_id=org_id)

            if err:
                errors.append(f"Error listing findings: {err}")
                return

            if not findings or not findings.results:
                print("No findings found to get details for")
                return

            finding_id = findings.results[0].id
            print(f"Using finding_id: {finding_id}")

            finding_details, _, err = client.zeasm.findings.get_finding_details(
                org_id=org_id,
                finding_id=finding_id
            )

            if err:
                errors.append(f"Error getting finding details: {err}")
            elif finding_details:
                print("Finding details retrieved successfully:")
                pprint(finding_details.as_dict())
            else:
                print("No finding details found")
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    @pytest.mark.vcr()
    def test_get_finding_evidence(self, fs, zeasm_client):
        client = zeasm_client
        errors = []

        try:
            org_id = self._get_org_id(client)
            print(f"Using org_id: {org_id}")

            # First get the list of findings to get a finding_id
            findings, _, err = client.zeasm.findings.list_findings(org_id=org_id)

            if err:
                errors.append(f"Error listing findings: {err}")
                return

            if not findings or not findings.results:
                print("No findings found to get evidence for")
                return

            finding_id = findings.results[0].id
            print(f"Using finding_id: {finding_id}")

            evidence, _, err = client.zeasm.findings.get_finding_evidence(
                org_id=org_id,
                finding_id=finding_id
            )

            if err:
                errors.append(f"Error getting finding evidence: {err}")
            elif evidence:
                print("Finding evidence retrieved successfully:")
                pprint(evidence.as_dict())
            else:
                print("No finding evidence found")
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))

    @pytest.mark.vcr()
    def test_get_finding_scan_output(self, fs, zeasm_client):
        client = zeasm_client
        errors = []

        try:
            org_id = self._get_org_id(client)
            print(f"Using org_id: {org_id}")

            # First get the list of findings to get a finding_id
            findings, _, err = client.zeasm.findings.list_findings(org_id=org_id)

            if err:
                errors.append(f"Error listing findings: {err}")
                return

            if not findings or not findings.results:
                print("No findings found to get scan output for")
                return

            finding_id = findings.results[0].id
            print(f"Using finding_id: {finding_id}")

            scan_output, _, err = client.zeasm.findings.get_finding_scan_output(
                org_id=org_id,
                finding_id=finding_id
            )

            if err:
                errors.append(f"Error getting finding scan output: {err}")
            elif scan_output:
                print("Finding scan output retrieved successfully:")
                pprint(scan_output.as_dict())
            else:
                print("No finding scan output found")
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
