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


from box import Box, BoxList
from restfly.endpoint import APIEndpoint


class DLPIncidentReceiverAPI(APIEndpoint):
    def list_receiver(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA Incident Receivers.

        Args:
            query (str): A search string used to match against a Incident Receiver's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP Incident Receivers.

        Examples:
            Print all incident receivers

            >>> for dlp receiver in zia.dlp_incident_receiver.list_receiver():
            ...    pprint(receiver)

            Print Incident Receivers that match the name or description 'ZS_INC_RECEIVER_01'

            >>> pprint(zia.dlp_incident_receiver.list_receiver('ZS_INC_RECEIVER_01'))

        """
        payload = {"search": query}
        return self._get("incidentReceiverServers", params=payload)

    def get_receiver(self, receiver_id: str) -> Box:
        """
        Returns the dlp incident receiver details for a given DLP Incident Receiver.

        Args:
            icap_server_id (str): The unique identifier for the DLP Incident Receiver.

        Returns:
            :obj:`Box`: The DLP Incident Receiver resource record.

        Examples:
            >>> receiver = zia.dlp_incident_receiver.get_receiver('99999')

        """
        return self._get(f"incidentReceiverServers/{receiver_id}")
