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


class ConfigAudit(ZscalerObject):
    """
    A class for ConfigAudit objects.
    """

    def __init__(self, config=None):
        """
        Initialize the ConfigAudit model based on API response.

        Args:
            config (dict): A dictionary representing the configuration.
        """
        super().__init__(config)

        if config:
            self.overall_grade = config["overallGrade"] if "overallGrade" in config else None
            self.high_availability_grade = config["highAvailabilityGrade"] if "highAvailabilityGrade" in config else None
            self.user_performance_grade = config["userPerformanceGrade"] if "userPerformanceGrade" in config else None
            self.other_grade = config["otherGrade"] if "otherGrade" in config else None
            self.gre_tunnel_grade = config["greTunnelGrade"] if "greTunnelGrade" in config else None
            self.pac_file_grade = config["pacFileGrade"] if "pacFileGrade" in config else None
            self.auth_frequency_grade = config["authFrequencyGrade"] if "authFrequencyGrade" in config else None
            self.pacfile_size_grade = config["pacfileSizeGrade"] if "pacfileSizeGrade" in config else None
            self.office365_flag = config["office365Flag"] if "office365Flag" in config else None
            self.office365_grade = config["office365Grade"] if "office365Grade" in config else None
            self.ip_visibility_grade = config["ipVisibilityGrade"] if "ipVisibilityGrade" in config else None
            self.report_timestamp = config["reportTimestamp"] if "reportTimestamp" in config else None
            self.data_present = config["dataPresent"] if "dataPresent" in config else None
            self.gre_tunnel_recommended_configuration = (
                config["greTunnelRecommendedConfiguration"] if "greTunnelRecommendedConfiguration" in config else None
            )
            self.pac_file_recommended_configuration = (
                config["pacFileRecommendedConfiguration"] if "pacFileRecommendedConfiguration" in config else None
            )
            self.auth_frequency_recommended_configuration = (
                config["authFrequencyRecommendedConfiguration"] if "authFrequencyRecommendedConfiguration" in config else None
            )
            self.pac_file_size_recommended_configuration = (
                config["pacFileSizeRecommendedConfiguration"] if "pacFileSizeRecommendedConfiguration" in config else None
            )
            self.office365_recommended_configuration = (
                config["office365RecommendedConfiguration"] if "office365RecommendedConfiguration" in config else None
            )
            self.ip_visibility_recommended_configuration = (
                config["ipVisibilityRecommendedConfiguration"] if "ipVisibilityRecommendedConfiguration" in config else None
            )

            if "authFrequency" in config:
                if isinstance(config["authFrequency"], AuthFrequency):
                    self.auth_frequency = config["authFrequency"]
                elif config["authFrequency"] is not None:
                    self.auth_frequency = AuthFrequency(config["authFrequency"])
                else:
                    self.auth_frequency = None
            else:
                self.auth_frequency = None

        else:
            self.overall_grade = None
            self.high_availability_grade = None
            self.user_performance_grade = None
            self.other_grade = None
            self.gre_tunnel_grade = None
            self.pac_file_grade = None
            self.auth_frequency = None
            self.auth_frequency_grade = None
            self.pacfile_size_grade = None
            self.office365_flag = None
            self.office365_grade = None
            self.ip_visibility_grade = None
            self.report_timestamp = None
            self.data_present = None
            self.gre_tunnel_recommended_configuration = None
            self.pac_file_recommended_configuration = None
            self.auth_frequency_recommended_configuration = None
            self.pac_file_size_recommended_configuration = None
            self.office365_recommended_configuration = None
            self.ip_visibility_recommended_configuration = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "overallGrade": self.overall_grade,
            "highAvailabilityGrade": self.high_availability_grade,
            "userPerformanceGrade": self.user_performance_grade,
            "otherGrade": self.other_grade,
            "greTunnelGrade": self.gre_tunnel_grade,
            "pacFileGrade": self.pac_file_grade,
            "authFrequency": self.auth_frequency,
            "authFrequencyGrade": self.auth_frequency_grade,
            "pacfileSizeGrade": self.pacfile_size_grade,
            "office365Flag": self.office365_flag,
            "office365Grade": self.office365_grade,
            "ipVisibilityGrade": self.ip_visibility_grade,
            "reportTimestamp": self.report_timestamp,
            "dataPresent": self.data_present,
            "greTunnelRecommendedConfiguration": self.gre_tunnel_recommended_configuration,
            "pacFileRecommendedConfiguration": self.pac_file_recommended_configuration,
            "authFrequencyRecommendedConfiguration": self.auth_frequency_recommended_configuration,
            "pacFileSizeRecommendedConfiguration": self.pac_file_size_recommended_configuration,
            "office365RecommendedConfiguration": self.office365_recommended_configuration,
            "ipVisibilityRecommendedConfiguration": self.ip_visibility_recommended_configuration,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class AuthFrequency(ZscalerObject):
    """
    A class for AuthFrequency objects.
    """

    def __init__(self, config=None):
        """
        Initialize the AuthFrequency model based on API response.

        Args:
            config (dict): A dictionary representing the Auth Frequency configuration.
        """
        super().__init__(config)

        if config:
            self.auth_frequency = config["authFrequency"] if "authFrequency" in config else None
            self.auth_custom_frequency = config["authCustomFrequency"] if "authCustomFrequency" in config else None

        else:
            self.auth_frequency = None
            self.auth_custom_frequency = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "authFrequency": self.auth_frequency,
            "authCustomFrequency": self.auth_custom_frequency,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class IPVisibility(ZscalerObject):
    """
    A class for IPVisibility objects.
    """

    def __init__(self, config=None):
        """
        Initialize the IPVisibility model based on API response.

        Args:
            config (dict): A dictionary representing the IP Visibility configuration.
        """
        super().__init__(config)

        if config:
            self.total_gre_locations = config["totalGreLocations"] if "totalGreLocations" in config else None
            self.recommendation = config["recommendation"] if "recommendation" in config else None
            self.details = config["details"] if "details" in config else None
            self.locations_with_nat = ZscalerCollection.form_list(
                config["locationsWithNat"] if "locationsWithNat" in config else [], str
            )
        else:
            self.total_gre_locations = None
            self.recommendation = None
            self.locations_with_nat = None
            self.details = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "totalGreLocations": self.auth_frequency,
            "locationsWithNat": self.auth_frequency,
            "recommendation": self.auth_custom_frequency,
            "details": self.auth_custom_frequency,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PacFile(ZscalerObject):
    """
    A class for PacFile objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PacFile model based on API response.

        Args:
            config (dict): A dictionary representing the Pac File configuration.
        """
        super().__init__(config)

        if config:
            self.total_pac_files = config["totalPacFiles"] if "totalPacFiles" in config else None
            self.pac_with_static_ips = ZscalerCollection.form_list(
                config["pacWithStaticIPs"] if "pacWithStaticIPs" in config else [], PacWithStaticIPs
            )
        else:
            self.total_pac_files = None
            self.pac_with_static_ips = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "totalPacFiles": self.total_pac_files,
            "pacWithStaticIPs": self.pac_with_static_ips,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format


