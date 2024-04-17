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
from functools import wraps

from zscaler.zpa import ZPAClientHelper

PYTEST_MOCK_CLIENT = "pytest_mock_client"


class MockZPAClient(ZPAClientHelper):
    def __init__(self, fs):
        # Fetch credentials from environment variables
        client_id = os.environ.get("ZPA_CLIENT_ID")
        client_secret = os.environ.get("ZPA_CLIENT_SECRET")
        customer_id = os.environ.get("ZPA_CUSTOMER_ID")
        cloud = os.environ.get("ZPA_CLOUD")

        if PYTEST_MOCK_CLIENT in os.environ:
            fs.pause()
            super().__init__()
            fs.resume()
        else:
            super().__init__(
                client_id=client_id,
                client_secret=client_secret,
                customer_id=customer_id,
                cloud=cloud,
                timeout=240,
                cache=None,
                fail_safe=False,
            )


def stub_sleep(func):
    """Decorator to speed up time.sleep function used in any methods under test."""
    import time
    from time import sleep

    def newsleep(seconds):
        sleep_speed_factor = 10.0
        sleep(seconds / sleep_speed_factor)

    time.sleep = newsleep

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
