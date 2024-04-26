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

"""Official Python SDK for the Zscaler Products (Beta)

Zscaler SDK Python is an SDK that provides a uniform and easy-to-use
interface for each of the Zscaler product APIs.

Documentation available at https://zscaler-sdk-python.readthedocs.io

"""

__author__ = "Zscaler Inc"
__email__ = "devrel@zscaler.com"
__license__ = "MIT"
__contributors__ = [
    "William Guilherme",
]
__version__ = "0.1.5"

from zscaler.zia import ZIAClientHelper  # noqa
from zscaler.zpa import ZPAClientHelper  # noqa
