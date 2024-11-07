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

from zscaler.zia import ZIAClientHelper

PYTEST_MOCK_CLIENT = "pytest_mock_client"


class MockZIAClient(ZIAClientHelper):
    def __init__(self, fs):
        # Fetch credentials from environment variables
        username = os.environ.get("ZIA_USERNAME")
        password = os.environ.get("ZIA_PASSWORD")
        api_key = os.environ.get("ZIA_API_KEY")
        cloud = os.environ.get("ZIA_CLOUD")
        sandbox_token = os.environ.get("ZIA_SANDBOX_TOKEN")

        if PYTEST_MOCK_CLIENT in os.environ:
            fs.pause()
            super().__init__()
            fs.resume()
        else:
            super().__init__(
                username=username,
                password=password,
                api_key=api_key,
                cloud=cloud,
                sandbox_token=sandbox_token,
                cache=None,
                fail_safe=False,
            )
