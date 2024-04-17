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


from box import BoxList

from zscaler.zia import ZIAClient


class DeviceManagementAPI:
    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_device_groups(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA Device Groups.

        Args:
            query (str): A search string used to match against a Device Group's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA Device Groups.

        Examples:
            Print all device groups

            >>> for device group in zia.device_groups.list_device_groups():
            ...    pprint(device)

            Print Device Groups that match the name or description 'Windows'

            >>> pprint(zia.device_groups.list_device_groups('Windows'))

        """
        payload = {"search": query}
        return self.rest.get("deviceGroups", params=payload)

    def list_devices(self, query: str = None) -> BoxList:
        """
        Returns the list of Devices.

        Args:
            query (str): A search string used to match against a Device's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing Device.

        Examples:
            Print all devices

            >>> for dlp idm in zia.device_groups.list_devices():
            ...    pprint(idm)

            Print IDM profiles that match the name or description 'WINDOWS_OS'

            >>> pprint(zia.device_groups.list_devices('WINDOWS_OS'))

        """
        payload = {"search": query}
        return self.rest.get("deviceGroups/devices", params=payload)

    def list_device_lite(self) -> BoxList:
        """
        Returns the list of devices that includes device ID, name, and owner name.

        Returns:
            :obj:`BoxList`: List of Device/ids.

        Examples:
            Get Device Lite results

            >>> results = zia.device.list_device_lite()
            ... for item in results:
            ...    print(item)

        """
        return self.rest.get("deviceGroups/devices/lite")
