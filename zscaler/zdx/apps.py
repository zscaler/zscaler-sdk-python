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

from zscaler.api_client import APIClient
from zscaler.request_executor import RequestExecutor
from zscaler.zdx.models.applications import ActiveApplications
from zscaler.zdx.models.applications import ApplicationScore
from zscaler.zdx.models.applications import ApplicationScoreTrend
from zscaler.zdx.models.applications import ApplicationMetrics
from zscaler.zdx.models.users import UserDetails
from zscaler.zdx.models.application_users import ApplicationUserDetails
from zscaler.utils import format_url, zdx_params


class AppsAPI(APIClient):

    def __init__(self, request_executor):
        super().__init__()
        self._request_executor: RequestExecutor = request_executor
        self._zdx_base_endpoint = "/zdx/v1"

    @zdx_params
    def list_apps(self, query_params=None) -> tuple:
        """
        Returns a list of all active applications configured within the ZDX tenant.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.location_id]`` {list}: The unique ID for the location.

                ``[query_params.department_id]`` {list}: The unique ID for the department.

                ``[query_params.geo_id]`` {list}: The unique ID for the geolocation.

        Returns:
            :obj:`Tuple`: The list of applications in ZDX.

        Examples:
            List all applications in ZDX for the past 2 hours:

            >>> app_list, _, err = client.zdx.apps.list_apps()
            ... if err:
            ...     print(f"Error listing applications: {err}")
            ...     return
            ... for app in app_list:
            ...     print(app.as_dict())

            List applications in ZDX for a specific time frame:

            >>> app_list, _, err = client.zdx.apps.list_apps(
            ... query_params={'since': 10, 'location_id': [545845]})
            ... if err:
            ...     print(f"Error listing applications: {err}")
            ...     return
            ... for app in app_list:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /apps
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = []
            for item in response.get_results():
                result.append(ActiveApplications(self.form_response_body(item)))
        except Exception as error:
            return (None, response, error)
        return (result, response, None)

    @zdx_params
    def get_app(self, app_id: str, query_params=None) -> tuple:
        """
        Returns information on the application's ZDX Score (for the previous 2 hours).
        Including most impacted locations, and the total number of users impacted.

        Args:
            app_id (str): The unique ID for the ZDX application.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.location_id]`` {list}: The unique ID for the location.

                ``[query_params.department_id]`` {list}: The unique ID for the department.

                ``[query_params.geo_id]`` {list}: The unique ID for the geolocation.

        Returns:
            :obj:`Tuple`: The application information.

        Examples:
            Return information on the application with the ID of 999999999:

            >>> apps, _, err = client.zdx.apps.get_app('1')
            ... if err:
            ...      print(f"Error listing application: {err}")
            ...     return
            ... for app in apps:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /apps/{app_id}
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [ApplicationScore(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_app_score(self, app_id: str, query_params=None) -> tuple:
        """
        Returns the ZDX score trend for the specified application configured within the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.location_id]`` {list}: The unique ID for the location.

                ``[query_params.department_id]`` {list}: The unique ID for the department.

                ``[query_params.geo_id]`` {list}: The unique ID for the geolocation.

        Returns:
            :obj:`Tuple`: The application's ZDX score trend.

        Examples:
            Return the ZDX score trend for the application with the ID of 999999999:

            >>> app_score, _, err = client.zdx.apps.get_app_score('1')
            ... if err:
            ...     print(f"Error listing application score: {err}")
            ...     return
            ... for app in app_score:
            ...     print(app.as_dict())

            Return the ZDX score trend for the application with the ID of 999999999 and location_id 125584:

            >>> app_score, _, err = client.zdx.apps.get_app_score(
            ... '999999999', query_params={"location_id": [125584]})
            ... if err:
            ...     print(f"Error listing application score: {err}")
            ...     return
            ... for app in app_score:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /apps/{app_id}/score
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [ApplicationScoreTrend(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_app_metrics(self, app_id: str, query_params=None) -> tuple:
        """
        Returns the ZDX metrics for the specified application configured within the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.location_id]`` {list}: The unique ID for the location.

                ``[query_params.department_id]`` {list}: The unique ID for the department.

                ``[query_params.geo_id]`` {list}: The unique ID for the geolocation.

                ``[query_params.metric_name]`` {str}: The name of the metric to return. Available values are:
                    * `pft` - Page Fetch Time
                    * `dns` - DNS Time
                    * `availability`

        Returns:
            :obj:`Tuple`: The application's ZDX metrics.

        Examples:
            Return the ZDX metrics for the application with the ID of 999999999:

            >>> app_avg, _, err = client.zdx.apps.get_app_metrics(app_id='999999999')
            ... if err:
            ...     print(f"Error listing application metric: {err}")
            ...     return
            ... for app in app_avg:
            ...     print(app.as_dict())

            Return the ZDX metrics for the app with an ID of 999999999 for the last 24 hours, including dns matrics,
            geolocation, department and location IDs:

            >>> app_avg, _, err = client.zdx.apps.get_app_metrics(
            ...    app_id='999999999', query_params={"since": '24', 'metric_name': 'dns', location_id=['888888888']})
            ... if err:
            ...     print(f"Error listing application metric: {err}")
            ...     return
            ... for app in app_avg:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /apps/{app_id}/metrics
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [ApplicationMetrics(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def list_app_users(self, app_id: str, query_params=None) -> tuple:
        """
        Returns a list of users and devices that were used to access the specified application configured within
        the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

                ``[query_params.location_id]`` {list}: The unique ID for the location.

                ``[query_params.department_id]`` {list}: The unique ID for the department.

                ``[query_params.geo_id]`` {list}: The unique ID for the geolocation.

                ``[query_params.score_bucket]`` {str}: The ZDX score bucket to filter by. Available values are:
                    * `poor` - 0-33
                    * `okay` - 34-65
                    * `good` - 66-100

        Returns:
            :obj:`Tuple`: The list of users and devices used to access the application.

        Examples:
            Return a list of users and devices who have accessed the application with the ID of 999999999:

            >>> app_users, _, err = client.zdx.apps.list_app_users('999999999')
            ... if err:
            ...     print(f"Error listing app users: {err}")
            ...     return
            ... for app in app_users:
            ...     print(app.as_dict())

            Return a list of users and devices who have accessed the application with the ID of 999999999
            with score_bucket of poor:

            >>> app_users, _, err = client.zdx.apps.list_app_users('999999999', query_params={"score_bucket": poor})
            ... if err:
            ...     print(f"Error listing app users: {err}")
            ...     return
            ... for app in app_users:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /apps/{app_id}/users
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        # try:
        #     result = [ApplicationUsers(
        #         self.form_response_body(response.get_body()))]
        # except Exception as error:
        #     return (None, response, error)

        # return (result, response, None)
        try:
            parsed_response = self.form_response_body(response.get_body())
            users_list = parsed_response.get("users", [])
            result = [UserDetails(user) for user in users_list]

        except Exception as error:
            return (None, response, error)

        return (result, response, None)

    @zdx_params
    def get_app_user(self, app_id: str, user_id: str, query_params=None) -> tuple:
        """
        Returns information on the specified user and device that was used to access the specified application
        configured within the ZDX tenant.

        Args:
            app_id (str): The unique ID for the ZDX application.
            user_id (str): The unique ID for the ZDX user.

        Keyword Args:
            query_params {dict}: Map of query parameters for the request.

                ``[query_params.since]`` {int}: The number of hours to look back for devices.

        Returns:
            :obj:`Tuple`: The user and device information.

        Examples:
            Return information on the user with the ID of 24328827 who has accessed the application with the ID of
            888888888:

            >>> app_list, _, err = client.zdx.apps.get_app_user(app_id='1', user_id='24328827')
            ... if err:
            ...     print(f"Error listing application user details: {err}")
            ...     return
            ... for app in app_list:
            ...     print(app.as_dict())

            Return information on the application ID 1 and user with the ID of 24328827 for the past 2 hours.

            >>> app_list, _, err = client.zdx.apps.get_app_user(
            ...    app_id='1', user_id='24328827', query_params={"since": 2})
            ... if err:
            ...     print(f"Error listing application user details: {err}")
            ...     return
            ... for app in app_list:
            ...     print(app.as_dict())
        """
        http_method = "get".upper()
        api_url = format_url(
            f"""
            {self._zdx_base_endpoint}
            /apps/{app_id}/users/{user_id}
        """
        )

        query_params = query_params or {}

        body = {}
        headers = {}

        request, error = self._request_executor.create_request(http_method, api_url, body, headers, params=query_params)

        if error:
            return (None, None, error)

        response, error = self._request_executor.execute(request)
        if error:
            return (None, response, error)

        try:
            result = [ApplicationUserDetails(self.form_response_body(response.get_body()))]
        except Exception as error:
            return (None, response, error)

        return (result, response, None)
