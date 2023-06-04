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


import json

from box import Box, BoxList
from restfly.endpoint import APIEndpoint


class DLPNotificationTemplateAPI(APIEndpoint):
    def list_templates(self, **kwargs) -> BoxList:
        """
        Returns a list of DLP Notification Templates.

        Returns:
            :obj:`BoxList`: List of DLP Notification Templates.

        Examples:
            Get a list of all DLP Notification Templates

            >>> results = zia.dlp_notification_template.list_templates()
            ... for template in results:
            ...    print(template)

        """
        return self._get("dlpNotificationTemplates")
