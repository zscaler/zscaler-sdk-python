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
}

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
MAX_RETRIES = 5
BACKOFF_FACTOR = 1
BACKOFF_BASE_DURATION = 2

DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"

EPOCH_YEAR = 1970
EPOCH_MONTH = 1
EPOCH_DAY = 1

_GLOBAL_YAML_PATH = os.path.join(os.path.expanduser("~"), ".zpa", "zpa.yaml")
_LOCAL_YAML_PATH = os.path.join(os.getcwd(), "zpa.yaml")
