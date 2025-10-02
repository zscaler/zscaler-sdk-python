import logging
import json as jsonp
import os
import time
from urllib.parse import urlencode
from http.client import HTTPConnection

LOG_FORMAT = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"

# Fields to sanitize in logs (case-insensitive matching)
SENSITIVE_FIELDS = {
    "password", "api_key", "apiKey", "apikey", 
    "clientSecret", "client_secret", "clientsecret",
    "authorization", "Authorization",
    "access_token", "accessToken", "accesstoken",
    "refresh_token", "refreshToken", "refreshtoken",
    "secret", "Secret",
    "privateKey", "private_key", "privatekey",
    "token", "Token",
    "key", "Key",
}

# Sensitive header keys (case-insensitive)
SENSITIVE_HEADERS = {
    "authorization", "x-api-key", "apikey", "api-key",
    "clientsecret", "client-secret", "access-token", 
    "refresh-token", "x-auth-token",
}


def _sanitize_for_logging(data):
    """
    Recursively mask sensitive fields in dicts/lists for logging.
    
    Args:
        data: The data structure to sanitize (dict, list, or other)
    
    Returns:
        Sanitized copy of the data with sensitive fields masked
    """
    if isinstance(data, dict):
        return {
            k: "***REDACTED***" if k in SENSITIVE_FIELDS or k.lower() in SENSITIVE_FIELDS 
            else _sanitize_for_logging(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [_sanitize_for_logging(item) for item in data]
    else:
        return data


def _sanitize_plaintext_for_logging(text):
    """
    Scan and mask sensitive keywords in plaintext strings.
    
    Args:
        text (str): Plain text that might contain sensitive data
    
    Returns:
        str: Text with sensitive patterns masked
    """
    import re
    
    if not isinstance(text, str):
        return text
    
    # Patterns to match common sensitive data formats in plain text
    # Match patterns like "password":"value", "password": "value", password=value, etc.
    patterns = [
        (r'("password"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("api_key"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("apiKey"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("clientSecret"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("client_secret"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("access_token"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("refresh_token"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("token"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("secret"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
        (r'("privateKey"\s*:\s*")[^"]*(")', r'\1***REDACTED***\2'),
    ]
    
    sanitized_text = text
    for pattern, replacement in patterns:
        sanitized_text = re.sub(pattern, replacement, sanitized_text, flags=re.IGNORECASE)
    
    return sanitized_text


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
    # Mask sensitive header values (e.g., Authorization, X-Api-Key, etc.)
    request_headers_filtered = {
        key: "***REDACTED***" if key.lower() in SENSITIVE_HEADERS else value 
        for key, value in headers.items()
    }
    
    # Log the request details before sending the request
    log_lines = []
    request_body = ""
    if body and json:
        # Sanitize request body before logging
        sanitized_json = _sanitize_for_logging(json)
        request_body = jsonp.dumps(sanitized_json)
    
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
    
    # Mask sensitive headers in response
    response_headers_dict = {
        key: "***REDACTED***" if key.lower() in SENSITIVE_HEADERS else value
        for key, value in dict(resp.headers).items()
    }
    
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
        # Try to sanitize response body if it's JSON
        try:
            parsed_body = jsonp.loads(response_body)
            sanitized_body = _sanitize_for_logging(parsed_body)
            response_body = jsonp.dumps(sanitized_body)
        except (jsonp.JSONDecodeError, ValueError):
            # If not JSON, sanitize sensitive keywords in plaintext
            response_body = _sanitize_plaintext_for_logging(response_body)
    
    if response_body and response_body != "" and response_body != "null":
        log_lines.append(f"\n{response_body}")
    log_lines.append("-" * 68)
    logger.info("\n".join(log_lines))
