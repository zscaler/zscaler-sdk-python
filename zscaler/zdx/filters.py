# filters.py
from zscaler.utils import CommonFilters


class GetDevicesFilters(CommonFilters):
    def __init__(self, user_ids=None, emails=None, mac_address=None, private_ipv4=None, **kwargs):
        super().__init__(**kwargs)
        self.user_ids = user_ids
        self.emails = emails
        self.mac_address = mac_address
        self.private_ipv4 = private_ipv4

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {
                "userids": self.user_ids,
                "emails": self.emails,
                "mac_address": self.mac_address,
                "private_ipv4": self.private_ipv4,
            }
        )
        return base_dict


class GeoLocationFilter(CommonFilters):
    def __init__(self, parent_geo_id=None, search=None, **kwargs):
        super().__init__(**kwargs)
        self.parent_geo_id = parent_geo_id
        self.search = search

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {
                "parent_geo_id": self.parent_geo_id,
                "search": self.search,
            }
        )
        return base_dict


class GetSoftwareFilters(CommonFilters):
    def __init__(self, user_ids=None, device_ids=None, software_key=None, **kwargs):
        super().__init__(**kwargs)
        self.user_ids = user_ids
        self.device_ids = device_ids
        self.software_key = software_key

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update(
            {
                "user_ids": self.user_ids,
                "device_ids": self.device_ids,
                "software_key": self.software_key,
            }
        )
        return base_dict
