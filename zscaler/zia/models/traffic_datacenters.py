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

from zscaler.oneapi_object import ZscalerObject


class TrafficDatacenters(ZscalerObject):
    """
    A class for TrafficDatacenters objects.
    """

    def __init__(self, config=None):
        """
        Initialize the TrafficDatacenters model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.provider = config["provider"] if "provider" in config else None
            self.city = config["city"] if "city" in config else None
            self.timezone = config["timezone"] if "timezone" in config else None
            self.lat = config["lat"] if "lat" in config else None
            self.longi = config["longi"] if "longi" in config else None
            self.latitude = config["latitude"] if "latitude" in config else None
            self.longitude = config["longitude"] if "longitude" in config else None
            self.gov_only = config["govOnly"] if "govOnly" in config else None
            self.third_party_cloud = config["thirdPartyCloud"] if "thirdPartyCloud" in config else None
            self.upload_bandwidth = config["uploadBandwidth"] if "uploadBandwidth" in config else None
            self.download_bandwidth = config["downloadBandwidth"] if "downloadBandwidth" in config else None
            self.owned_by_customer = config["ownedByCustomer"] if "ownedByCustomer" in config else None
            self.managed_bcp = config["managedBcp"] if "managedBcp" in config else None
            self.dont_publish = config["dontPublish"] if "dontPublish" in config else None
            self.dont_provision = config["dontProvision"] if "dontProvision" in config else None
            self.not_ready_for_use = config["notReadyForUse"] if "notReadyForUse" in config else None
            self.for_future_use = config["forFutureUse"] if "forFutureUse" in config else None
            self.regional_surcharge = config["regionalSurcharge"] if "regionalSurcharge" in config else None
            self.create_time = config["createTime"] if "createTime" in config else None
            self.last_modified_time = config["lastModifiedTime"] if "lastModifiedTime" in config else None
            self.virtual = config["virtual"] if "virtual" in config else None
        else:
            self.id = None
            self.name = None
            self.provider = None
            self.city = None
            self.timezone = None
            self.lat = None
            self.longi = None
            self.latitude = None
            self.longitude = None
            self.gov_only = None
            self.third_party_cloud = None
            self.upload_bandwidth = None
            self.download_bandwidth = None
            self.owned_by_customer = None
            self.managed_bcp = None
            self.dont_publish = None
            self.dont_provision = None
            self.not_ready_for_use = None
            self.for_future_use = None
            self.regional_surcharge = None
            self.create_time = None
            self.last_modified_time = None
            self.virtual = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "city": self.city,
            "timezone": self.timezone,
            "lat": self.lat,
            "longi": self.longi,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "govOnly": self.gov_only,
            "thirdPartyCloud": self.third_party_cloud,
            "uploadBandwidth": self.upload_bandwidth,
            "downloadBandwidth": self.download_bandwidth,
            "ownedByCustomer": self.owned_by_customer,
            "managedBcp": self.managed_bcp,
            "dontPublish": self.dont_publish,
            "dontProvision": self.dont_provision,
            "notReadyForUse": self.not_ready_for_use,
            "forFutureUse": self.for_future_use,
            "regionalSurcharge": self.regional_surcharge,
            "createTime": self.create_time,
            "lastModifiedTime": self.last_modified_time,
            "virtual": self.virtual,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
