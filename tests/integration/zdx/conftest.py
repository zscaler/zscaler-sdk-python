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

import os

from zscaler.zdx import ZDXClientHelper
from zscaler.zdx.admin import AdminAPI
from zscaler.zdx.apps import AppsAPI
from zscaler.zdx.alerts import AlertsAPI
from zscaler.zdx.devices import DevicesAPI
from zscaler.zdx.inventory import InventoryAPI
from zscaler.zdx.troubleshooting import TroubleshootingAPI
from zscaler.zdx.users import UsersAPI

PYTEST_MOCK_CLIENT = "pytest_mock_client"


class MockZDXClient(ZDXClientHelper):
    def __init__(self, fs):
        # Fetch credentials from environment variables
        client_id = os.environ.get("ZDX_CLIENT_ID")
        client_secret = os.environ.get("ZDX_CLIENT_SECRET")

        if PYTEST_MOCK_CLIENT in os.environ:
            fs.pause()
            super().__init__()
            fs.resume()
        else:
            super().__init__(
                client_id=client_id,
                client_secret=client_secret,
            )

        # Instantiate the admin API
        self.admin = AdminAPI(self)
        self.apps = AppsAPI(self)
        self.alerts = AlertsAPI(self)
        self.devices = DevicesAPI(self)
        self.inventory = InventoryAPI(self)
        self.troubleshooting = TroubleshootingAPI(self)
        self.users = UsersAPI(self)
