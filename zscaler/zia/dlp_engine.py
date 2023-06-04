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


class DLPEngineAPI(APIEndpoint):
    def list_engines(self, query: str = None) -> BoxList:
        """
        Returns the list of ZIA DLP Engines.

        Args:
            query (str): A search string used to match against a DLP Engine's name or description attributes.

        Returns:
            :obj:`BoxList`: A list containing ZIA DLP Engines.

        Examples:
            Print all dlp engines

            >>> for dlp engines in zia.dlp_engine.list_engines():
            ...    pprint(engine)

            Print engines that match the name or description 'GDPR'

            >>> pprint(zia.dlp_engine.list_engines('GDPR'))

        """
        payload = {"search": query}
        return self._get("dlpEngines", params=payload)

    def get_engine(self, engine_id: str) -> Box:
        """
        Returns the dlp engine details for a given DLP Engine.

        Args:
            engine_id (str): The unique identifier for the DLP Engine.

        Returns:
            :obj:`Box`: The DLP Engine resource record.

        Examples:
            >>> engine = zia.dlp_engine.get_engine('99999')

        """
        return self._get(f"dlpEngines/{engine_id}")
