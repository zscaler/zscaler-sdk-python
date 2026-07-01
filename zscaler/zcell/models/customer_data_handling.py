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
from zscaler.zcell.models import customer_data_handling as customer_data_handling


class CustomerDataHandling(ZscalerObject):
    """
    A class representing a CustomerDataHandling object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.email = config["email"] if "email" in config else None
            self.user_name = config["userName"] if "userName" in config else None
            if "zia" in config:
                if isinstance(config["zia"], customer_data_handling.ZCloud):
                    self.zia = config["zia"]
                elif config["zia"] is not None:
                    self.zia = customer_data_handling.ZCloud(config["zia"])
                else:
                    self.zia = None
            else:
                self.zia = None
            if "zpa" in config:
                if isinstance(config["zpa"], customer_data_handling.ZCloud):
                    self.zpa = config["zpa"]
                elif config["zpa"] is not None:
                    self.zpa = customer_data_handling.ZCloud(config["zpa"])
                else:
                    self.zpa = None
            else:
                self.zpa = None
            self.regions = ZscalerCollection.form_list(config["regions"] if "regions" in config else [], str)
            self.mvno_ids = ZscalerCollection.form_list(
                config["mvnoIds"] if "mvnoIds" in config else [], customer_data_handling.Mvno
            )
            if "simProvider" in config:
                if isinstance(config["simProvider"], customer_data_handling.SimProvider):
                    self.sim_provider = config["simProvider"]
                elif config["simProvider"] is not None:
                    self.sim_provider = customer_data_handling.SimProvider(config["simProvider"])
                else:
                    self.sim_provider = None
            else:
                self.sim_provider = None
            self.parent_id = config["parentId"] if "parentId" in config else None
            self.is_activated = config["isActivated"] if "isActivated" in config else False
            if "bcSize" in config:
                if isinstance(config["bcSize"], customer_data_handling.BcSizeEnum):
                    self.bc_size = config["bcSize"]
                elif config["bcSize"] is not None:
                    self.bc_size = customer_data_handling.BcSizeEnum(config["bcSize"])
                else:
                    self.bc_size = None
            else:
                self.bc_size = None
            if "platformType" in config:
                if isinstance(config["platformType"], customer_data_handling.PlatformTypeEnum):
                    self.platform_type = config["platformType"]
                elif config["platformType"] is not None:
                    self.platform_type = customer_data_handling.PlatformTypeEnum(config["platformType"])
                else:
                    self.platform_type = None
            else:
                self.platform_type = None
            self.total_sims = config["totalSims"] if "totalSims" in config else None
            self.active_sims = config["activeSims"] if "activeSims" in config else None
            self.inactive_sims = config["inactiveSims"] if "inactiveSims" in config else None
            self.current_usage = config["currentUsage"] if "currentUsage" in config else None
        else:
            self.id = None
            self.name = None
            self.email = None
            self.user_name = None
            self.zia = None
            self.zpa = None
            self.regions = []
            self.mvno_ids = []
            self.sim_provider = None
            self.parent_id = None
            self.is_activated = False
            self.bc_size = None
            self.platform_type = None
            self.total_sims = None
            self.active_sims = None
            self.inactive_sims = None
            self.current_usage = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "userName": self.user_name,
            "zia": self.zia,
            "zpa": self.zpa,
            "regions": self.regions,
            "mvnoIds": [item.request_format() for item in (self.mvno_ids or [])],
            "simProvider": self.sim_provider,
            "parentId": self.parent_id,
            "isActivated": self.is_activated,
            "bcSize": self.bc_size,
            "platformType": self.platform_type,
            "totalSims": self.total_sims,
            "activeSims": self.active_sims,
            "inactiveSims": self.inactive_sims,
            "currentUsage": self.current_usage,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ResponseMessage(ZscalerObject):
    """
    A class representing a ResponseMessage object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.id = config["id"] if "id" in config else None
            self.message = config["message"] if "message" in config else None
        else:
            self.id = None
            self.message = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "message": self.message,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ActivateCustomer(ZscalerObject):
    """
    A class representing a ActivateCustomer object.
    """

    def __init__(self, config=None):
        super().__init__(config)
        if config:
            self.username = config["username"] if "username" in config else None
            self.password = config["password"] if "password" in config else None
            self.api_key = config["apiKey"] if "apiKey" in config else None
        else:
            self.username = None
            self.password = None
            self.api_key = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "username": self.username,
            "password": self.password,
            "apiKey": self.api_key,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
