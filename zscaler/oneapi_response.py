from typing import Dict, List, Any, Optional, Tuple, Union, Type
import json
import logging
import uuid
import requests
import jmespath

logger = logging.getLogger(__name__)


class ZscalerAPIResponse:
    """
    Class for defining the wrapper of a Zscaler API response.
    The user can check if more pages exist with `has_next()` and fetch them on-demand using `next()`.
    """

    SERVICE_PAGE_LIMITS = {
        "zpa": {"default": 100, "max": 500},
        "zia": {"default": 500, "max": 10000},
        "zdx": {"default": 10, "min": 1},
    }

    def __init__(
        self,
        request_executor: "RequestExecutor",
        req: Dict[str, Any],
        service_type: str,
        res_details: Optional[requests.Response] = None,
        response_body: str = "",
        data_type: Optional[Type] = None,
        all_entries: bool = False,
        sort_order: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_dir: Optional[str] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> None:
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
        self._next_offset = None
        self._list = []
        self._is_flat_list_response = False

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

        if self._service_type == "zia":
            # Normalize page_size → pageSize if still in snake_case
            if "page_size" in self._params:
                self._params["pageSize"] = self._params.pop("page_size")
            # If user supplied pageNumber, initialize self._page accordingly
            if "pageNumber" in self._params:
                try:
                    self._page = int(self._params["pageNumber"])
                except Exception:
                    self._page = 1
            self._params.pop("page", None)

        # Resolve the user-supplied page size from the correct param key per service.
        # ZIA uses "pageSize"; ZPA uses "pagesize"; others use "limit".
        raw_page_size = self._params.get("pageSize") or self._params.get("pagesize") or self._params.get("limit")
        self._limit = self.validate_page_size(raw_page_size, service_type)

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

    def validate_page_size(self, page_size: Optional[int], service_type: str) -> Optional[int]:
        """
        Validates the page size if provided by the user.
        Returns None if no page_size provided - let the API use its own default.
        """
        if page_size is None:
            # Don't set any default - let the API use its own default behavior
            logger.debug("No page size provided - letting API use its default")
            return None

        limits = self.SERVICE_PAGE_LIMITS.get(service_type, {})
        max_page_size = limits.get("max", 100)
        min_page_size = limits.get("min", 1)

        validated_size = min(max(int(page_size), min_page_size), max_page_size)
        logger.debug("Validated page size: %d (user provided: %s)", validated_size, page_size)
        return validated_size

    def get_headers(self) -> Dict[str, Any]:
        """
        Returns the response body of the Zscaler API Response.

        Returns:
            CIMultiDictProxy: dict-like object
        """
        logger.debug("Fetching response headers")
        return self._resp_headers

    def get_body(self) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """
        Returns the response body of the Zscaler API Response.

        Returns:
            dict: Dictionary format of response
        """
        return self._body

    def get_status(self) -> Optional[int]:
        """
        Returns HTTP Status Code of response

        Returns:
            int: HTTP Code
        """
        logger.debug("Fetching response status code: %s", self._status)
        return self._status

    def _build_json_response(self, response_body: str) -> None:
        """
        Converts JSON response text into Python dictionary.

        Args:
            response_body (str): Response text
        """
        self._body = json.loads(response_body)

        if isinstance(self._body, list):
            self._list = self._body

            # ZIA returns flat JSON arrays for paginated list endpoints.
            # Do NOT mark those as flat-list (non-paginated); let the
            # page-size heuristic in _has_next() drive pagination instead.
            if self._service_type == "zia":
                self._is_flat_list_response = False
            else:
                self._is_flat_list_response = True

            if self._body and len(self._body) > 0 and not isinstance(self._body[0], dict):
                pass
            elif self._body and len(self._body) > 0:
                cleaned_list = []
                for item in self._list:
                    if isinstance(item, dict):
                        cleaned_list.append(item)
                    else:
                        logger.warning("Non-dict item found in response list, skipping: %s", item)
                self._list = cleaned_list
        elif self._service_type == "zdx":
            self._list = self._body.get("items", [])
            self._next_offset = self._body.get("next_offset")
        elif self._service_type == "zidentity":
            # Zidentity uses "records" field for paginated responses
            self._list = self._body.get("records", [])
            self._next_link = self._body.get("next_link")
            self._prev_link = self._body.get("prev_link")
            self._results_total = self._body.get("results_total")
            self._page_offset = self._body.get("pageOffset")
            self._page_size = self._body.get("pageSize")
        elif self._service_type == "zeasm":
            # ZEASM uses "results" field for paginated responses
            self._list = self._body.get("results", [])
            self._total_results = self._body.get("total_results", 0)
            self._next_page = self._body.get("next_page")
            self._prev_page = self._body.get("prev_page")
        elif self._service_type == "zcc":
            # ZCC can return either a single object or a list of objects
            if isinstance(self._body, dict):
                self._list = [self._body]
            else:
                self._list = self._body if isinstance(self._body, list) else []
        elif self._service_type == "bi":
            # ZBI list reports returns {"reportType": "...", "reports": [...]}
            # Custom apps and report configs return flat lists (handled above)
            self._list = self._body.get("reports", [])
            logger.debug("ZBI response: extracted %d reports from 'reports' key", len(self._list))
        elif self._service_type == "ztb":
            # ZTB wraps most responses in {"result": {...}}
            # For list endpoints the items live inside result (e.g. result.alarms)
            # Some endpoints (e.g. api-key-auth/list) return {"count": N, "rows": [...]} directly
            result = self._body.get("result", {})
            if isinstance(result, dict) and result:
                items = []
                for key, val in result.items():
                    if isinstance(val, list):
                        items = val
                        break
                self._list = items
            elif isinstance(result, list):
                self._list = result
            else:
                # Fallback: look for any list field directly in the body (e.g. "rows")
                items = []
                for key, val in self._body.items():
                    if isinstance(val, list):
                        items = val
                        break
                self._list = items
        else:
            # ZPA and possibly other services use a dict with "list" field
            self._list = self._body.get("list", [])
            if self._service_type == "zpa":
                self._total_pages = int(self._body.get("totalPages", 1))
                self._total_count = int(self._body.get("totalCount", 0))

        # Only apply cleaning logic if we haven't already handled it above
        if not isinstance(self._body, list):
            cleaned_list = []
            for item in self._list:
                if isinstance(item, dict):
                    cleaned_list.append(item)
                else:
                    logger.warning("Non-dict item found in response list, skipping: %s", item)
            self._list = cleaned_list

        self._items_fetched += len(self._list)
        self._pages_fetched += 1

    def get_results(self) -> List[Any]:
        """
        Returns the current page of results.
        The initial call to the API returns only one page.
        """
        logger.debug("Fetching current page results")

        if self._service_type == "zcc" and self._type:
            try:
                return [self._type(item) for item in self._list if isinstance(item, dict)]
            except Exception as wrap_error:
                logger.warning(f"Failed to wrap results with {self._type}: {wrap_error}")
                return self._list

        return self._list

    def search(self, expression: str) -> List[Any]:
        """
        Applies a JMESPath expression to the current page of results for
        client-side filtering and projection.

        The expression is first evaluated against the full response body
        (useful for expressions that reference top-level keys, e.g.
        ``"users[?name=='Alice']"``).  If the body is a plain list, the
        expression is applied directly to the list instead.

        Args:
            expression: A JMESPath expression string.

        Returns:
            A list of matching items (or projected dicts/values).  Returns
            an empty list when nothing matches.

        Raises:
            jmespath.exceptions.ParseError: If *expression* is not valid
                JMESPath syntax.

        Examples:
            >>> items, resp, err = client.zia.user_management.list_users()
            >>> admins = resp.search("[?adminUser==`true`]")

            >>> items, resp, err = client.zdx.software.list_inventory()
            >>> zscaler = resp.search(
            ...     "items[?vendor=='Zscaler'].{name: software_name}"
            ... )
        """
        compiled = jmespath.compile(expression)

        # Apply against the full body first (handles expressions that target
        # a named key inside the response envelope, e.g. "reports[?x>1]").
        target = self._body if self._body is not None else self._list
        result = compiled.search(target)

        if result is None:
            return []
        if isinstance(result, list):
            return result
        return [result]

    def has_next(self) -> bool:
        """
        Returns True if there are more pages to fetch, False otherwise.

        Returns:
            bool: Existence of next page of results
        """
        return self._has_next()

    def next(self) -> Tuple[Optional[List[Any]], "ZscalerAPIResponse", Optional[Exception]]:
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

    def _fetch_next_page(self) -> Tuple[List[Any], Optional[Exception]]:
        logger.debug(f"[DEBUG] _fetch_next_page called. service_type={self._service_type}, params={self._params}")
        if not self._has_next():
            logger.debug("No more pages to fetch")
            return [], None

        if self._service_type == "zdx":
            logger.debug("[DEBUG] Taking ZDX pagination branch.")
            self._params["offset"] = self._next_offset
        elif self._service_type == "zia":
            logger.debug("[DEBUG] Taking ZIA pagination branch.")
            self._page += 1
            self._params["page"] = self._page
            # Only set pageSize if user explicitly provided it (don't override API defaults)
            if self._limit and "pageSize" not in self._params:
                self._params["pageSize"] = self._limit
            logger.debug(f"[DEBUG] _fetch_next_page params for ZIA: {self._params}")
        elif self._service_type == "zidentity":
            logger.debug("[DEBUG] Taking ZIDENTITY pagination branch.")
            # For Zidentity, use the next_link URL directly
            if self._next_link:
                # Parse the next_link URL to extract parameters
                from urllib.parse import urlparse, parse_qs

                parsed_url = urlparse(self._next_link)
                query_params = parse_qs(parsed_url.query)
                # Update params with the next page parameters
                for key, value in query_params.items():
                    self._params[key] = value[0] if len(value) == 1 else value
                # Update the URL to the base URL (remove the full next_link)
                self._url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            logger.debug(f"[DEBUG] _fetch_next_page params for ZIDENTITY: {self._params}")
        else:
            logger.debug("[DEBUG] Taking ZPA/other pagination branch.")
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

    def _has_next(self) -> bool:
        # If the response was a flat list (no pagination metadata), there are no more pages
        # This handles ZIA endpoints that return all results in a single response
        if self._is_flat_list_response:
            logger.debug("Has next page: False (flat list response - all results returned in single response)")
            return False

        if self._service_type == "zpa":
            has_next = self._page < self._total_pages
            logger.debug("Has next page for ZPA: %s (page %d of %d)", has_next, self._page, self._total_pages)
            return has_next
        elif self._service_type == "zdx":
            has_next = self._next_offset is not None
            logger.debug("Has next page for ZDX: %s", has_next)
            return has_next
        elif self._service_type == "zidentity":
            # More pages if next_link is not None
            has_next = self._next_link is not None
            logger.debug("Has next page for ZIDENTITY: %s", has_next)
            return has_next
        elif self._service_type == "bi":
            # ZBI endpoints return all results in a single response
            return False
        else:
            # For ZIA/ZCC with paginated responses (dict with "list" field):
            # - If we're on the first page and got results, try next page
            # - If we're on a subsequent page and the last fetch returned results equal to or greater than limit, try next page
            # - If the last fetch returned fewer results than limit (or 0), we're done
            if self._pages_fetched == 1:
                # First page - continue if we got any results
                has_next = bool(self._list)
            else:
                # Subsequent pages - if no explicit limit, use heuristic based on results returned
                # If we got results, try one more page. The next call will return empty and stop.
                # If user provided limit, only continue if last page was "full"
                if self._limit:
                    has_next = len(self._list) >= self._limit
                else:
                    # No explicit limit set - assume more pages exist if we got results
                    # This may result in one extra empty API call, but respects API defaults
                    has_next = bool(self._list)

            logger.debug(
                "Has next page for ZIA/ZCC: %s (page %d, items fetched: %d, limit: %s)",
                has_next,
                self._page,
                len(self._list),
                self._limit,
            )
            return has_next

    def __str__(self) -> str:
        try:
            return json.dumps(self.get_results(), indent=2)
        except Exception as e:
            return f"<ZscalerAPIResponse error displaying results: {e}>"
