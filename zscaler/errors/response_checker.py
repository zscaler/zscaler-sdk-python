import json
import logging
from zscaler.errors.http_error import HTTPError
from zscaler.errors.zscaler_api_error import ZscalerAPIError
from zscaler.exceptions import HTTPException, ZscalerAPIException
from zscaler.exceptions import exceptions

logger = logging.getLogger(__name__)

@staticmethod
def check_response_for_error(url, response_details, response_body):
    """
    Checks HTTP response for errors in the response body.

    Args:
        url (str): URL of the response
        response_details (requests.Response): Response object with details
        response_body (str): Response body in JSON or plain string

    Returns:
        Tuple(dict or None, error or None)
    """
    # Defensive check: if response_details is not a real HTTP response, skip
    if not hasattr(response_details, "headers"):
        logger.debug(f"[SKIP] check_response_for_error received non-Response object: {type(response_details)}")
        return response_details, None

    content_type = response_details.headers.get("Content-Type", "")
    is_json = "application/json" in content_type
    body_text = response_body if isinstance(response_body, str) else str(response_body)

    try:
        formatted_response = json.loads(response_body) if is_json else response_body
    except json.JSONDecodeError as e:
        logger.warning(f"Non-JSON response from {url}: {body_text}")
        if exceptions.raise_exception:
            raise HTTPException(url, response_details, body_text)
        return None, HTTPError(url, response_details, body_text)

    # ✅ Only now we are confident it's safe to access .status_code
    status_code = response_details.status_code

    if 200 <= status_code < 300:
        return formatted_response, None

    try:
        error = ZscalerAPIError(url, response_details, formatted_response)
        if exceptions.raise_exception:
            raise ZscalerAPIException(error)
        return None, error

    except Exception as e:
        logger.exception("Failed to construct ZscalerAPIError.")
        generic_error = HTTPError(url, response_details, formatted_response)
        if exceptions.raise_exception:
            raise HTTPException(str(generic_error)) from e
        return None, generic_error
