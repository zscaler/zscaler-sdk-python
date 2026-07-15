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

from zscaler.oneapi_collection import ZscalerCollection
from zscaler.oneapi_object import ZscalerObject


class CustomerRegionHandling(ZscalerObject):
    """
    A class representing a CustomerRegionHandling object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.region = config["region"] if "region" in config else None
            self.configured = config["configured"] if "configured" in config else False
        else:
            self.region = None
            self.configured = False

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "region": self.region,
            "configured": self.configured,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApiDeployRegionsRequestBody(ZscalerObject):
    """
    A class representing a ApiDeployRegionsRequestBody object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            pass
        else:
            pass

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {}
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ExtendedRegionStatus(ZscalerObject):
    """
    A class representing a ExtendedRegionStatus object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.region = config["region"] if "region" in config else None
            self.operational_status = config["operationalStatus"] if "operationalStatus" in config else None
            if "bc" in config:
                if isinstance(config["bc"], BC):
                    self.bc = config["bc"]
                elif config["bc"] is not None:
                    self.bc = BC(config["bc"])
                else:
                    self.bc = None
            else:
                self.bc = None
            if "ac" in config:
                if isinstance(config["ac"], AC):
                    self.ac = config["ac"]
                elif config["ac"] is not None:
                    self.ac = AC(config["ac"])
                else:
                    self.ac = None
            else:
                self.ac = None
            self.map_a_c_status = config["mapACStatus"] if "mapACStatus" in config else None
            self.map_b_c_status = config["mapBCStatus"] if "mapBCStatus" in config else None
        else:
            self.region = None
            self.operational_status = None
            self.bc = None
            self.ac = None
            self.map_a_c_status = None
            self.map_b_c_status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "region": self.region,
            "operationalStatus": self.operational_status,
            "bc": self.bc,
            "ac": self.ac,
            "mapACStatus": self.map_a_c_status,
            "mapBCStatus": self.map_b_c_status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class BC(ZscalerObject):
    """
    A class representing a BC object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.status = config["status"] if "status" in config else None
            self.operational_status = ZscalerCollection.form_list(
                config["operationalStatus"] if "operationalStatus" in config else [], OperationalStatus
            )
        else:
            self.status = None
            self.operational_status = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
            "operationalStatus": [item.request_format() for item in (self.operational_status or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AC(ZscalerObject):
    """
    A class representing a AC object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.status = config["status"] if "status" in config else None
            self.operational_status = ZscalerCollection.form_list(
                config["operationalStatus"] if "operationalStatus" in config else [], OperationalStatus
            )
        else:
            self.status = None
            self.operational_status = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "status": self.status,
            "operationalStatus": [item.request_format() for item in (self.operational_status or [])],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class OperationalStatus(ZscalerObject):
    """
    A class representing a OperationalStatus object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.status = config["status"] if "status" in config else None
        else:
            self.id = None
            self.name = None
            self.status = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
