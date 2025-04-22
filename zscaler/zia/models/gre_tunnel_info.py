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


class GreTunnelInfo(ZscalerObject):
    """
    A class for GreTunnelInfo objects.
    """

    def __init__(self, config=None):
        """
        Initialize the GreTunnelInfo model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.ip_address = config["ipAddress"] if "ipAddress" in config else None
            self.gre_enabled = config["greEnabled"] if "greEnabled" in config else None
            self.gre_tunnel_ip = config["greTunnelIP"] if "greTunnelIP" in config else None
            self.primary_gw = config["primaryGW"] if "primaryGW" in config else None
            self.secondary_gw = config["secondaryGW"] if "secondaryGW" in config else None
            self.tunid = config["tunID"] if "tunID" in config else None
            self.gre_range_primary = config["greRangePrimary"] if "greRangePrimary" in config else None
            self.gre_range_secondary = config["greRangeSecondary"] if "greRangeSecondary" in config else None
        else:
            self.ip_address = None
            self.gre_enabled = None
            self.gre_tunnel_ip = None
            self.primary_gw = None
            self.secondary_gw = None
            self.tunid = None
            self.gre_range_primary = None
            self.gre_range_secondary = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "ipAddress": self.ip_address,
            "greEnabled": self.gre_enabled,
            "greTunnelIP": self.gre_tunnel_ip,
            "primaryGW": self.primary_gw,
            "secondaryGW": self.secondary_gw,
            "tunID": self.tunid,
            "greRangePrimary": self.gre_range_primary,
            "greRangeSecondary": self.gre_range_secondary,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
