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
from box import Box

@pytest.fixture
def fs():
    yield
 
class TestPacFiles:
    """
    Integration Tests for the pac file
    """

    def test_pac_files(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        pac_file_name = "tests-" + generate_random_string()
        pac_file_description = "tests-" + generate_random_string()
        pac_id = None
        pac_version = None

        try:
            # Test validate_pac_file
            try:
                validate_pac_file = client.pac_files.validate_pac_file(
                    pac_file_content="""
                    function FindProxyForURL(url, host) {
                        var privateIP = /^(0|10|127|192\\.168|172\\.1[6789]|172\\.2[0-9]|172\\.3[01]|169\\.254|192\\.88\\.99)\\.[0-9.]+$/;
                        var resolved_ip = dnsResolve(host);

                        if (isPlainHostName(host) || isInNet(resolved_ip, "192.0.2.0", "255.255.255.0") || privateIP.test(resolved_ip))
                            return "DIRECT";

                        if (url.substring(0, 4) == "ftp:")
                            return "DIRECT";

                        if (isInNet(resolved_ip, "100.64.0.0", "255.255.0.0"))
                            return "DIRECT";

                        if (((localHostOrDomainIs(host, "trust.zscaler.com")) ||
                                (localHostOrDomainIs(host, "trust.zscaler.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalerone.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalertwo.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalerthree.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalergov.net")) ||
                                (localHostOrDomainIs(host, "trust.zsdemo.net")) ||
                                (localHostOrDomainIs(host, "trust.zscloud.net")) ||
                                (localHostOrDomainIs(host, "trust.zsfalcon.net")) ||
                                (localHostOrDomainIs(host, "trust.zdxcloud.net")) ||
                                (localHostOrDomainIs(host, "trust.zdxpreview.net")) ||
                                (localHostOrDomainIs(host, "trust.zdxbeta.net")) ||
                                (localHostOrDomainIs(host, "trust.zsdevel.net")) ||
                                (localHostOrDomainIs(host, "trust.zsbetagov.net")) ||
                                (localHostOrDomainIs(host, "trust.zspreview.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalerten.net")) ||
                                (localHostOrDomainIs(host, "trust.zdxten.net")) ) &&
                                (url.substring(0,5) == "http:" || url.substring(0,6) == "https:"))
                            return "DIRECT";

                        return "PROXY ${GATEWAY_FX}:80; PROXY ${SECONDARY_GATEWAY_FX}:80; DIRECT";
                    }
                    """,
                )
                assert validate_pac_file is not None, "PAC file validation returned None"
                assert validate_pac_file.success, "PAC file validation failed"
            except Exception as exc:
                errors.append(f"Failed to validate PAC file: {exc}")

            # Test add_pac_file
            try:
                created_pac_file = client.pac_files.add_pac_file(
                    name=f"{pac_file_name}",
                    description=f"{pac_file_description}",
                    domain="bd-redhat.com",
                    pac_commit_message="tests-" + generate_random_string(),
                    pac_verification_status="VERIFY_NOERR",
                    pac_version_status="DEPLOYED",
                    pac_content="""
                    function FindProxyForURL(url, host) {
                        var privateIP = /^(0|10|127|192\\.168|172\\.1[6789]|172\\.2[0-9]|172\\.3[01]|169\\.254|192\\.88\\.99)\\.[0-9.]+$/;
                        var resolved_ip = dnsResolve(host);

                        if (isPlainHostName(host) || isInNet(resolved_ip, "192.0.2.0", "255.255.255.0") || privateIP.test(resolved_ip))
                            return "DIRECT";

                        if (url.substring(0, 4) == "ftp:")
                            return "DIRECT";

                        if (isInNet(resolved_ip, "100.64.0.0", "255.255.0.0"))
                            return "DIRECT";

                        if (((localHostOrDomainIs(host, "trust.zscaler.com")) ||
                                (localHostOrDomainIs(host, "trust.zscaler.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalerone.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalertwo.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalerthree.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalergov.net")) ||
                                (localHostOrDomainIs(host, "trust.zsdemo.net")) ||
                                (localHostOrDomainIs(host, "trust.zscloud.net")) ||
                                (localHostOrDomainIs(host, "trust.zsfalcon.net")) ||
                                (localHostOrDomainIs(host, "trust.zdxcloud.net")) ||
                                (localHostOrDomainIs(host, "trust.zdxpreview.net")) ||
                                (localHostOrDomainIs(host, "trust.zdxbeta.net")) ||
                                (localHostOrDomainIs(host, "trust.zsdevel.net")) ||
                                (localHostOrDomainIs(host, "trust.zsbetagov.net")) ||
                                (localHostOrDomainIs(host, "trust.zspreview.net")) ||
                                (localHostOrDomainIs(host, "trust.zscalerten.net")) ||
                                (localHostOrDomainIs(host, "trust.zdxten.net")) ) &&
                                (url.substring(0,5) == "http:" || url.substring(0,6) == "https:"))
                            return "DIRECT";

                        return "PROXY ${GATEWAY_FX}:80; PROXY ${SECONDARY_GATEWAY_FX}:80; DIRECT";
                    }
                    """,
                )
                assert created_pac_file is not None, "PAC file creation returned None"
                assert created_pac_file.name == pac_file_name, "PAC file name mismatch"
                assert created_pac_file.description == pac_file_description, "PAC file description mismatch"
                pac_id = created_pac_file.id
                pac_version = created_pac_file.pac_version
            except Exception as exc:
                errors.append(f"Failed to add PAC file: {exc}")

            # Test clone_pac_file
            # try:
            #     cloned_pac_file = client.pac_files.clone_pac_file(
            #         pac_id=pac_id,
            #         pac_version=pac_version,
            #         name=f"{pac_file_name}-clone",
            #         description=f"{pac_file_description}-clone",
            #         domain="bd-redhat.com",
            #         pac_commit_message="tests-" + generate_random_string(),
            #         pac_verification_status="VERIFY_NOERR",
            #         pac_version_status="DEPLOYED",
            #         pac_content="""
            #         function FindProxyForURL(url, host) {
            #             var privateIP = /^(0|10|127|192\\.168|172\\.1[6789]|172\\.2[0-9]|172\\.3[01]|169\\.254|192\\.88\\.99)\\.[0-9.]+$/;
            #             var resolved_ip = dnsResolve(host);

            #             if (isPlainHostName(host) || isInNet(resolved_ip, "192.0.2.0", "255.255.255.0") || privateIP.test(resolved_ip))
            #                 return "DIRECT";

            #             if (url.substring(0, 4) == "ftp:")
            #                 return "DIRECT";

            #             if (isInNet(resolved_ip, "100.64.0.0", "255.255.0.0"))
            #                 return "DIRECT";

            #             if (((localHostOrDomainIs(host, "trust.zscaler.com")) ||
            #                     (localHostOrDomainIs(host, "trust.zscaler.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zscalerone.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zscalertwo.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zscalerthree.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zscalergov.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zsdemo.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zscloud.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zsfalcon.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zdxcloud.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zdxpreview.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zdxbeta.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zsdevel.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zsbetagov.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zspreview.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zscalerten.net")) ||
            #                     (localHostOrDomainIs(host, "trust.zdxten.net")) ) &&
            #                     (url.substring(0,5) == "http:" || url.substring(0,6) == "https:"))
            #                 return "DIRECT";

            #             return "PROXY ${GATEWAY_FX}:80; PROXY ${SECONDARY_GATEWAY_FX}:80; DIRECT";
            #         }
            #         """,
            #     )
            #     assert cloned_pac_file is not None, "PAC file cloning returned None"
            #     assert cloned_pac_file.name == f"{pac_file_name}-clone", "Cloned PAC file name mismatch"
            #     assert cloned_pac_file.description == f"{pac_file_description}-clone", "Cloned PAC file description mismatch"
            # except Exception as exc:
            #     errors.append(f"Failed to clone PAC file: {exc}")

            # Test get_pac_file
            try:
                # Retrieve PAC file without filter
                retrieved_pac_file_list = client.pac_files.get_pac_file(pac_id)
                assert isinstance(retrieved_pac_file_list, list), f"Expected a list, got {type(retrieved_pac_file_list).__name__}"
                assert len(retrieved_pac_file_list) > 0, "No PAC files returned by get_pac_file"

                retrieved_pac_file = retrieved_pac_file_list[0]  # Access the first PAC file
                assert retrieved_pac_file["id"] == pac_id, f"Retrieved PAC file ID mismatch: {retrieved_pac_file['id']} != {pac_id}"
                assert retrieved_pac_file["name"] == pac_file_name, f"Retrieved PAC file name mismatch: {retrieved_pac_file['name']} != {pac_file_name}"

                # Retrieve PAC file with filter
                retrieved_pac_file_list_with_filter = client.pac_files.get_pac_file(pac_id, filter="pac_content")
                assert isinstance(retrieved_pac_file_list_with_filter, list), f"Expected a list, got {type(retrieved_pac_file_list_with_filter).__name__}"
                assert len(retrieved_pac_file_list_with_filter) > 0, "No PAC files returned by get_pac_file with filter"

                retrieved_pac_file_with_filter = retrieved_pac_file_list_with_filter[0]
                assert retrieved_pac_file_with_filter["id"] == pac_id, f"Retrieved PAC file ID mismatch with filter: {retrieved_pac_file_with_filter['id']} != {pac_id}"
            except Exception as exc:
                errors.append(f"Failed to retrieve PAC file: {exc}")

            # Test get_pac_file_version
            try:
                # Retrieve PAC file version without filter
                retrieved_pac_file_version = client.pac_files.get_pac_file_version(pac_id, pac_version)
                assert isinstance(retrieved_pac_file_version, dict) or isinstance(retrieved_pac_file_version, Box), (
                    f"Expected a dict or Box, got {type(retrieved_pac_file_version).__name__}"
                )
                # Use snake_case key for Box object or fallback to original key
                pac_version_key = "pac_version" if isinstance(retrieved_pac_file_version, Box) else "pacVersion"
                assert retrieved_pac_file_version[pac_version_key] == pac_version, (
                    f"Retrieved PAC file version mismatch: {retrieved_pac_file_version[pac_version_key]} != {pac_version}"
                )

                # Retrieve PAC file version with filter
                retrieved_pac_file_version_with_filter = client.pac_files.get_pac_file_version(
                    pac_id, pac_version, filter="pac_content"
                )
                assert isinstance(retrieved_pac_file_version_with_filter, dict) or isinstance(retrieved_pac_file_version_with_filter, Box), (
                    f"Expected a dict or Box, got {type(retrieved_pac_file_version_with_filter).__name__}"
                )
                assert retrieved_pac_file_version_with_filter[pac_version_key] == pac_version, (
                    f"Retrieved PAC file version mismatch with filter: {retrieved_pac_file_version_with_filter[pac_version_key]} != {pac_version}"
                )
            except Exception as exc:
                errors.append(f"Failed to retrieve PAC file version: {exc}")


        finally:
            # Cleanup: Attempt to delete the PAC file
            if pac_id:
                try:
                    delete_response_code = client.pac_files.delete_pac_file(pac_id)
                    assert str(delete_response_code) == "204", "Failed to delete PAC file"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the PAC file lifecycle test: {errors}"