class PacWithStaticIPs(ZscalerObject):
    """
    A class for PacWithStaticIPs objects.
    """

    def __init__(self, config=None):
        """
        Initialize the PacFile model based on API response.

        Args:
            config (dict): A dictionary representing the Pac With Static IPs configuration.
        """
        super().__init__(config)

        if config:
            self.pac_file_name = config["pacFileName"] if "pacFileName" in config else None
            self.static_service_ips = ZscalerCollection.form_list(
                config["staticServiceIps"] if "staticServiceIps" in config else [], str
            )
            self.static_virtual_ips = ZscalerCollection.form_list(
                config["staticVirtualIps"] if "staticVirtualIps" in config else [], str
            )
        else:
            self.pac_file_name = None
            self.pac_with_static_ips = None
            self.static_service_ips = None
            self.static_virtual_ips = None

    def request_format(self):
        """
        Return the object as a dictionary in the format expected for API requests.
        """
        parent_req_format = super().request_format()
        current_obj_format = {
            "pacFileName": self.pac_file_name,
            "pacWithStaticIPs": self.pac_with_static_ips,
            "staticServiceIps": self.static_service_ips,
            "staticVirtualIps": self.static_virtual_ips,
        }
        parent_req_format.update(current_obj_format)
        return parent_req_format
