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

import os

from zscaler import ZscalerClient

PYTEST_MOCK_CLIENT = "pytest_mock_client"


class MockZIAClient(ZscalerClient):
    def __init__(self, fs, config=None):
        """
        Initialize the MockZPAClient with support for environment variables and
        optional inline config.
        
        Args:
            fs: Fixture to pause/resume the filesystem mock for pyfakefs.
            config: Optional dictionary containing client configuration (clientId, clientSecret, etc.).
        """
        # If config is not provided, initialize it as an empty dictionary
        config = config or {}

        # Fetch credentials from environment variables, allowing them to be overridden by the config dictionary
        clientId = config.get("clientId", os.getenv("ZSCALER_CLIENT_ID"))
        clientSecret = config.get("clientSecret", os.getenv("ZSCALER_CLIENT_SECRET"))
        customerId = config.get("customerId", os.getenv("ZPA_CUSTOMER_ID"))
        vanityDomain = config.get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "PRODUCTION"))
        
        # Extract logging configuration or use defaults
        logging_config = config.get("logging", {
            "enabled": False, 
            "verbose": False
        })

        # Set up the client config dictionary
        client_config = {
            "clientId": clientId,
            "clientSecret": clientSecret,
            "customerId": customerId,
            "vanityDomain": vanityDomain,
            "cloud": cloud,
            "logging": {
                "enabled": logging_config.get("enabled", True), 
                "verbose": logging_config.get("verbose", True)
            },
        }

        # Check if we are running in a pytest mock environment
        if PYTEST_MOCK_CLIENT in os.environ:
            fs.pause()
            super().__init__(client_config)
            fs.resume()
        else:
            super().__init__(client_config)
