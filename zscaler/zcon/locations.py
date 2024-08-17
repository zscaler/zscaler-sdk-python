# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from box import Box, BoxList

from zscaler.utils import Iterator, convert_keys
from zscaler.zcon import ZCONClient


class LocationAPI:
    def __init__(self, client: ZCONClient):
        self.rest = client

    def list_location_templates(self, **kwargs) -> BoxList:
        """
        List all existing location templates.

        Args:
            **kwargs: Optional keyword args to filter the results.

        Keyword Args:
            page (int): The page number to return.
            page_size (int): The number of items to return per page.

        Returns:
            :obj:`BoxList`: The list of location templates.

        Examples:
            List all location templates::

                for template in zcon.locations.list_location_templates():
                    print(template)

        """
        return self.rest.get("locationTemplate", params=kwargs)

    def get_location_template(self, template_id: str) -> Box:
        """
        Get details for a specific location template.

        Args:
            template_id (str): The ID of the location template to retrieve.

        Returns:
            :obj:`Box`: The location template details.

        Examples:
            Get details of a specific location template::

                print(zcon.locations.get_location_template("123456789"))

        """
        return self.rest.get(f"locationTemplate/{template_id}")

    def add_location_template(self, name: str, template: dict = None, **kwargs) -> Box:
        """
        Add a new location template.

        Args:
            name (str): The name of the location template.
            template (dict, optional): A dictionary containing the template settings. Possible keys include:

                - ``template_prefix`` (str): Prefix of Cloud & Branch Connector location template.
                - ``xff_forward_enabled`` (bool): Enable to use the X-Forwarded-For headers.
                - ``auth_required`` (bool): Enable if "Authentication Required" is needed.
                - ``caution_enabled`` (bool): Enable to display an end user notification for unauthenticated traffic.
                - ``aup_enabled`` (bool): Enable to display an Acceptable Use Policy (AUP) for unauthenticated traffic.
                - ``aup_timeout_in_days`` (int): Frequency in days for displaying the AUP, if enabled.
                - ``ofw_enabled`` (bool): Enable the service's firewall controls.
                - ``ips_control`` (bool): Enable IPS controls, if firewall is enabled.
                - ``enforce_bandwidth_control`` (bool): Enable to specify bandwidth limits.
                - ``up_bandwidth`` (int): Upload bandwidth in Mbps, if bandwidth control is enabled.
                - ``dn_bandwidth`` (int): Download bandwidth in Mbps, if bandwidth control is enabled.
                - ``display_time_unit`` (str): Time unit for IP Surrogate idle time to disassociation.
                - ``idle_time_in_minutes`` (int): User mapping idle time in minutes for IP Surrogate.
                - ``surrogate_ip_enforced_for_known_browsers`` (bool): Enforce IP Surrogate for all known browsers.
                - ``surrogate_refresh_time_unit`` (str): Time unit for refresh time for re-validation of surrogacy.
                - ``surrogate_refresh_time_in_minutes`` (int): Refresh time in minutes for re-validation of surrogacy.
                - ``surrogate_ip`` (bool): Enable the IP Surrogate feature.

        Keyword Args:
            description (str): The description of the location template.

        Returns:
            :obj:`Box`: The location template details.

        Examples:
            Add a new location template with minimal settings::

                print(zcon.locations.add_location_template(name="MyTemplate"))

            Add a new location template with additional settings::

                template_settings = {
                    "surrogate_ip": True,
                    "surrogate_ip_enforced_for_known_browsers": False,
                    "template_prefix": "office",
                    "aup_enabled": True,
                    "aup_timeout_in_days": 30,
                    "ofw_enabled": True,
                    "idle_time_in_minutes": 35,
                    "auth_required": True,
                    "display_time_unit": "MINUTE",
                }
                print(zcon.locations.add_location_template(name="MyTemplate", template=template_settings))
        """
        # Rename 'description' to 'desc' if it exists
        if "description" in kwargs:
            kwargs["desc"] = kwargs.pop("description")

        payload = {"name": name, "template": template if template is not None else {}}

        # Add optional parameters to payload
        payload.update({k: v for k, v in kwargs.items() if v is not None})

        # Convert snake to camelcase
        payload = convert_keys(payload)

        return self.rest.post("locationTemplate", json=payload)

    def update_location_template(self, template_id: str, **kwargs) -> Box:
        """
        Update an existing location template.

        Args:
            template_id (str): The ID of the location template to update.

        Keyword Args:
            name (str): The name of the location template.
            description (str): A description for the location template.
            template (dict): A dictionary containing the template settings. Possible keys include:

                - ``template_prefix`` (str): Prefix of Cloud & Branch Connector location template.
                - ``xff_forward_enabled`` (bool): Enable to use the X-Forwarded-For headers.
                - ``auth_required`` (bool): Enable if "Authentication Required" is needed.
                - ``caution_enabled`` (bool): Enable to display an end user notification for unauthenticated traffic.
                - ``aup_enabled`` (bool): Enable to display an Acceptable Use Policy (AUP) for unauthenticated traffic.
                - ``aup_timeout_in_days`` (int): Frequency in days for displaying the AUP, if enabled.
                - ``ofw_enabled`` (bool): Enable the service's firewall controls.
                - ``ips_control`` (bool): Enable IPS controls, if firewall is enabled.
                - ``enforce_bandwidth_control`` (bool): Enable to specify bandwidth limits.
                - ``up_bandwidth`` (int): Upload bandwidth in Mbps, if bandwidth control is enabled.
                - ``dn_bandwidth`` (int): Download bandwidth in Mbps, if bandwidth control is enabled.
                - ``display_time_unit`` (str): Time unit for IP Surrogate idle time to disassociation.
                - ``idle_time_in_minutes`` (int): User mapping idle time in minutes for IP Surrogate.
                - ``surrogate_ip_enforced_for_known_browsers`` (bool): Enforce IP Surrogate for all known browsers.
                - ``surrogate_refresh_time_unit`` (str): Time unit for refresh time for re-validation of surrogacy.
                - ``surrogate_refresh_time_in_minutes`` (int): Refresh time in minutes for re-validation of surrogacy.
                - ``surrogate_ip`` (bool): Enable the IP Surrogate feature.

        Returns:
            :obj:`Box`: The updated location template details.

        Note:
            - Any provided keys will update existing keys.
            - The template dictionary does not support partial updates. Any provided template will completely overwrite
              the existing template.

        Examples:
            Update the name of a location template::

                print(zcon.locations.update_location_template(template_id="123456789", name="MyTemplate"))

            Update the template details of a location template::

                template_settings = {
                    "surrogate_ip": True,
                    "surrogate_ip_enforced_for_known_browsers": False,
                    "template_prefix": "office",
                    "aup_enabled": True,
                    "aup_timeout_in_days": 30,
                    "ofw_enabled": True,
                    "idle_time_in_minutes": 4,  # <-- changed to 4 hours
                    "auth_required": True,
                    "display_time_unit": "HOUR",  # <-- changed from minutes to hours
                }
                print(zcon.locations.update_location_template(template_id="123456789", template=template_settings))
        """

        # Rename 'description' to 'desc' if it exists
        if "description" in kwargs:
            kwargs["desc"] = kwargs.pop("description")

        # Retrieve existing location template
        payload = self.get_location_template(template_id)

        # Merge all kwargs into payload
        payload.update(kwargs)

        # Ensure the entire payload is converted to camelCase
        payload = convert_keys(payload)

        return self.rest.put(f"locationTemplate/{template_id}", json=payload)

    def delete_location_template(self, template_id: str):
        """
        Delete an existing location template.

        Args:
            template_id (str): The ID of the location template to delete.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            Delete a location template::

                print(zcon.locations.delete_location_template("123456789"))
        """
        return self.rest.delete(f"locationTemplate/{template_id}").status_code

    def list_locations(self, **kwargs) -> BoxList:
        """
        Returns a list of locations.

        Keyword Args:
            **auth_required (bool, optional):
                Filter based on whether the Enforce Authentication setting is enabled or disabled for a location.
            **bw_enforced (bool, optional):
                Filter based on whether Bandwith Control is being enforced for a location.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.
            **xff_enabled (bool, optional):
                Filter based on whether the Enforce XFF Forwarding setting is enabled or disabled for a location.

        Returns:
            :obj:`BoxList`: List of configured locations.

        Examples:
            List locations using default settings:

            >>> for location in zcon.locations.list_locations():
            ...    print(location)

            List locations, limiting to a maximum of 10 items:

            >>> for location in zcon.locations.list_locations(max_items=10):
            ...    print(location)

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zcon.locations.list_locations(page_size=200, max_pages=2):
            ...    print(location)

        """
        return BoxList(Iterator(self.rest, "location", **kwargs))

    def get_location(self, location_id: str) -> Box:
        """
        Get details for a specific location.

        Args:
            location_id (str): The ID of the location to retrieve.

        Returns:
            :obj:`Box`: The location details.

        Examples:
            Get details of a specific location::

                print(zcon.locations.get_location("123456789"))

        """
        return self.rest.get(f"location/{location_id}")

    def list_locations_lite(self, **kwargs) -> BoxList:
        """
        Returns only the name and ID of all configured locations.

        Keyword Args:
            **include_parent_locations (bool, optional):
                Only locations with sub-locations will be included in the response if `True`.
            **include_sub_locations (bool, optional):
                Sub-locations will be included in the response if `True`.
            **max_items (int, optional):
                The maximum number of items to request before stopping iteration.
            **max_pages (int, optional):
                The maximum number of pages to request before stopping iteration.
            **page_size (int, optional):
                Specifies the page size. The default size is 100, but the maximum size is 1000.
            **search (str, optional):
                The search string used to partially match against a location's name and port attributes.

        Returns:
            :obj:`BoxList`: A list of configured locations.

        Examples:
            List locations with default settings:

            >>> for location in zcon.locations.list_locations_lite():
            ...    print(location)

            List locations, limiting to a maximum of 10 items:

            >>> for location in zcon.locations.list_locations_lite(max_items=10):
            ...    print(location)

            List locations, returning 200 items per page for a maximum of 2 pages:

            >>> for location in zcon.locations.list_locations_lite(page_size=200, max_pages=2):
            ...    print(location)

        """
        return BoxList(Iterator(self.rest, "location/lite", **kwargs))
