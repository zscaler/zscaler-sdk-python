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


class Findings(ZscalerObject):
    """
    A class for Findings objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Findings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.results = ZscalerCollection.form_list(
                config["results"] if "results" in config else [], FindingDetails
            )
            self.total_results: Optional[Any] = config["total_results"] \
                if "total_results" in config else None
        else:
            self.results: List[Any] = ZscalerCollection.form_list([], str)
            self.total_results: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "results": self.results,
            "total_results": self.total_results
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class FindingDetails(ZscalerObject):
    """
    A class for FindingDetails objects.
    """

    def __init__(self, config=None):
        """
        Initialize the FindingDetails model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.category = config["category"] \
                if "category" in config else None
            self.cisa_likelihood = config["cisa_likelihood"] \
                if "cisa_likelihood" in config else None
            self.country = config["country"] \
                if "country" in config else None
            self.description = config["description"] \
                if "description" in config else None
            self.epss_likelihood = config["epss_likelihood"] \
                if "epss_likelihood" in config else None
            self.first_seen = config["first_seen"] \
                if "first_seen" in config else None
            self.id = config["id"] \
                if "id" in config else None
            self.impacted_asset_id = config["impacted_asset_id"] \
                if "impacted_asset_id" in config else None
            self.impacted_asset_name = config["impacted_asset_name"] \
                if "impacted_asset_name" in config else None
            self.is_stale = config["is_stale"] \
                if "is_stale" in config else None
            self.last_seen = config["last_seen"] \
                if "last_seen" in config else None
            self.name = config["name"] \
                if "name" in config else None
            self.profile_id = config["profile_id"] \
                if "profile_id" in config else None
            self.risk_level = config["risk_level"] \
                if "risk_level" in config else None
            self.risk_score = config["risk_score"] \
                if "risk_score" in config else None
            self.scan_type = config["scan_type"] \
                if "scan_type" in config else None
            self.severity_score = config["severity_score"] \
                if "severity_score" in config else None
            self.status = config["status"] \
                if "status" in config else None
            self.type = config["type"] \
                if "type" in config else None
        else:
            self.category = None
            self.cisa_likelihood = None
            self.country = None
            self.description = None
            self.epss_likelihood = None
            self.first_seen = None
            self.id = None
            self.impacted_asset_id = None
            self.impacted_asset_name = None
            self.is_stale = None
            self.last_seen = None
            self.name = None
            self.profile_id = None
            self.risk_level = None
            self.risk_score = None
            self.scan_type = None
            self.severity_score = None
            self.status = None
            self.type = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "category": self.category,
            "cisa_likelihood": self.cisa_likelihood,
            "country": self.country,
            "description": self.description,
            "epss_likelihood": self.epss_likelihood,
            "first_seen": self.first_seen,
            "id": self.id,
            "impacted_asset_id": self.impacted_asset_id,
            "impacted_asset_name": self.impacted_asset_name,
            "is_stale": self.is_stale,
            "last_seen": self.last_seen,
            "name": self.name,
            "profile_id": self.profile_id,
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "scan_type": self.scan_type,
            "severity_score": self.severity_score,
            "status": self.status,
            "type": self.type
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class CommonFindings(ZscalerObject):
    """
    A class for CommonFindings objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the CommonFindings model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.content: Optional[Any] = config["content"] \
                if "content" in config else None
            self.source_type: Optional[Any] = config["source_type"] \
                if "source_type" in config else None
        else:
            self.content: Optional[Any] = None
            self.source_type: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "content": self.content,
            "source_type": self.source_type,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
