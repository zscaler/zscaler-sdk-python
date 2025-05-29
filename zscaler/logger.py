import logging
import json as jsonp
import os
import time
from urllib.parse import urlencode
from http.client import HTTPConnection

LOG_FORMAT = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"


def setup_logging(logger_name="zscaler-sdk-python", enabled=None, verbose=None):
    """
    Set up logging with specified level and logger name.
    Log level is controlled via ZSCALER_SDK_VERBOSE environment variable.
    Logging can be enabled/disabled via ZSCALER_SDK_LOG environment variable.

    Parameters:
    - logger_name (str, optional): Logger name. Defaults to "zscaler-sdk-python".
    - enabled (bool, optional): Enable logging. Defaults to None, which uses the environment variable.
    - verbose (bool, optional): Set verbose logging. Defaults to None, which uses the environment variable.
    """
    if enabled is None:
        enabled = os.getenv("ZSCALER_SDK_LOG", "false").lower() == "true"

    if not enabled:
        # If logging is not enabled, set up a null handler
        # logging.disable(logging.INFO)
        logging.getLogger(logger_name).addHandler(logging.NullHandler())
        return

    if verbose is None:
        verbose = os.getenv("ZSCALER_SDK_VERBOSE", "false").lower() == "true"

    log_level = logging.DEBUG if verbose else logging.INFO
    HTTPConnection.debuglevel = 0
    # Create a logger with the specified name
    logger = logging.getLogger(logger_name)
    default_logger = logging.getLogger()

    # If the logger already has handlers, remove them to avoid duplicate logging
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    for handler in default_logger.handlers[:]:
        default_logger.removeHandler(handler)

    # Set log level
    logger.setLevel(log_level)
    default_logger.setLevel(log_level)
    logging.basicConfig(level=log_level)
    # Create a stream handler with the specified level and formatter
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    log_formatter = logging.Formatter(LOG_FORMAT)
    stream_handler.setFormatter(log_formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    # Option: Add FileHandler if you want logs to be written to a file.
    if os.getenv("LOG_TO_FILE", "false").lower() == "true":
        file_handler = logging.FileHandler(os.getenv("LOG_FILE_PATH", "sdk.log"))
        file_handler.setLevel(log_level)
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)


def dump_request(logger, url: str, method: str, json, params, headers, request_uuid: str, body=True):
    request_headers_filtered = {key: value for key, value in headers.items() if key != "Authorization"}
    # Log the request details before sending the request
    log_lines = []
    request_body = ""
    if body:
        request_body = jsonp.dumps(json)
    log_lines.append(f"\n---[ ZSCALER SDK REQUEST | ID:{request_uuid} ]-------------------------------")
    full_url = url
    if params:
        full_url += "?" + urlencode(params)
    log_lines.append(f"{method} {full_url}")
    for key, value in request_headers_filtered.items():
        log_lines.append(f"{key}: {value}")
    if body and request_body != "" and request_body != "null":
        log_lines.append(f"\n{request_body}")
    log_lines.append("--------------------------------------------------------------------")
    logger.info("\n".join(log_lines))


def dump_response(
    logger,
    url: str,
    method: str,
    resp,
    params,
    request_uuid: str,
    start_time,
    from_cache: bool = None,
):
    # Calculate the duration in seconds
    end_time = time.time()
    duration_seconds = end_time - start_time
    # Convert the duration to milliseconds
    duration_ms = duration_seconds * 1000
    # Convert the headers to a regular dictionary
    response_headers_dict = dict(resp.headers)
    full_url = url
    if params:
        full_url += "?" + urlencode(params)
    log_lines = []

    if from_cache:
        log_lines.append(
            f"\n---[ ZSCALER SDK RESPONSE | ID:{request_uuid} | " f"FROM CACHE | DURATION:{duration_ms}ms ]" + "-" * 31
        )
    else:
        log_lines.append(f"\n---[ ZSCALER SDK RESPONSE | ID:{request_uuid} | " f"DURATION:{duration_ms}ms ]" + "-" * 46)
    log_lines.append(f"{method} {full_url}")
    for key, value in response_headers_dict.items():
        log_lines.append(f"{key}: {value}")
    response_body = ""
    if resp.text:
        response_body = resp.text
    if response_body and response_body != "" and response_body != "null":
        log_lines.append(f"\n{response_body}")
    log_lines.append("-" * 68)
    logger.info("\n".join(log_lines))