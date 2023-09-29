import logging
import os

LOG_FORMAT = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"


def setup_logging(log_level=logging.INFO, logger_name="zscaler-sdk-python"):
    # Get the logging environment variable and verbose logging environment variable
    is_logging_enabled = os.getenv("ZSCALER_SDK_LOG", "false").lower() == "true"
    is_verbose = os.getenv("ZSCALER_SDK_VERBOSE", "false").lower() == "true"

    # If logging is not enabled, return without setting up the logger
    if not is_logging_enabled:
        return

    # If verbose logging is enabled, set the log level to DEBUG
    if is_verbose:
        log_level = logging.DEBUG

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    log_formatter = logging.Formatter(LOG_FORMAT)
    stream_handler.setFormatter(log_formatter)

    file_handler = logging.FileHandler("zscaler_sdk_python.log")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)

    logger = logging.getLogger(logger_name)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
    logger.disabled = False


def enable_logging():
    logger = logging.getLogger("zscaler-sdk-python")
    logger.disabled = False


def disable_logging():
    logger = logging.getLogger("zscaler-sdk-python")
    logger.disabled = True
