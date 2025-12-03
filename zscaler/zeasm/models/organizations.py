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

from typing import Any, Dict, List, Optional
from zscaler.oneapi_object import ZscalerObject
from zscaler.oneapi_collection import ZscalerCollection
from zscaler.zeasm.models import common as common


class Organizations(ZscalerObject):
    """
    A class for Organizations objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Organizations model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.next_page: Optional[Any] = config["next_page"] \
                if "next_page" in config else None
            self.prev_page: Optional[Any] = config["prev_page"] \
                if "prev_page" in config else None
            self.results = ZscalerCollection.form_list(
                config["results"] if "results" in config else [], common.CommonIDName
            )
            self.total_results: Optional[Any] = config["total_results"] \
                if "total_results" in config else None
        else:
            self.next_page: Optional[Any] = None
            self.prev_page: Optional[Any] = None
            self.results: List[Any] = ZscalerCollection.form_list([], str)
            self.total_results: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "next_page": self.next_page,
            "prev_page": self.prev_page,
            "results": self.results,
            "total_results": self.total_results
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
