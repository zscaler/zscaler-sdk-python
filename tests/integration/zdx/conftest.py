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

from zscaler.oneapi_client import LegacyZDXClient
from zscaler.zdx.admin import AdminAPI
from zscaler.zdx.apps import AppsAPI
from zscaler.zdx.alerts import AlertsAPI
from zscaler.zdx.devices import DevicesAPI
from zscaler.zdx.inventory import InventoryAPI
from zscaler.zdx.troubleshooting import TroubleshootingAPI
from zscaler.zdx.users import UsersAPI

PYTEST_MOCK_CLIENT = "pytest_mock_client"


class MockZDXClient(LegacyZDXClient):
    def __init__(self, fs, config=None):
        """
        Initialize the MockZDXClient with support for environment variables and
        optional inline config.
        
        Args:
            fs: Fixture to pause/resume the filesystem mock for pyfakefs.
            config: Optional dictionary containing client configuration (client_id, client_secret, etc.).
        """
        # If config is not provided, initialize it as an empty dictionary
        config = config or {}
        
        # Fetch credentials from environment variables, allowing them to be overridden by the config dictionary
        client_id = config.get("client_id", os.getenv("ZDX_CLIENT_ID"))
        client_secret = config.get("client_secret", os.getenv("ZDX_CLIENT_SECRET"))

        # Extract logging configuration or use defaults
        logging_config = config.get("logging", {
            "enabled": False, 
            "verbose": False
        })
        
        # Set up the client config dictionary
        client_config = {
            "client_id": client_id,
            "client_secret": client_secret,
            "logging": {
                "enabled": logging_config.get("enabled", True), 
                "verbose": logging_config.get("verbose", True)
            },
        }

        if PYTEST_MOCK_CLIENT in os.environ:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)
