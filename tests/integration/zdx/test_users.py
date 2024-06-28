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
import time
from pprint import pprint
from tests.integration.zdx.conftest import MockZDXClient


@pytest.fixture
def fs():
    yield


class TestUsers:
    """
    Integration Tests for the users
    """

    def test_list_users(self, fs):
        client = MockZDXClient(fs)
        errors = []

        try:
            # time.sleep(5)  # Sleep for 5 seconds before making the request
            now = int(time.time())
            from_time = now - 2 * 60 * 60  # 2 hours ago
            to_time = now

            kwargs = {
                "from_time": from_time,
                "to": to_time,
            }

            users_iterator = client.users.list_users(**kwargs)
            users = list(users_iterator)

            if not users:
                print("No users found within the specified time range.")
            else:
                print(f"Retrieved {len(users)} users")
                for user in users:
                    pprint(user)
        except Exception as e:
            errors.append(f"Exception occurred: {e}")

        assert not errors, "Errors occurred:\n{}".format("\n".join(errors))
