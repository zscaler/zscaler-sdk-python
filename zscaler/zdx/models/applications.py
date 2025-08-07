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
from zscaler.zdx.models import common


class ActiveApplications(ZscalerObject):
    """
    A class for Active Applications objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Active Applications model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.score = config["score"] if "score" in config else None
            self.total_users = config["total_users"] if "total_users" in config else None

            if "most_impacted_region" in config:
                if isinstance(config["most_impacted_region"], common.MostImpactedRegion):
                    self.most_impacted_region = config["most_impacted_region"]
                elif config["most_impacted_region"] is not None:
                    self.most_impacted_region = common.MostImpactedRegion(config["most_impacted_region"])
                else:
                    self.most_impacted_region = None
            else:
                self.most_impacted_region = None

        else:
            self.id = None
            self.name = None
            self.score = None
            self.total_users = None
            self.most_impacted_region = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "total_users": self.total_users,
            "most_impacted_region": self.most_impacted_region,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationScore(ZscalerObject):
    """
    A class for Application Score objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ApplicationScore model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.id = config["id"] if "id" in config else None
            self.name = config["name"] if "name" in config else None
            self.score = config["score"] if "score" in config else None

            if "most_impacted_region" in config:
                if isinstance(config["most_impacted_region"], common.MostImpactedRegion):
                    self.most_impacted_region = config["most_impacted_region"]
                elif config["most_impacted_region"] is not None:
                    self.most_impacted_region = common.MostImpactedRegion(config["most_impacted_region"])
                else:
                    self.most_impacted_region = None
            else:
                self.most_impacted_region = None

            if "stats" in config:
                if isinstance(config["stats"], Stats):
                    self.stats = config["stats"]
                elif config["stats"] is not None:
                    self.stats = Stats(config["stats"])
                else:
                    self.stats = None
            else:
                self.stats = None
        else:
            self.id = None
            self.name = None
            self.score = None
            self.most_impacted_region = None
            self.stats = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "most_impacted_region": self.most_impacted_region,
            "stats": self.stats,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class Stats(ZscalerObject):
    """
    A class for Stats objects.
    """

    def __init__(self, config=None):
        """
        Initialize the Stats model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.active_users = config["active_users"] if "active_users" in config else None
            self.active_devices = config["active_devices"] if "active_devices" in config else None
            self.num_poor = config["num_poor"] if "num_poor" in config else None
            self.num_okay = config["num_okay"] if "num_okay" in config else None
            self.num_good = config["num_good"] if "num_good" in config else None
        else:
            self.active_users = None
            self.active_devices = None
            self.num_poor = None
            self.num_okay = None
            self.num_good = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "active_users": self.active_users,
            "active_devices": self.active_devices,
            "num_poor": self.num_poor,
            "num_okay": self.num_okay,
            "num_good": self.num_good,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationScoreTrend(ZscalerObject):
    """
    A class for ApplicationScoreTrend objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ApplicationScoreTrend model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.metric = config["metric"] if "metric" in config else None
            self.unit = config["unit"] if "unit" in config else None

            self.datapoints = ZscalerCollection.form_list(
                config["datapoints"] if "datapoints" in config else [], common.DataPoints
            )
        else:
            self.metric = None
            self.unit = None
            self.datapoints = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "metric": self.metric,
            "unit": self.unit,
            "datapoints": self.datapoints,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class ApplicationMetrics(ZscalerObject):
    """
    A class for ApplicationMetrics objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ApplicationMetrics model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.metric = config["metric"] if "metric" in config else None
            self.unit = config["unit"] if "unit" in config else None

            self.datapoints = ZscalerCollection.form_list(
                config["datapoints"] if "datapoints" in config else [], common.DataPoints
            )
        else:
            self.metric = None
            self.unit = None
            self.datapoints = []

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "metric": self.metric,
            "unit": self.unit,
            "datapoints": self.datapoints,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
