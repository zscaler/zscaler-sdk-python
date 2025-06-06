import requests
import logging
import os

from zscaler.config.config_setter import ConfigSetter
from zscaler.config.config_validator import ConfigValidator
from zscaler.logger import setup_logging
from zscaler.request_executor import RequestExecutor
from zscaler.cache.no_op_cache import NoOpCache
from zscaler.cache.zscaler_cache import ZscalerCache
from zscaler.oneapi_oauth_client import OAuth
from zscaler.zcc.zcc_service import ZCCService
from zscaler.ztw.ztw_service import ZTWService
from zscaler.zdx.zdx_service import ZDXService
from zscaler.zia.zia_service import ZIAService
from zscaler.zpa.zpa_service import ZPAService
from zscaler.zwa.zwa_service import ZWAService
from zscaler.zcc.legacy import LegacyZCCClientHelper
from zscaler.ztw.legacy import LegacyZTWClientHelper
from zscaler.zdx.legacy import LegacyZDXClientHelper
from zscaler.zpa.legacy import LegacyZPAClientHelper
from zscaler.zia.legacy import LegacyZIAClientHelper
from zscaler.zwa.legacy import LegacyZWAClientHelper


class Client:
    """A Zscaler client object"""

    def __init__(
        self,
        user_config: dict = {},
        zcc_legacy_client: LegacyZCCClientHelper = None,
        ztw_legacy_client: LegacyZTWClientHelper = None,
        zdx_legacy_client: LegacyZDXClientHelper = None,
        zpa_legacy_client: LegacyZPAClientHelper = None,
        zia_legacy_client: LegacyZIAClientHelper = None,
        zwa_legacy_client: LegacyZWAClientHelper = None,
        use_legacy_client: bool = False,
    ):
        self.use_legacy_client = use_legacy_client
        self.zcc_legacy_client = zcc_legacy_client
        self.ztw_legacy_client = ztw_legacy_client
        self.zdx_legacy_client = zdx_legacy_client
        self.zpa_legacy_client = zpa_legacy_client
        self.zia_legacy_client = zia_legacy_client
        self.zwa_legacy_client = zwa_legacy_client

        # ZCC Legacy client initialization logic
        if use_legacy_client and zcc_legacy_client:
            self._config = {}
            self._request_executor = zcc_legacy_client
            self.logger = logging.getLogger(__name__)
            self.logger.info("Legacy ZCC client initialized successfully.")
            return

        # ZDX Legacy client initialization logic
        if use_legacy_client and zdx_legacy_client:
            self._config = {}
            self._request_executor = zdx_legacy_client
            self.logger = logging.getLogger(__name__)
            self.logger.info("Legacy ZDX client initialized successfully.")
            return

        # ZWA Legacy client initialization logic
        if use_legacy_client and zwa_legacy_client:
            self._config = {}
            self._request_executor = zwa_legacy_client
            self.logger = logging.getLogger(__name__)
            self.logger.info("Legacy ZWA client initialized successfully.")
            return

        # ZPA Legacy client initialization logic
        if use_legacy_client and zpa_legacy_client:
            self._config = {}
            self._request_executor = zpa_legacy_client
            self.logger = logging.getLogger(__name__)
            self.logger.info("Legacy ZPA client initialized successfully.")
            return

        # ZIA Legacy client initialization logic for ZIA
        if use_legacy_client and zia_legacy_client:
            self._config = {}
            self._request_executor = zia_legacy_client
            self.logger = logging.getLogger(__name__)
            self.logger.info("Legacy ZIA client initialized successfully.")
            return

        # ZTWService Legacy client initialization logic for ZTWService
        if use_legacy_client and ztw_legacy_client:
            self._config = {}
            self._request_executor = ztw_legacy_client
            self.logger = logging.getLogger(__name__)
            self.logger.info("Legacy ZTWService client initialized successfully.")
            return

        # Assuming user_config is a dictionary or an object with a 'logging' attribute
        logging_config = (
            user_config.get("logging", {}) if isinstance(user_config, dict) else getattr(user_config, "logging", {})
        )
        self.zcc_legacy_client = zcc_legacy_client
        self.ztw_legacy_client = ztw_legacy_client
        self.zdx_legacy_client = zdx_legacy_client
        self.zpa_legacy_client = zpa_legacy_client
        self.zia_legacy_client = zia_legacy_client
        self.zwa_legacy_client = zwa_legacy_client

        # Extract enabled and verbose from the logging configuration
        enabled = logging_config.get("enabled", None)
        verbose = logging_config.get("verbose", None)

        # Setup logging with the extracted configuration
        setup_logging("zscaler-sdk-python", enabled=enabled, verbose=verbose)
        self.logger = logging.getLogger(__name__)

        # self.logger.debug("Initializing Client with user configuration.")
        client_config_setter = ConfigSetter()
        client_config_setter._apply_config({"client": user_config})
        self._config = client_config_setter.get_config()

        # Retrieve optional customerId from config or environment
        self._customer_id = self._config["client"].get("customerId", os.getenv("ZSCALER_CUSTOMER_ID"))

        # Prune unnecessary configuration fields
        self._config = client_config_setter._prune_config(self._config)
        # Setup logging based on config
        client_config_setter._setup_logging()
        # self.logger.debug(f"Customer ID set to: {self._customer_id}")
        # Validate configuration
        ConfigValidator(self._config)
        # self.logger.debug("Configuration validated successfully.")

        # Check inline configuration first, and if not provided, use environment variables
        self._client_id = self._config["client"].get("clientId", os.getenv("ZSCALER_CLIENT_ID"))

        self._client_secret = self._config["client"].get("clientSecret", os.getenv("ZSCALER_CLIENT_SECRET"))

        self._private_key = self._config["client"].get("privateKey", os.getenv("ZSCALER_PRIVATE_KEY"))

        self._vanity_domain = self._config["client"].get("vanityDomain", os.getenv("ZSCALER_VANITY_DOMAIN"))

        self._cloud = self._config["client"].get("cloud", os.getenv("ZSCALER_CLOUD", "PRODUCTION"))

        self._sandbox_token = self._config["client"].get("sandboxToken", os.getenv("ZSCALER_SANDBOX_TOKEN"))

        self._auth_token = None

        # Ensure required fields are set, either through inline config or environment variables
        if not self._client_id and not self._sandbox_token:
            raise ValueError("Client ID is required. Please set 'clientId' or 'ZSCALER_CLIENT_ID' environment variable.")
        if not self._sandbox_token and not (self._client_secret or self._private_key):
            raise ValueError("Either Client Secret or Private Key is required. Please set 'clientSecret' or 'privateKey'.")

        # self.logger.debug(f"Client ID: {self._client_id}")
        # self.logger.debug(f"Vanity Domain: {self._vanity_domain}")
        # self.logger.debug(f"Cloud: {self._cloud}")
        # self.logger.debug(f"Customer ID: {self._customer_id}")

        # Handle cache
        cache = NoOpCache()
        if self._config["client"]["cache"]["enabled"]:
            if user_config.get("cacheManager") is None:
                time_to_idle = self._config["client"]["cache"]["defaultTti"]
                time_to_live = self._config["client"]["cache"]["defaultTtl"]
                cache = ZscalerCache(time_to_live, time_to_idle)
                self.logger.debug(f"Using default cache with TTL: {time_to_live}, TTI: {time_to_idle}")
            else:
                cache = user_config.get("cacheManager")
                self.logger.debug("Using custom cache manager.")

        self._request_executor = user_config.get("requestExecutor", RequestExecutor)(
            self._config,
            cache,
            user_config.get("httpClient", None),
            self.zcc_legacy_client,
            self.ztw_legacy_client,
            self.zdx_legacy_client,
            self.zpa_legacy_client,
            self.zia_legacy_client,
            self.zwa_legacy_client,
        )
        # self.logger.debug("Request executor initialized.")

        # Lazy load ZIA and ZPA clients
        self._zcc = None
        self._ztw = None
        self._zia = None
        self._zwa = None
        self._zpa = None
        self._zdx = None
        # self.logger.debug("Client initialized successfully.")

    def authenticate(self):
        """
        Handles authentication by using either client_secret or private_key.
        """
        # self.logger.debug("Starting authentication process.")
        oauth_client = OAuth(self._request_executor, self._config)
        self._auth_token = oauth_client._get_access_token()
        self.logger.debug("Authentication successful. Access token obtained.")

        # Update the default headers by setting the Authorization Bearer token
        self._request_executor._default_headers.update({"Authorization": f"Bearer {self._auth_token}"})
        self.logger.debug("Authorization header updated with access token.")

    @property
    def zcc(self):
        if self.use_legacy_client:
            return self.zcc_legacy_client
        if self._zcc is None:
            self._zcc = ZCCService(self)
        return self._zcc

    @property
    def zdx(self):
        if self.use_legacy_client:
            return self.zdx_legacy_client
        if self._zdx is None:
            self._zdx = ZDXService(self)
        return self._zdx

    @property
    def zia(self):
        if self.use_legacy_client:
            return self.zia_legacy_client
        if self._zia is None:
            # Pass RequestExecutor directly
            self._zia = ZIAService(self._request_executor)
        return self._zia

    @property
    def zwa(self):
        if self.use_legacy_client:
            return self.zwa_legacy_client
        if self._zwa is None:
            self._zwa = ZWAService(self)
        return self._zwa

    @property
    def ztw(self):
        if self.use_legacy_client:
            return self.ztw_legacy_client
        if self._ztw is None:
            # Pass RequestExecutor directly
            self._ztw = ZTWService(self._request_executor)
        return self._ztw

    @property
    def zpa(self):
        if self.use_legacy_client:
            return self.zpa_legacy_client
        if self._zpa is None:
            self._zpa = ZPAService(self._request_executor, self._config)
        return self._zpa

    def __enter__(self):
        """
        Automatically create and set session within context manager.
        """
        if not self.use_legacy_client:
            # Create and set up a session using 'requests' library for sync.
            self._session = requests.Session()
            self._request_executor.set_session(self._session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically close session within context manager."""
        self.logger.debug("Exiting context manager, closing session.")
        if hasattr(self, "_session"):
            self._session.close()
            self.logger.debug("Session closed.")

    """
    Getters
    """

    def get_config(self):
        return self._config

    def get_request_executor(self):
        return self._request_executor

    """
    Misc
    """

    def set_custom_headers(self, headers):
        self._request_executor.set_custom_headers(headers)

    def clear_custom_headers(self):
        self._request_executor.clear_custom_headers()

    def get_custom_headers(self):
        return self._request_executor.get_custom_headers()

    def get_default_headers(self):
        return self._request_executor.get_default_headers()


class LegacyZPAClient(Client):
    def __init__(
        self,
        config: dict = {},
    ):
        client_id = config.get("clientId", os.getenv("ZPA_CLIENT_ID"))
        client_secret = config.get("clientSecret", os.getenv("ZPA_CLIENT_SECRET"))
        customer_id = config.get("customerId", os.getenv("ZPA_CUSTOMER_ID"))
        cloud = config.get("cloud", os.getenv("ZSCALER_CLOUD", "PRODUCTION"))
        microtenant_id = config.get("microtenantId", os.getenv("ZPA_MICROTENANT_ID"))
        timeout = config.get("timeout", 240)
        cache = config.get("cache", None)
        fail_safe = config.get("failSafe", None)
        request_executor_impl = config.get("requestExecutor", None)

        # Initialize the LegacyZPAClientHelper with the extracted parameters
        legacy_helper = LegacyZPAClientHelper(
            client_id=client_id,
            client_secret=client_secret,
            customer_id=customer_id,
            cloud=cloud,
            microtenant_id=microtenant_id,
            timeout=timeout,
            cache=cache,
            fail_safe=fail_safe,
            request_executor_impl=request_executor_impl,
        )
        super().__init__(config, zpa_legacy_client=legacy_helper, use_legacy_client=True)


class LegacyZIAClient(Client):
    def __init__(
        self,
        config: dict = {},
    ):
        username = config.get("username", os.getenv("ZIA_USERNAME"))
        password = config.get("password", os.getenv("ZIA_PASSWORD"))
        api_key = config.get("api_key", os.getenv("ZIA_API_KEY"))
        cloud = config.get("cloud", os.getenv("ZIA_CLOUD"))
        timeout = config.get("timeout", 240)
        cache = config.get("cache", None)
        fail_safe = config.get("failSafe", None)
        request_executor_impl = config.get("requestExecutor", None)

        # Initialize the LegacyZIAClientHelper with the extracted parameters
        legacy_helper = LegacyZIAClientHelper(
            username=username,
            password=password,
            api_key=api_key,
            cloud=cloud,
            timeout=timeout,
            cache=cache,
            fail_safe=fail_safe,
            request_executor_impl=request_executor_impl,
        )
        super().__init__(config, zia_legacy_client=legacy_helper, use_legacy_client=True)


class LegacyZTWClient(Client):
    def __init__(
        self,
        config: dict = {},
    ):
        username = config.get("username", os.getenv("ZTW_USERNAME"))
        password = config.get("password", os.getenv("ZTW_PASSWORD"))
        api_key = config.get("api_key", os.getenv("ZTW_API_KEY"))
        cloud = config.get("cloud", os.getenv("ZTW_CLOUD"))
        timeout = config.get("timeout", 240)
        cache = config.get("cache", None)
        fail_safe = config.get("failSafe", None)
        request_executor_impl = config.get("requestExecutor", None)
        # Initialize the LegacyZTWClientHelper with the extracted parameters
        legacy_helper = LegacyZTWClientHelper(
            username=username,
            password=password,
            api_key=api_key,
            cloud=cloud,
            timeout=timeout,
            cache=cache,
            fail_safe=fail_safe,
            request_executor_impl=request_executor_impl,
        )
        super().__init__(config, ztw_legacy_client=legacy_helper, use_legacy_client=True)


class LegacyZCCClient(Client):
    def __init__(
        self,
        config: dict = {},
    ):
        api_key = config.get("api_key", os.getenv("ZCC_CLIENT_ID"))
        secret_key = config.get("secret_key", os.getenv("ZCC_CLIENT_SECRET"))
        cloud = config.get("cloud", os.getenv("ZCC_CLOUD"))
        timeout = config.get("timeout", 240)
        request_executor_impl = config.get("requestExecutor", None)

        # Initialize the LegacyZCCClientHelper with the extracted parameters
        legacy_helper = LegacyZCCClientHelper(
            api_key=api_key,
            secret_key=secret_key,
            cloud=cloud,
            timeout=timeout,
            request_executor_impl=request_executor_impl,
        )
        super().__init__(config, zcc_legacy_client=legacy_helper, use_legacy_client=True)


class LegacyZDXClient(Client):
    def __init__(
        self,
        config: dict = {},
    ):
        client_id = config.get("key_id", os.getenv("ZDX_CLIENT_ID"))
        client_secret = config.get("key_secret", os.getenv("ZDX_CLIENT_SECRET"))
        cloud = config.get("cloud", os.getenv("ZDX_CLOUD", "zdxcloud"))
        timeout = config.get("timeout", 240)
        request_executor_impl = config.get("requestExecutor", None)
        # Initialize the LegacyZDXClientHelper with the extracted parameters
        legacy_helper = LegacyZDXClientHelper(
            client_id=client_id,
            client_secret=client_secret,
            cloud=cloud,
            timeout=timeout,
            request_executor_impl=request_executor_impl,
        )
        super().__init__(config, zdx_legacy_client=legacy_helper, use_legacy_client=True)


class LegacyZWAClient(Client):
    def __init__(
        self,
        config: dict = {},
    ):
        key_id = config.get("key_id", os.getenv("ZWA_CLIENT_ID"))
        key_secret = config.get("key_secret", os.getenv("ZWA_CLIENT_SECRET"))
        cloud = config.get("cloud", os.getenv("ZWA_CLOUD", "us1"))
        timeout = config.get("timeout", 240)
        request_executor_impl = config.get("requestExecutor", None)
        # Initialize the LegacyZWAClientHelper with the extracted parameters
        legacy_helper = LegacyZWAClientHelper(
            key_id=key_id,
            key_secret=key_secret,
            cloud=cloud,
            timeout=timeout,
            request_executor_impl=request_executor_impl,
        )
        super().__init__(config, zwa_legacy_client=legacy_helper, use_legacy_client=True)
