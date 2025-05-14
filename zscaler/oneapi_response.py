import json
import logging
import uuid

logger = logging.getLogger(__name__)


class ZscalerAPIResponse:
    """
    Class for defining the wrapper of a Zscaler API response.
    Inspired by the Okta approach, this class only returns the initial page of results.
    The user can check if more pages exist with `has_next()` and fetch them on-demand using `next()`.
    """

    SERVICE_PAGE_LIMITS = {
        "ZPA": {"default": 100, "max": 500},
        "ZIA": {"default": 500, "max": 10000},
        "ZDX": {"default": 10, "min": 1},
    }

    def __init__(
        self,
        request_executor,
        req,
        service_type,
        res_details=None,
        response_body="",
        data_type=None,
        all_entries=False,
        sort_order=None,
        sort_by=None,
        sort_dir=None,
        start_time=None,
        end_time=None,
    ):
        self._url = req.get("url", None)
        self._headers = req.get("headers", {})
        self._params = req.get("params", {})
        self._resp_headers = res_details.headers if res_details and hasattr(res_details, "headers") else {}
        self._body = None
        self._type = data_type
        self._status = res_details.status_code if res_details and hasattr(res_details, "status_code") else None
        self._request_executor = request_executor

        # self._max_items = max_items
        # self._max_pages = max_pages
        self._page = 1
        self._items_fetched = 0
        self._pages_fetched = 0

        self._service_type = service_type
        self._offset = self._params.get("offset", 0)
        self._limit = self.validate_page_size(self._params.get("limit"), service_type)
        self._next_offset = None
        self._list = []

        if all_entries:
            self._params["allEntries"] = True
        if sort_order:
            self._params["sortOrder"] = sort_order
        if sort_by:
            self._params["sortBy"] = sort_by
        if sort_dir:
            self._params["sortDir"] = sort_dir
        if start_time:
            self._params["startTime"] = start_time
        if end_time:
            self._params["endTime"] = end_time

        # If service is ZPA and user did not specify a pagesize, set it to max=500 by default
        if self._service_type == "ZPA" and "pagesize" not in self._params:
            self._params["pagesize"] = self.SERVICE_PAGE_LIMITS["ZPA"]["max"]

        # If service is ZIA, ensure the pagination parameter is "pageSize" in camelCase
        if self._service_type == "ZIA":
            if "page_size" in self._params:
                self._params["pageSize"] = self._params.pop("page_size")

        if res_details:
            content_type = res_details.headers.get("Content-Type", "").lower()

            if "application/json" in content_type:
                try:
                    self._build_json_response(response_body)
                except (json.JSONDecodeError, AttributeError, TypeError):
                    # Fallback if body is not JSON object or list (e.g., int or plain string)
                    self._body = response_body
                    self._list = []
            else:
                # Attempt JSON parse, else store as raw text
                try:
                    self._build_json_response(response_body)
                except (json.JSONDecodeError, AttributeError, TypeError):
                    self._body = response_body
                    self._list = []

    def validate_page_size(self, page_size, service_type):
        limits = self.SERVICE_PAGE_LIMITS.get(service_type, {})
        max_page_size = limits.get("max", 100)
        default_page_size = limits.get("default", 20)

        if page_size is None:
            return default_page_size
        validated_size = min(max(int(page_size), limits.get("min", 1)), max_page_size)
        logger.debug("Validated page size: %d", validated_size)
        return validated_size

    def get_headers(self):
        """
        Returns the response body of the Okta API Response.

        Returns:
            CIMultiDictProxy: dict-like object
        """
        logger.debug("Fetching response headers")
        return self._resp_headers

    def get_body(self):
        """
        Returns the response body of the Okta API Response.

        Returns:
            dict: Dictionary format of response
        """
        return self._body

    def get_status(self):
        """
        Returns HTTP Status Code of response

        Returns:
            int: HTTP Code
        """
        logger.debug("Fetching response status code: %s", self._status)
        return self._status

    def _build_json_response(self, response_body):
        """
        Converts JSON response text into Python dictionary.

        Args:
            response_body (str): Response text
        """
        self._body = json.loads(response_body)

        if isinstance(self._body, list):
            # ZIA response may just be a list of items
            self._list = self._body
        elif self._service_type == "ZDX":
            self._list = self._body.get("items", [])
            self._next_offset = self._body.get("next_offset")
        else:
            # ZPA and possibly other services use a dict with "list" field
            self._list = self._body.get("list", [])
            if self._service_type == "ZPA":
                self._total_pages = int(self._body.get("totalPages", 1))
                self._total_count = int(self._body.get("totalCount", 0))

        cleaned_list = []
        for item in self._list:
            if isinstance(item, dict):
                cleaned_list.append(item)
            else:
                logger.warning("Non-dict item found in response list, skipping: %s", item)
        self._list = cleaned_list

        self._items_fetched += len(self._list)
        self._pages_fetched += 1
    
    def get_results(self):
        """
        Returns the current page of results.
        The initial call to the API returns only one page.
        """
        logger.debug("Fetching current page results")

        if self._service_type.upper() == "ZCC" and self._type:
            try:
                return [self._type(item) for item in self._list if isinstance(item, dict)]
            except Exception as wrap_error:
                logger.warning(f"Failed to wrap results with {self._type}: {wrap_error}")
                return self._list

        return self._list

    def has_next(self):
        """
        Returns True if there are more pages to fetch, False otherwise.

        Returns:
            bool: Existence of next page of results
        """
        return self._has_next()

    def next(self):
        if not self.has_next():
            raise StopIteration("No more pages available.")

        results, error = self._fetch_next_page()
        if error:
            return None, self, error
        if not results:
            return None, self, None

        if self._type:
            try:
                results = [self._type(item) for item in results if isinstance(item, dict)]
            except Exception as wrap_error:
                logger.warning(f"Failed to wrap pagination results with {self._type}: {wrap_error}")

        return results, self, None


    def _fetch_next_page(self):
        if not self._has_next():
            logger.debug("No more pages to fetch")
            return [], None

        if self._service_type == "ZDX":
            self._params["offset"] = self._next_offset
        else:
            self._page += 1
            self._params["page"] = self._page

        logger.debug(f"Requesting next page with params: {self._params}")

        req = {
            "method": "GET",
            "url": self._url,
            "headers": self._headers,
            "params": self._params,
            "uuid": uuid.uuid4(),
        }
        _, _, response_body, error = self._request_executor.fire_request(req)

        if error:
            logger.error(f"Error fetching the next page: {error}")
            return None, error

        self._build_json_response(response_body)
        return self._list, None

    def _has_next(self):

        if self._service_type == "ZPA":
            # More pages if current page < total_pages
            has_next = self._page < self._total_pages
            logger.debug("Has next page for ZPA: %s (page %d of %d)", has_next, self._page, self._total_pages)
            return has_next
        elif self._service_type == "ZDX":
            # More pages if next_offset is not None
            has_next = self._next_offset is not None
            logger.debug("Has next page for ZDX: %s", has_next)
            return has_next
        else:
            # For ZIA/ZCC, if we got results last time, assume we can try next page
            # If next page returns empty, has_next() will be False on next call.
            # This logic may need refinement depending on API behavior, but follows a pattern:
            #   If the previous page was not empty, we assume another page might exist.
            #   If next() returns empty, we won't continue.
            has_next = bool(self._list) and (self._pages_fetched == 1 or self._page < 9999999)
            # The above large number is a placeholder. Ideally, you'd base this on known API behavior.
            # If the API doesn't give a clear signal that there's another page, we may need a heuristic.
            logger.debug("Has next page for ZIA/ZCC: %s", has_next)
            return has_next
