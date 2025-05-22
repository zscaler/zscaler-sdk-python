import requests
import logging
import os
import time
from zscaler.logger import dump_request, dump_response
from zscaler.zcc.legacy import LegacyZCCClientHelper
from zscaler.ztw.legacy import LegacyZTWClientHelper
from zscaler.zdx.legacy import LegacyZDXClientHelper
from zscaler.zpa.legacy import LegacyZPAClientHelper
from zscaler.zia.legacy import LegacyZIAClientHelper
from zscaler.zwa.legacy import LegacyZWAClientHelper
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class HTTPClient:
    """
    This class is the basic HTTPClient for the Zscaler Client.
    Custom HTTP clients should inherit from this class.
    """

    # raise_exception = False

    def __init__(
        self,
        http_config={},
        zcc_legacy_client: LegacyZCCClientHelper = None,
        ztw_legacy_client: LegacyZTWClientHelper = None,
        zdx_legacy_client: LegacyZDXClientHelper = None,
        zpa_legacy_client: LegacyZPAClientHelper = None,
        zia_legacy_client: LegacyZIAClientHelper = None,
        zwa_legacy_client: LegacyZWAClientHelper = None,
    ):

        # Get headers from Request Executor
        self._default_headers = http_config.get("headers", {})
        self.zcc_legacy_client = zcc_legacy_client
        self.ztw_legacy_client = ztw_legacy_client
        self.zdx_legacy_client = zdx_legacy_client
        self.zpa_legacy_client = zpa_legacy_client
        self.zia_legacy_client = zia_legacy_client
        self.zwa_legacy_client = zwa_legacy_client

        # Determine if legacy clients are enabled
        self.use_zcc_legacy_client = zcc_legacy_client is not None
        self.use_ztw_legacy_client = ztw_legacy_client is not None
        self.use_zdx_legacy_client = zdx_legacy_client is not None
        self.use_zpa_legacy_client = zpa_legacy_client is not None
        self.use_zia_legacy_client = zia_legacy_client is not None
        self.use_zwa_legacy_client = zwa_legacy_client is not None

        # Set timeout for all HTTP requests
        request_timeout = http_config.get("requestTimeout", None)
        self._timeout = request_timeout if request_timeout and request_timeout > 0 else None

        if "proxy" in http_config:
            self._proxy = self._setup_proxy(http_config["proxy"])
        else:
            self._proxy = None

        # Setup SSL context or handle disableHttpsCheck
        if "sslContext" in http_config:
            self._ssl_context = http_config["sslContext"]  # Use the custom SSL context
        elif "disableHttpsCheck" in http_config and http_config["disableHttpsCheck"]:
            self._ssl_context = False  # Disable SSL certificate validation if disableHttpsCheck is true
        else:
            self._ssl_context = True  # Enable SSL certificate validation by default

        self._session = None

    def _setup_proxy(self, proxy):
        return proxy if proxy else None

    def set_session(self, session):
        """Set Client Session to improve performance by reusing session.

        Session should be closed manually or within context manager.
        """
        self._session = session

    def close_session(self):
        """Closes the session if one was used."""
        if self._session:
            self._session.close()

    def send_request(self, request):
        try:
            logger.debug(f"Request: {request}")

            # Sanitize the authorization header before logging
            headers = request.get("headers", {}).copy()
            if "Authorization" in headers:
                headers["Authorization"] = "Bearer <TOKEN>"

            # Prepare request parameters
            params = {
                "method": request["method"],
                "url": request["url"],
                "headers": request.get("headers", {}),
                "timeout": self._timeout,
                "proxies": {"http": self._proxy, "https": self._proxy} if self._proxy else None,
                "verify": self._ssl_context,
            }

            # Handle payload
            if request.get("json"):
                params["json"] = request["json"]
            elif request.get("data"):
                params["data"] = request["data"]
            elif request.get("form"):
                params["data"] = request["form"]
            if request["params"]:
                params["params"] = request["params"]

            # Use Legacy Client if enabled
            if self.use_zpa_legacy_client:
                parsed_url = urlparse(request["url"])
                path = parsed_url.path
                logger.debug(f"Sending request via ZPA legacy client. Path: {path}")
                response, legacy_request = self.zpa_legacy_client.send(
                    method=request["method"],
                    path=path,
                    params=request["params"],
                    json=request.get("json") or request.get("data"),
                )

                logger.debug(f"ZPA Legacy Client Response: {response}, Legacy Request: {legacy_request}")

                if response is None:
                    # No response from legacy client: return (None, error)
                    error_msg = f"ZPA Legacy client returned None for request {legacy_request}"
                    logger.error(error_msg)
                    return (None, ValueError(error_msg))

                params.update(
                    {
                        "url": legacy_request["url"],
                        "params": legacy_request["params"],
                        "headers": legacy_request["headers"],
                    }
                )

            elif self.use_zcc_legacy_client:
                parsed_url = urlparse(request["url"])
                path = parsed_url.path
                logger.debug(f"Sending request via ZCC legacy client. Path: {path}")

                response, legacy_request = self.zcc_legacy_client.send(
                    method=request["method"],
                    path=path,
                    params=request["params"],
                    json=request.get("json") or request.get("data"),
                )

                logger.debug(f"ZCC Legacy Client Response: {response}, Legacy Request: {legacy_request}")

                if response is None:
                    error_msg = f"ZCC Legacy client returned None for request {legacy_request}"
                    logger.error(error_msg)
                    return (None, ValueError(error_msg))

                params.update(
                    {
                        "url": legacy_request["url"],
                        "params": legacy_request["params"],
                        "headers": legacy_request["headers"],
                    }
                )

            elif self.use_zdx_legacy_client:
                parsed_url = urlparse(request["url"])
                path = parsed_url.path
                logger.debug(f"Sending request via ZDX legacy client. Path: {path}")

                # Unpack the returned tuple into response and legacy_req_info
                response, legacy_req_info = self.zdx_legacy_client.send(
                    method=request["method"],
                    path=path,
                    params=request["params"],
                    json=request.get("json") or request.get("data"),
                )

                logger.debug(f"ZDX Legacy Client Response: {response}, Legacy Request Info: {legacy_req_info}")

                if response is None:
                    error_msg = f"ZDX Legacy client returned None for request {legacy_req_info}"
                    logger.error(error_msg)
                    return (None, ValueError(error_msg))

                # Update params with the correct dictionary from the legacy client's response
                params.update(
                    {
                        "url": legacy_req_info["url"],
                        "params": legacy_req_info["params"],
                        "headers": legacy_req_info["headers"],
                    }
                )

            elif self.use_zwa_legacy_client:
                parsed_url = urlparse(request["url"])
                path = parsed_url.path
                logger.debug(f"Sending request via ZWA legacy client. Path: {path}")

                # Unpack the returned tuple into response and legacy_req_info
                response, legacy_req_info = self.zwa_legacy_client.send(
                    method=request["method"],
                    path=path,
                    params=request["params"],
                    json=request.get("json") or request.get("data"),
                )

                logger.debug(f"ZWA Legacy Client Response: {response}, Legacy Request Info: {legacy_req_info}")

                if response is None:
                    error_msg = f"ZWA Legacy client returned None for request {legacy_req_info}"
                    logger.error(error_msg)
                    return (None, ValueError(error_msg))

                # Update params with the correct dictionary from the legacy client's response
                params.update(
                    {
                        "url": legacy_req_info["url"],
                        "params": legacy_req_info["params"],
                        "headers": legacy_req_info["headers"],
                    }
                )

            elif self.use_zia_legacy_client:
                parsed_url = urlparse(request["url"])
                path = parsed_url.path
                logger.debug(f"Sending request via ZIA legacy client. Path: {path}")

                response, legacy_request = self.zia_legacy_client.send(
                    method=request["method"],
                    path=path,
                    params=request["params"],
                    json=request.get("json") or request.get("data"),
                )

                logger.debug(f"ZIA Legacy Client Response: {response}, Legacy Request: {legacy_request}")

                if response is None:
                    error_msg = f"ZIA Legacy client returned None for request {legacy_request}"
                    logger.error(error_msg)
                    return (None, ValueError(error_msg))

                params.update(
                    {
                        "url": legacy_request["url"],
                        "params": legacy_request["params"],
                        "headers": legacy_request["headers"],
                    }
                )

            elif self.use_ztw_legacy_client:
                parsed_url = urlparse(request["url"])
                path = parsed_url.path
                logger.debug(f"Sending request via ZTW legacy client. Path: {path}")

                response, legacy_request = self.ztw_legacy_client.send(
                    method=request["method"],
                    path=path,
                    params=request["params"],
                    json=request.get("json") or request.get("data"),
                )

                logger.debug(f"ZTW Legacy Client Response: {response}, Legacy Request: {legacy_request}")

                if response is None:
                    error_msg = f"ZTW Legacy client returned None for request {legacy_request}"
                    logger.error(error_msg)
                    return (None, ValueError(error_msg))

                params.update(
                    {
                        "url": legacy_request["url"],
                        "params": legacy_request["params"],
                        "headers": legacy_request["headers"],
                    }
                )

            else:
                # Standard session
                if self._session:
                    logger.debug("Request with re-usable session.")
                    response = self._session.request(**params)
                else:
                    logger.debug("Request without re-usable session.")
                    response = requests.request(**params)

            if response is None:
                logger.error("Request execution failed. Response is None.")
                return (None, ValueError("No response received."))

            dump_request(
                logger,
                params["url"],
                params["method"],
                params.get("json"),
                params.get("params"),
                params.get("headers"),
                request["uuid"],
                body=not ("/zscsb" in request["url"]),
            )

            start_time = time.time()

            logger.info(f"Received response with status code: {response.status_code}")

            dump_response(
                logger,
                params["url"],
                params["method"],
                response,
                request.get("params"),
                request["uuid"],
                start_time,
            )
            # Return response and None even for 4xx/5xx – let check_response_for_error() decide
            return (response, None)

        except (requests.RequestException, requests.Timeout) as error:
            # Network-level errors
            logger.error(f"Request to {request['url']} failed: {error}")
            return (None, error)

        except Exception as error:
            # Unexpected errors
            # logger.error(f"Unexpected error during request execution: {error}")
            return (None, error)

    @staticmethod
    def format_binary_data(data):
        """Formats binary data for multipart uploads."""
        return data  # Requests will handle this directly, no need for aiohttp-specific formatting

    def _setup_proxy(self, proxy):
        """Sets up the proxy string from the configuration or environment variables."""
        proxy_string = ""

        if proxy is None:
            if "HTTP_PROXY" in os.environ:
                proxy_string = os.environ["HTTP_PROXY"]
            if "HTTPS_PROXY" in os.environ:
                proxy_string = os.environ["HTTPS_PROXY"]
            return proxy_string if proxy_string != "" else None

        host = proxy["host"]
        port = int(proxy["port"]) if "port" in proxy else ""

        if "username" in proxy and "password" in proxy:
            username = proxy["username"]
            password = proxy["password"]
            proxy_string = f"http://{username}:{password}@{host}"
        else:
            proxy_string = f"http://{host}"

        if port:
            proxy_string += f":{port}/"

        return proxy_string if proxy_string != "" else None
