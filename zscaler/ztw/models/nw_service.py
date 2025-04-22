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
from zscaler.oneapi_collection import ZscalerCollection


class NetworkServices(ZscalerObject):
    """
    A class representing a Network Services object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None

            self.name = config["name"] if "name" in config else None

            self.description = config["description"] if "description" in config else None

            self.tag = config["tag"] if "tag" in config else None

            self.type = config["type"] if "type" in config else None

            self.creator_context = config["creatorContext"] if "creatorContext" in config else None

            self.is_name_l10n_tag = config["isNameL10nTag"] if "isNameL10nTag" in config else None

            # Use ZscalerCollection.form_list to handle port ranges with the PortRange class
            self.src_tcp_ports = ZscalerCollection.form_list(config.get("srcTcpPorts", []), PortRange)
            self.dest_tcp_ports = ZscalerCollection.form_list(config.get("destTcpPorts", []), PortRange)
            self.src_udp_ports = ZscalerCollection.form_list(config.get("srcUdpPorts", []), PortRange)
            self.dest_udp_ports = ZscalerCollection.form_list(config.get("destUdpPorts", []), PortRange)
        else:
            self.id = None
            self.name = None
            self.description = None
            self.tag = None
            self.type = None
            self.creator_context = None
            self.is_name_l10n_tag = None
            self.src_tcp_ports = []
            self.dest_tcp_ports = []
            self.src_udp_ports = []
            self.dest_udp_ports = []

    def request_format(self):
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tag": self.tag,
            "type": self.type,
            "creatorContext": self.creator_context,
            "isNameL10nTag": self.is_name_l10n_tag,
            "srcTcpPorts": [port.request_format() for port in self.src_tcp_ports],
            "destTcpPorts": [port.request_format() for port in self.dest_tcp_ports],
            "srcUdpPorts": [port.request_format() for port in self.src_udp_ports],
            "destUdpPorts": [port.request_format() for port in self.dest_udp_ports],
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PortRange(ZscalerObject):
    """
    A class representing a port range with a start and optional end.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.start = config["start"] if "start" in config else None
            self.end = config["end"] if "end" in config else None
        else:
            self.start = None
            self.end = None

    def request_format(self):
        return {"start": self.start, "end": self.end}
