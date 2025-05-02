import os

ZPA_BASE_URLS = {
    "PRODUCTION": "https://config.private.zscaler.com",
    "ZPATWO": "https://config.zpatwo.net",
    "BETA": "https://config.zpabeta.net",
    "GOV": "https://config.zpagov.net",
    "GOVUS": "https://config.zpagov.us",
    "PREVIEW": "https://config.zpapreview.net",
    "QA": "https://config.qa.zpath.net",
    "QA2": "https://pdx2-zpa-config.qa2.zpath.net",
    "DEV": "https://public-api.dev.zpath.net",
}

DEV_AUTH_URL = "https://authn1.dev.zpath.net/authn/v1/oauth/token"


RETRYABLE_STATUS_CODES = {408, 409, 412, 429, 500, 502, 503, 504}
MAX_RETRIES = 5
BACKOFF_FACTOR = 1
BACKOFF_BASE_DURATION = 2

ZSCALER_ONE_API_DEV = "https://help.zscaler.com/oneapi"
ZIDENTITY_DEV = "https://help.zscaler.com/zidentity"

GET_ZSCALER_CLIENT_ID = f"{ZIDENTITY_DEV}" "/about-api-clients"

GET_ZSCALER_CLIENT_SECRET = f"{ZIDENTITY_DEV}" "/about-api-clients"

GET_ZSCALER_VANITY_DOMAIN = f"{ZIDENTITY_DEV}" "/migrating-zscaler-service-admins-zidentity"

GET_ZSCALER_CLOUD = f"{ZIDENTITY_DEV}" "/migrating-zscaler-service-admins-zidentity"

GET_ZPA_CUSTOMER_ID = f"{ZSCALER_ONE_API_DEV}" "/getting-started#ZPA-customerId-ZSLogin-admin-portal"

GET_ZPA_MICROTENANT_ID = f"{ZSCALER_ONE_API_DEV}" "/getting-started#ZPA-customerId-ZSLogin-admin-portal"

EPOCH_YEAR = 1970
EPOCH_MONTH = 1
EPOCH_DAY = 1

DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


_GLOBAL_YAML_PATH = os.path.join(os.path.expanduser("~"), ".zscaler", "zscaler.yaml")
_LOCAL_YAML_PATH = os.path.join(os.getcwd(), "zscaler.yaml")
