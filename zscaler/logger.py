import logging
import os

LOG_FORMAT = "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s"


def setup_logging(logger_name="zscaler-sdk-python"):
    """
    Set up logging with specified level and logger name.
    Log level is controlled via ZSCALER_SDK_VERBOSE environment variable.
    Logging can be enabled/disabled via ZSCALER_SDK_LOG environment variable.

    Parameters:
    - logger_name (str, optional): Logger name. Defaults to "zscaler-sdk-python".
    """

    logging_enabled = os.getenv("ZSCALER_SDK_LOG", "false").lower() == "true"

    if not logging_enabled:
        # If logging is not enabled, set up a null handler
        logging.getLogger(logger_name).addHandler(logging.NullHandler())
        return

    verbose = os.getenv("ZSCALER_SDK_VERBOSE", "false").lower() == "true"
    log_level = logging.DEBUG if verbose else logging.INFO

    # Create a logger with the specified name
    logger = logging.getLogger(logger_name)

    # If the logger already has handlers, remove them to avoid duplicate logging
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Set log level
    logger.setLevel(log_level)

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
