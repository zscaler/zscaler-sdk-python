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


class LookALikeDomains(ZscalerObject):
    """
    A class for LookALikeDomains objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LookALikeDomains model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.results = ZscalerCollection.form_list(
                config["results"] if "results" in config else [], LookalikeDomainDetails
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


class LookalikeDomainDetails(ZscalerObject):
    """
    A class for LookalikeDomainDetails objects.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the LookalikeDomainDetails model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.created_date: Optional[Any] = config["created_date"] \
                if "created_date" in config else None
            self.deception_method: List[Any] = ZscalerCollection.form_list(
                config["deception_method"] if "deception_method" in config else [], str
            )
            self.description: Optional[Any] = config["description"] \
                if "description" in config else None
            self.expiration_date: Optional[Any] = config["expiration_date"] \
                if "expiration_date" in config else None
            self.is_registered: Optional[Any] = config["is_registered"] \
                if "is_registered" in config else None
            self.lookalike_raw: Optional[Any] = config["lookalike_raw"] \
                if "lookalike_raw" in config else None
            self.original_domain: Optional[Any] = config["original_domain"] \
                if "original_domain" in config else None
            self.registered_by: Optional[Any] = config["registered_by"] \
                if "registered_by" in config else None
            self.registrar: Optional[Any] = config["registrar"] \
                if "registrar" in config else None
            self.remediation: Optional[Any] = config["remediation"] \
                if "remediation" in config else None
            self.risk_category: Optional[Any] = config["risk_category"] \
                if "risk_category" in config else None
            self.risk_score: Optional[Any] = config["risk_score"] \
                if "risk_score" in config else None
            self.status: Optional[Any] = config["status"] \
                if "status" in config else None
            self.updated_date: Optional[Any] = config["updated_date"] \
                if "updated_date" in config else None
        else:
            self.created_date: Optional[Any] = None
            self.deception_method: List[Any] = []
            self.description: Optional[Any] = None
            self.expiration_date: Optional[Any] = None
            self.is_registered: Optional[Any] = None
            self.lookalike_raw: Optional[Any] = None
            self.original_domain: Optional[Any] = None
            self.registered_by: Optional[Any] = None
            self.registrar: Optional[Any] = None
            self.remediation: Optional[Any] = None
            self.risk_category: Optional[Any] = None
            self.risk_score: Optional[Any] = None
            self.status: Optional[Any] = None
            self.updated_date: Optional[Any] = None

    def request_format(self) -> Dict[str, Any]:
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "created_date": self.created_date,
            "deception_method": self.deception_method,
            "description": self.description,
            "expiration_date": self.expiration_date,
            "is_registered": self.is_registered,
            "lookalike_raw": self.lookalike_raw,
            "original_domain": self.original_domain,
            "registered_by": self.registered_by,
            "registrar": self.registrar,
            "remediation": self.remediation,
            "risk_category": self.risk_category,
            "risk_score": self.risk_score,
            "status": self.status,
            "updated_date": self.updated_date
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
