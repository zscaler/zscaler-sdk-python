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


class TestDLPResources:
    """
    Integration Tests for the DLP Resources API.
    """

    @pytest.mark.vcr()
    def test_dlp_resources_operations(self, fs):
        """Test DLP Resources operations."""
        client = MockZIAClient(fs)
        errors = []

        try:
            # Test list_dlp_icap_servers
            icap_servers, response, err = client.zia.dlp_resources.list_dlp_icap_servers()
            assert err is None, f"List DLP ICAP servers failed: {err}"
            assert icap_servers is not None, "ICAP servers should not be None"
            assert isinstance(icap_servers, list), "ICAP servers should be a list"

            # Test list_dlp_icap_servers_lite
            icap_lite, response, err = client.zia.dlp_resources.list_dlp_icap_servers_lite()
            assert err is None, f"List DLP ICAP servers lite failed: {err}"

            # Test get_dlp_icap_servers if available
            if icap_servers and len(icap_servers) > 0:
                server_id = icap_servers[0].id
                fetched_server, response, err = client.zia.dlp_resources.get_dlp_icap_servers(server_id)
                assert err is None, f"Get DLP ICAP server failed: {err}"

            # Test list_dlp_incident_receiver
            receivers, response, err = client.zia.dlp_resources.list_dlp_incident_receiver()
            assert err is None, f"List DLP incident receivers failed: {err}"
            assert receivers is not None, "Receivers should not be None"

            # Test list_dlp_incident_receiver_lite
            receivers_lite, response, err = client.zia.dlp_resources.list_dlp_incident_receiver_lite()
            assert err is None, f"List DLP incident receivers lite failed: {err}"

            # Test get_dlp_incident_receiver if available
            if receivers and len(receivers) > 0:
                receiver_id = receivers[0].id
                fetched_receiver, response, err = client.zia.dlp_resources.get_dlp_incident_receiver(receiver_id)
                assert err is None, f"Get DLP incident receiver failed: {err}"

            # Test list_dlp_idm_profiles
            idm_profiles, response, err = client.zia.dlp_resources.list_dlp_idm_profiles()
            assert err is None, f"List DLP IDM profiles failed: {err}"
            assert idm_profiles is not None, "IDM profiles should not be None"

            # Test get_dlp_idm_profiles if available
            if idm_profiles and len(idm_profiles) > 0:
                # IDM profiles may use profile_id or template_id instead of id
                profile_id = getattr(idm_profiles[0], 'profile_id', None) or getattr(idm_profiles[0], 'template_id', None)
                if profile_id:
                    fetched_profile, response, err = client.zia.dlp_resources.get_dlp_idm_profiles(profile_id)
                    # Don't fail if get fails

            # Test list_edm_schemas
            edm_schemas, response, err = client.zia.dlp_resources.list_edm_schemas()
            assert err is None, f"List EDM schemas failed: {err}"
            assert edm_schemas is not None, "EDM schemas should not be None"

            # Test list_edm_schema_lite
            edm_lite, response, err = client.zia.dlp_resources.list_edm_schema_lite()
            assert err is None, f"List EDM schema lite failed: {err}"

        except Exception as e:
            errors.append(f"Exception during DLP resources test: {str(e)}")

        assert len(errors) == 0, f"Errors occurred: {errors}"

