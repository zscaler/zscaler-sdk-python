from zscaler.constants import (
    GET_ZSCALER_CLIENT_ID,
    GET_ZSCALER_CLIENT_SECRET,
    GET_ZSCALER_VANITY_DOMAIN,
    GET_ZSCALER_CLOUD,
    GET_ZPA_CUSTOMER_ID,
    GET_ZPA_MICROTENANT_ID,
)


ERROR_MESSAGE_CLIENT_ID_MISSING = (
    "Your Zscaler Client ID is missing. "
    "You can generate one in the ZIdentity"
    " Console. Follow these instructions:"
    f" {GET_ZSCALER_CLIENT_ID}"
)

ERROR_MESSAGE_CLIENT_SECRET_MISSING = (
    "Your Zscaler Client Secret is missing. "
    "You can generate one in the ZIdentity"
    " Console. Follow these instructions:"
    f" {GET_ZSCALER_CLIENT_SECRET}"
)

ERROR_MESSAGE_VANITY_DOMAIN_MISSING = (
    "Your Zscaler vanity domain is missing. " " Follow these instructions:" f" {GET_ZSCALER_VANITY_DOMAIN}"
)

ERROR_MESSAGE_CLOUD_MISSING = "Your Zscaler vanity domain is missing. " " Follow these instructions:" f" {GET_ZSCALER_CLOUD}"

ERROR_MESSAGE_ZPA_CUSTOMER_ID = "Your ZPA customer ID is missing. " " Follow these instructions:" f" {GET_ZPA_CUSTOMER_ID}"

ERROR_MESSAGE_ZPA_MICROTENANT_ID = (
    "Your ZPA customer ID is missing. " " Follow these instructions:" f" {GET_ZPA_MICROTENANT_ID}"
)

ERROR_MESSAGE_URL_NOT_HTTPS = "Your Zscaler URL must start with 'https'."
ERROR_MESSAGE_429_MISSING_DATE_X_RESET = "429 response must have the 'x-ratelimit-reset' and 'Date' headers"

ERROR_MESSAGE_PROXY_MISSING_HOST = "Please add a host URL to your proxy configuration."

ERROR_MESSAGE_PROXY_MISSING_AUTH = (
    "Proxy configuration must include BOTH your username and password " "if authentication is required"
)

ERROR_MESSAGE_PROXY_INVALID_PORT = "Proxy port number must be a number, and between 1 and 65535 (inclusive)"
