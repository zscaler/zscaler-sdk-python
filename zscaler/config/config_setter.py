import os
import logging
import yaml
from zscaler.constants import _GLOBAL_YAML_PATH, _LOCAL_YAML_PATH
from flatdict import FlatDict

from zscaler.helpers import to_snake_case


logger = logging.getLogger(__name__)


class ConfigSetter:
    """
    This class sets up the configuration for the Zscaler Client
    """

    _ZSCALER = "ZSCALER"
    _DEFAULT_CONFIG = {
        "client": {
            "clientId": "",
            "clientSecret": "",
            "privateKey": "",
            "vanityDomain": "",
            "cloud": "",
            "userAgent": "",
            "customerId": "",
            "microtenantId": "",
            "sandboxToken": "",
            "sandboxCloud": "",
            "connectionTimeout": 30,
            "requestTimeout": 0,
            "cache": {
                "enabled": False,
                "defaultTtl": "",
                "defaultTti": "",
            },
            "logging": {"enabled": False, "verbose": False},
            "proxy": {"port": "", "host": "", "username": "", "password": ""},
            "rateLimit": {
                "maxRetries": 2,
            },
            "testing": {"disableHttpsCheck": ""},
        }
    }

    def __init__(self):
        """
        Constructor for Configuration Setter class. Sets default config
        and checks for configuration settings to update config.
        """
        # logger.info("Initializing ConfigSetter with default configuration.")
        # Create configuration using default config
        self._config = ConfigSetter._DEFAULT_CONFIG
        # Update configuration
        self._update_config()

    def get_config(self):
        """
        Return Zscaler client configuration

        Returns:
            dict -- Dictionary containing the client configuration
        """
        # logger.debug("Fetching current configuration.")
        return self._config

    def _prune_config(self, config):
        """
        This method cleans up the configuration object by removing fields
        with no value
        """
        # logger.debug("Pruning configuration to remove empty fields.")
        flat_current_config = FlatDict(config, delimiter="_")
        for key in flat_current_config.keys():
            if flat_current_config.get(key) == "":
                del flat_current_config[key]

        return flat_current_config.as_dict()

    def _update_config(self):
        """
        Updates the configuration of the Zscaler Client by:
        1. Applying default values
        2. Checking for a global Zscaler config YAML
        3. Checking for a local Zscaler config YAML
        4. Checking for corresponding ENV variables
        """
        # logger.info("Updating configuration with defaults, YAML files, and environment variables.")
        # apply default config values to config
        self._apply_default_values()

        # check if GLOBAL yaml exists, apply if true
        if os.path.exists(_GLOBAL_YAML_PATH):
            logger.info(f"Applying global YAML configuration from {_GLOBAL_YAML_PATH}.")
            self._apply_yaml_config(_GLOBAL_YAML_PATH)

        # check if LOCAL yaml exists, apply if true
        if os.path.exists(_LOCAL_YAML_PATH):
            logger.info(f"Applying local YAML configuration from {_LOCAL_YAML_PATH}.")
            self._apply_yaml_config(_LOCAL_YAML_PATH)

        # apply existing environment variables
        self._apply_env_config("client")
        self._apply_env_config("testing")

    def _setup_logging(self):
        """
        Setup logging based on configuration.
        """
        logging_enabled = self._config["client"]["logging"].get("enabled", False)
        verbose_logging = self._config["client"]["logging"].get("verbose", False)

        if logging_enabled:
            # logger.debug("Enabling logging for Zscaler SDK.")
            os.environ["ZSCALER_SDK_LOG"] = "true"
            os.environ["ZSCALER_SDK_VERBOSE"] = "true" if verbose_logging else "false"
        else:
            logger.debug("Disabling logging for Zscaler SDK.")
            os.environ["ZSCALER_SDK_LOG"] = "false"

    def _apply_default_values(self):
        """Apply default values to default client configuration"""
        # logger.debug("Applying default values to configuration.")
        # Ensure both 'client' and 'testing' dictionaries are initialized
        if "client" not in self._config:
            self._config["client"] = {}

        if "testing" not in self._config:
            self._config["testing"] = {}

        # Set default values for 'client' and 'testing' configurations
        self._config["client"]["connectionTimeout"] = 30
        self._config["client"]["cache"] = {"enabled": False, "defaultTtl": 300, "defaultTti": 300}
        self._config["client"]["logging"] = {"enabled": False, "logLevel": logging.INFO}

        self._config["client"]["userAgent"] = ""
        self._config["client"]["requestTimeout"] = 0
        self._config["client"]["rateLimit"] = {"maxRetries": 2}

        # Add a check for the 'testing' key before accessing it
        if "testing" not in self._config:
            self._config["testing"] = {}

        # Initialize the 'testing' section with default values
        self._config["testing"]["disableHttpsCheck"] = False

    def _apply_config(self, new_config: dict):
        """Apply a config dictionary to the current config, overwriting values"""
        # logger.debug("Applying new configuration settings.")
        flat_current_client = FlatDict(self._config["client"], delimiter="_")
        flat_current_testing = FlatDict(self._config["testing"], delimiter="_")

        flat_new_client = FlatDict(new_config.get("client", {}), delimiter="_")
        flat_new_testing = FlatDict(new_config.get("testing", {}), delimiter="_")

        flat_current_client.update(flat_new_client)
        flat_current_testing.update(flat_new_testing)

        self._config = {"client": flat_current_client.as_dict(), "testing": flat_current_testing.as_dict()}

    def _apply_yaml_config(self, path: str):
        """This method applies a YAML configuration to the Zscaler Client Config"""
        logger.debug(f"Loading YAML configuration from {path}.")
        # Start with empty config
        config = {}
        with open(path, "r") as file:
            # Open file stream and attempt to load YAML
            config = yaml.load(file, Loader=yaml.SafeLoader)
        # Apply acquired config to configuration
        self._apply_config(config.get("zscaler", {}))

    def _apply_env_config(self, conf_key):
        """
        This method checks the environment variables for any Zscaler
        configuration parameters and applies them if available.
        """
        # logger.debug(f"Applying environment variables for {conf_key} configuration.")
        # Flatten current config and join with underscores
        # (for environment variable format)
        flattened_config = FlatDict(self._config.get(conf_key, {}), delimiter="_")
        flattened_keys = flattened_config.keys()

        # Create empty result config and populate
        updated_config = FlatDict({}, delimiter="_")

        # Go through keys and search for it in the environment vars
        # using the format described in the README
        for key in flattened_keys:
            env_key = ConfigSetter._ZSCALER + "_" + to_snake_case(key).upper()
            env_value = os.environ.get(env_key, None)

            if env_value is not None:
                updated_config[key] = env_value
        self._apply_config({conf_key: updated_config.as_dict()})
