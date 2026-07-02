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
from zscaler.zcell.models import network_events as network_events


class NetworkEvents(ZscalerObject):
    """
    A class representing a NetworkEvents object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.account_id = config["accountId"] if "accountId" in config else None
            self.seller_id = config["sellerId"] if "sellerId" in config else None
            self.country = config["country"] if "country" in config else None
            self.imsi = config["imsi"] if "imsi" in config else None
            self.operator_name = config["operatorName"] if "operatorName" in config else None
            self.sim_name = config["simName"] if "simName" in config else None
            self.source_system = config["sourceSystem"] if "sourceSystem" in config else None
            self.timestamp = config["timestamp"] if "timestamp" in config else None
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.loc_cid = config["locCid"] if "locCid" in config else None
            self.loc_lac = config["locLac"] if "locLac" in config else None
            self.loc_mcc = config["locMcc"] if "locMcc" in config else None
            self.loc_mnc = config["locMnc"] if "locMnc" in config else None
            self.rat_type = config["ratType"] if "ratType" in config else None
            self.zone = config["zone"] if "zone" in config else None
            self.data_cap_reached = config["dataCapReached"] if "dataCapReached" in config else False
            self.event_name = config["eventName"] if "eventName" in config else None
            self.iccid = config["iccid"] if "iccid" in config else None
            self.session_id = config["sessionId"] if "sessionId" in config else None
            self.sim_id = config["simId"] if "simId" in config else None
            self.sim_eid = config["simEid"] if "simEid" in config else None
            self.tags = ZscalerCollection.form_list(config["tags"] if "tags" in config else [], str)
            self.account_name = config["accountName"] if "accountName" in config else None
            self.outcome = config["outcome"] if "outcome" in config else None
        else:
            self.account_id = None
            self.seller_id = None
            self.country = None
            self.imsi = None
            self.operator_name = None
            self.sim_name = None
            self.source_system = None
            self.timestamp = None
            self.ip_address = None
            self.loc_cid = None
            self.loc_lac = None
            self.loc_mcc = None
            self.loc_mnc = None
            self.rat_type = None
            self.zone = None
            self.data_cap_reached = False
            self.event_name = None
            self.iccid = None
            self.session_id = None
            self.sim_id = None
            self.sim_eid = None
            self.tags = []
            self.account_name = None
            self.outcome = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "accountId": self.account_id,
            "sellerId": self.seller_id,
            "country": self.country,
            "imsi": self.imsi,
            "operatorName": self.operator_name,
            "simName": self.sim_name,
            "sourceSystem": self.source_system,
            "timestamp": self.timestamp,
            "ipAddress": self.ip_address,
            "locCid": self.loc_cid,
            "locLac": self.loc_lac,
            "locMcc": self.loc_mcc,
            "locMnc": self.loc_mnc,
            "ratType": self.rat_type,
            "zone": self.zone,
            "dataCapReached": self.data_cap_reached,
            "eventName": self.event_name,
            "iccid": self.iccid,
            "sessionId": self.session_id,
            "simId": self.sim_id,
            "simEid": self.sim_eid,
            "tags": self.tags,
            "accountName": self.account_name,
            "outcome": self.outcome,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SearchRequest(ZscalerObject):
    """
    A class representing a SearchRequest object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            if "sortBy" in config:
                if isinstance(config["sortBy"], network_events.SortBy):
                    self.sort_by = config["sortBy"]
                elif config["sortBy"] is not None:
                    self.sort_by = network_events.SortBy(config["sortBy"])
                else:
                    self.sort_by = None
            else:
                self.sort_by = None
            self.filter_by = ZscalerCollection.form_list(
                config["filterBy"] if "filterBy" in config else [], network_events.FilterBy
            )
            self.exclude_apn_config = config["excludeApnConfig"] if "excludeApnConfig" in config else False
            self.page = config["page"] if "page" in config else None
            self.size = config["size"] if "size" in config else None
        else:
            self.sort_by = None
            self.filter_by = []
            self.exclude_apn_config = False
            self.page = None
            self.size = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "sortBy": self.sort_by,
            "filterBy": [item.request_format() for item in (self.filter_by or [])],
            "excludeApnConfig": self.exclude_apn_config,
            "page": self.page,
            "size": self.size,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class SortBy(ZscalerObject):
    """
    A class representing a SortBy object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.name = config["name"] if "name" in config else None
        else:
            self.name = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "name": self.name,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class FilterBy(ZscalerObject):
    """
    A class representing a FilterBy object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.filter_name = config["filterName"] if "filterName" in config else None
            self.operator = config["operator"] if "operator" in config else None
            self.values = ZscalerCollection.form_list(config["values"] if "values" in config else [], str)
        else:
            self.filter_name = None
            self.operator = None
            self.values = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "filterName": self.filter_name,
            "operator": self.operator,
            "values": self.values,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
