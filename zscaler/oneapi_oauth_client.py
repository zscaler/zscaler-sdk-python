from typing import Dict, Optional, Any, Union
import logging
import json
import os
import requests
from jose import jwt
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from zscaler.user_agent import UserAgent
from zscaler.oneapi_http_client import HTTPClient
from zscaler.errors.response_checker import check_response_for_error

logger = logging.getLogger(__name__)

# Security constants for key validation
MIN_RSA_KEY_SIZE: int = 2048  # NIST recommends minimum 2048 bits for RSA keys


def validate_rsa_key_strength(private_key_obj: Union[rsa.RSAPrivateKey, Any]) -> Optional[int]:
    """
    Validate that an RSA private key meets minimum security requirements.
    
    This addresses CWE-326 (Inadequate Encryption Strength) by ensuring
    RSA keys meet NIST recommendations of at least 2048 bits.
    
    Args:
        private_key_obj: RSA private key object from cryptography library
        
    Raises:
        ValueError: If the key size is below the minimum requirement
        
    Returns:
        int: The key size in bits
    """
    if isinstance(private_key_obj, rsa.RSAPrivateKey):
        key_size: int = private_key_obj.key_size
        if key_size < MIN_RSA_KEY_SIZE:
            logger.error(f"RSA key size ({key_size} bits) is below minimum requirement ({MIN_RSA_KEY_SIZE} bits)")
            raise ValueError(
                f"Insufficient RSA key strength: {key_size} bits. "
                f"Minimum required: {MIN_RSA_KEY_SIZE} bits (NIST recommendation). "
                f"Please use a stronger RSA key to ensure secure authentication."
            )
        logger.debug(f"RSA key validation passed: {key_size} bits")
        return key_size
    else:
        logger.warning(f"Key validation skipped: Unsupported key type {type(private_key_obj)}")
        return None


class OAuth:
    """
    This class contains the OAuth actions for the Zscaler Client.
    """

    _instance: Optional['OAuth'] = None
    _last_config: Optional[Dict[str, Any]] = None

    def __new__(cls, request_executor: 'RequestExecutor', config: Dict[str, Any]) -> 'OAuth':
        if cls._instance is None or cls._last_config != config:
            cls._instance = super(OAuth, cls).__new__(cls)
            cls._last_config = config
            cls._instance.__init__(request_executor, config)
        return cls._instance

    def __init__(self, request_executor: 'RequestExecutor', config: Dict[str, Any]) -> None:
        if not hasattr(self, "_initialized"):
            self._request_executor: 'RequestExecutor' = request_executor
            self._config: Dict[str, Any] = config
            self._access_token: Optional[str] = None
            self._token_expires_at: Optional[float] = None
            self._token_issued_at: Optional[float] = None

            # Initialize cache based on config
            self._cache: Optional[Any] = self._initialize_cache()
            self._cache_key: str = self._generate_cache_key()
            # No buffer needed - simple expiration check
            # logging.debug("OAuth instance created with provided configuration.")
            self._initialized: bool = True

    def _initialize_cache(self) -> Optional[Any]:
        """
        Initialize cache based on configuration.

        Returns:
            Cache instance or None if caching is disabled
        """
        cache_config: Union[Dict[str, Any], Any] = self._config.get("cache", {})

        # If cache is already a cache instance, return it
        if hasattr(cache_config, 'get') and hasattr(cache_config, 'add'):
            return cache_config

        # If cache is a dict with enabled flag
        if isinstance(cache_config, dict) and cache_config.get("enabled", False):
            from zscaler.cache.zscaler_cache import ZscalerCache

            # Get TTL and TTI from config
            ttl: int = cache_config.get("defaultTtl", 3600)  # Default 1 hour
            tti: int = cache_config.get("defaultTti", 1800)  # Default 30 minutes

            return ZscalerCache(ttl=ttl, tti=tti)

        return None

    def _generate_cache_key(self) -> str:
        """
        Generate a unique cache key for this OAuth instance.

        Returns:
            str: Unique cache key based on client configuration
        """
        # Handle legacy client configurations that don't have OneAPI OAuth fields
        client_config: Dict[str, Any] = self._config.get("client", {})

        # For legacy clients, use alternative identifiers
        if "clientId" not in client_config:
            # Legacy clients might have username, api_key, etc.
            username: str = client_config.get("username", "unknown")
            api_key: str = client_config.get("api_key", "unknown")
            cloud: str = client_config.get("cloud", "production").lower()
            return f"oauth_token_legacy_{username}_{api_key}_{cloud}"

        # For OneAPI clients, use the standard fields
        client_id: str = client_config["clientId"]
        vanity_domain: str = client_config["vanityDomain"]
        cloud: str = client_config.get("cloud", "PRODUCTION").lower()
        return f"oauth_token_{client_id}_{vanity_domain}_{cloud}"

    def _get_cached_token(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve token from cache if available and enabled.

        Returns:
            dict: Cached token data or None if not available
        """
        if not self._cache or not self._cache_enabled():
            return None

        try:
            cached_data: Optional[Any] = self._cache.get(self._cache_key)
            if cached_data and isinstance(cached_data, dict):
                logger.debug("Retrieved token from cache")
                return cached_data
        except Exception as e:
            logger.warning(f"Failed to retrieve token from cache: {e}")

        return None

    def _cache_token(self, access_token: str, expires_at: float) -> None:
        """
        Cache the token if caching is enabled.

        Args:
            access_token (str): The access token to cache
            expires_at (float): Token expiration timestamp
        """
        if not self._cache or not self._cache_enabled():
            return

        try:
            token_data: Dict[str, Union[str, float]] = {
                'access_token': access_token,
                'expires_at': expires_at,
                'issued_at': time.time()
            }

            # Store token data directly (not as tuple)
            self._cache.add(self._cache_key, token_data)
            logger.debug("Token cached successfully")
        except Exception as e:
            logger.warning(f"Failed to cache token: {e}")

    def _cache_enabled(self) -> bool:
        """
        Check if caching is enabled in the configuration.

        Returns:
            bool: True if caching is enabled
        """
        return self._cache is not None

    def _is_token_expired(self, token_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if the current token is expired.

        Args:
            token_data (dict, optional): Token data to check. If None, uses instance data.

        Returns:
            bool: True if token is expired
        """
        if token_data:
            # Check cached token data
            expires_at: Optional[float] = token_data.get('expires_at')
            if not expires_at:
                return True
            return time.time() >= expires_at
        else:
            # Check instance token data
            if not self._token_expires_at:
                return True
            return time.time() >= self._token_expires_at

    def authenticate(self) -> requests.Response:
        """
        Main authentication function. Determines which authentication
        method to use (Client Secret or JWT Private Key) and retrieves the
        OAuth access token.

        Returns:
            str: OAuth access token.
        """
        # Check if this is a legacy client configuration
        client_config: Dict[str, Any] = self._config.get("client", {})
        if "clientId" not in client_config:
            logging.error("OAuth authentication not available for legacy client configurations.")
            raise ValueError("OAuth authentication not available for legacy client configurations. "
                             "Use legacy authentication methods instead.")

        # logging.debug("Starting authentication process.")
        client_id: str = client_config["clientId"]
        client_secret: str = client_config.get("clientSecret", "")
        private_key: str = client_config.get("privateKey", "")

        if not client_id or (not client_secret and not private_key):
            logging.error("No valid client credentials provided.")
            raise ValueError("No valid client credentials provided")

        # Determine whether to authenticate with client secret or JWT
        if private_key:
            logging.info("Authenticating using JWT private key.")
            response: requests.Response = self._authenticate_with_private_key(client_id, private_key)
        else:
            # logging.info("Authenticating using client secret.")
            response: requests.Response = self._authenticate_with_client_secret(client_id, client_secret)

        # logging.debug("Authentication process completed.")
        return response

    def _setup_proxy(self, proxy: Optional[Union[Dict[str, Any], str]]) -> Optional[str]:
        """Sets up the proxy string from the configuration or environment variables."""
        proxy_string: str = ""

        if proxy is None:
            if "HTTP_PROXY" in os.environ:
                proxy_string = os.environ["HTTP_PROXY"]
            if "HTTPS_PROXY" in os.environ:
                proxy_string = os.environ["HTTPS_PROXY"]
            return proxy_string if proxy_string != "" else None

        host: str = proxy["host"]
        port: Union[int, str] = int(proxy["port"]) if "port" in proxy else ""

        if "username" in proxy and "password" in proxy:
            username: str = proxy["username"]
            password: str = proxy["password"]
            proxy_string = f"http://{username}:{password}@{host}"
        else:
            proxy_string = f"http://{host}"

        if port:
            proxy_string += f":{port}/"

        return proxy_string if proxy_string != "" else None

    def _authenticate_with_client_secret(self, client_id: str, client_secret: str) -> requests.Response:
        """
        Authenticate using client ID and client secret.

        Args:
            client_id (str): Client ID for authentication.
            client_secret (str): Client secret for authentication.

        Returns:
            str: OAuth access token.
        """
        # logging.debug("Preparing to authenticate with client secret.")
        vanity_domain: str = self._config["client"]["vanityDomain"]
        cloud: str = self._config["client"].get("cloud", "PRODUCTION").lower()
        auth_url: str = self._get_auth_url(vanity_domain, cloud)

        # Prepare form data (like in the Go SDK)
        form_data: Dict[str, str] = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": "https://api.zscaler.com",
        }

        user_agent: str = UserAgent().get_user_agent_string()
        headers: Dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": user_agent,
        }

        # Setup proxy if configured
        proxy_config: Optional[Dict[str, Any]] = self._config["client"].get("proxy")
        proxy_string: Optional[str] = self._setup_proxy(proxy_config)
        proxies: Optional[Dict[str, str]] = None
        if proxy_string:
            proxies = {"http": proxy_string, "https": proxy_string}

        # logging.debug(f"Sending authentication request to {auth_url}.")
        # Synchronous HTTP request (with form data in the body)
        response: requests.Response = requests.post(auth_url, data=form_data, headers=headers, proxies=proxies)

        if response.status_code >= 300:
            logging.error(f"Error authenticating: {response.status_code}, {response.text}")
            raise Exception(f"Error authenticating: {response.status_code}, {response.text}")

        # logging.debug("Authentication with client secret successful.")
        return response

    def _authenticate_with_private_key(self, client_id: str, private_key: str) -> requests.Response:
        """
        Authenticate using client ID and JWT private key.

        Args:
            client_id (str): Client ID for authentication.
            private_key (str): Path to the private key file, JWK JSON string, or raw private key.

        Returns:
            str: OAuth access token.
        """
        logging.debug("Preparing to authenticate with JWT private key.")
        vanity_domain: str = self._config["client"]["vanityDomain"]
        cloud: str = self._config["client"].get("cloud", "PRODUCTION").lower()
        auth_url: str = self._get_auth_url(vanity_domain, cloud)

        # **Step 1: Determine the Private Key Type**
        private_key_obj: Union[rsa.RSAPrivateKey, Any]
        if private_key.strip().startswith("{"):
            # **JWK JSON Format**
            logging.info("Using JWK JSON format for private key.")
            jwk_key: Dict[str, Any] = json.loads(private_key.strip())  # Convert JWK string to dict
            private_key_obj = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk_key))

        elif "BEGIN PRIVATE KEY" in private_key:
            # **Raw PEM Private Key**
            logging.info("Using raw PEM private key.")
            private_key_obj = serialization.load_pem_private_key(
                private_key.encode(), password=None, backend=default_backend()
            )

        else:
            # **Assume it's a file path and read the private key**
            logging.info("Using private key from file.")
            with open(private_key, "rb") as key_file:
                private_key_obj = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

        # **Validate key strength to mitigate CWE-326 (Inadequate Encryption Strength)**
        validate_rsa_key_strength(private_key_obj)

        # **Step 2: Create JWT for Client Assertion**
        now: int = int(time.time())
        payload: Dict[str, Union[str, int]] = {
            "iss": client_id,
            "sub": client_id,
            "aud": "https://api.zscaler.com",
            "exp": now + 600,  # 10 minutes expiration
        }

        # **Generate the JWT assertion using the private key**
        assertion: str = jwt.encode(payload, private_key_obj, algorithm="RS256")

        # **Step 3: Prepare OAuth Request**
        form_data: Dict[str, str] = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_assertion": assertion,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "audience": "https://api.zscaler.com",
        }

        headers: Dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Zscaler-SDK",
        }

        # Setup proxy if configured
        proxy_config: Optional[Dict[str, Any]] = self._config["client"].get("proxy")
        proxy_string: Optional[str] = self._setup_proxy(proxy_config)
        proxies: Optional[Dict[str, str]] = None
        if proxy_string:
            proxies = {"http": proxy_string, "https": proxy_string}

        logging.debug(f"Sending authentication request to {auth_url} with JWT.")
        response: requests.Response = requests.post(auth_url, data=form_data, headers=headers, proxies=proxies)

        if response.status_code >= 300:
            logging.error(f"Error authenticating: {response.status_code}, {response.text}")
            raise Exception(f"Error authenticating: {response.status_code}, {response.text}")

        logging.info("Authentication with JWT private key successful.")
        return response

    def _get_access_token(self) -> Optional[str]:
        """
        Retrieves or generates the OAuth access token for the Zscaler OneAPI Client.
        Implements proactive token refresh using expires_in with configurable buffer.

        Returns:
            str: OAuth access token.
        """
        # Check if this is a legacy client configuration
        client_config: Dict[str, Any] = self._config.get("client", {})
        if "clientId" not in client_config:
            logger.warning("OAuth client initialized with legacy configuration - OAuth functionality not available")
            return None

        # 1. Check cache first (if enabled)
        cached_token: Optional[Dict[str, Any]] = self._get_cached_token()
        if cached_token and not self._is_token_expired(cached_token):
            self._access_token = cached_token['access_token']
            self._token_expires_at = cached_token['expires_at']
            self._token_issued_at = cached_token.get('issued_at', time.time())
            logger.debug("Using cached access token")
            return self._access_token

        # 2. Check if current token is about to expire (proactive refresh)
        if self._access_token and not self._is_token_expired():
            logger.debug("Using existing access token")
            return self._access_token

        # 3. Get new token
        logger.info("Access token expired or not available, requesting new token")
        try:
            # Call the authenticate function, which now returns the response object
            response: requests.Response = self.authenticate()

            # Check the response body for error messages using check_response_for_error
            parsed_response: Any
            err: Optional[str]
            parsed_response, err = check_response_for_error(response.url, response, response.text)

            if err:
                logging.error(f"Error during authentication: {err}")
                raise ValueError(f"Error during authentication: {err}")

            # Extract access token and expiration from the parsed response
            if isinstance(parsed_response, dict):
                self._access_token = parsed_response.get("access_token")
                expires_in: int = parsed_response.get("expires_in", 3600)  # Default to 1 hour
                self._token_expires_at = time.time() + expires_in
                self._token_issued_at = time.time()

                # Cache the new token
                self._cache_token(self._access_token, self._token_expires_at)

                logger.info(f"New access token obtained, expires in {expires_in} seconds")
            else:
                logging.error("Parsed response is not a dictionary as expected.")
                raise ValueError("Parsed response is not a dictionary as expected")

        except Exception as e:
            logging.error(f"Failed to get access token: {e}")
            raise  # Re-raise the exception to handle it outside

        return self._access_token

    def _get_auth_url(self, vanity_domain: str, cloud: str) -> str:
        """
        Determines the OAuth2 provider URL based on the vanity domain and cloud.

        Args:
            vanity_domain (str): Vanity domain for the authentication URL.
            cloud (str): Cloud environment (e.g., "production", "stage").

        Returns:
            str: The fully constructed authentication URL.
        """
        # logging.debug(f"Constructing auth URL for cloud: {cloud}.")
        if cloud == "production":
            return f"https://{vanity_domain}.zslogin.net/oauth2/v1/token"
        else:
            return f"https://{vanity_domain}.zslogin{cloud}.net/oauth2/v1/token"

    def clear_access_token(self) -> None:
        """
        Clear the current OAuth access token and remove from cache.
        """
        logging.info("Clearing the current access token.")
        self._access_token = None
        self._token_expires_at = None
        self._token_issued_at = None

        # Clear from cache if enabled
        if self._cache and self._cache_enabled():
            try:
                self._cache.delete(self._cache_key)
                logger.debug("Token cleared from cache")
            except Exception as e:
                logger.warning(f"Failed to clear token from cache: {e}")

        self._request_executor._default_headers.pop("Authorization", None)

    def get_token_info(self) -> Dict[str, Any]:
        """
        Get information about the current token status.

        Returns:
            dict: Token information including expiration and cache status
        """
        if not self._access_token:
            return {
                'has_token': False,
                'expires_at': None,
                'issued_at': None,
                'is_expired': True,
                'time_until_expiry': None,
                'cached': False
            }

        now: float = time.time()
        time_until_expiry: Optional[float] = self._token_expires_at - now if self._token_expires_at else None

        return {
            'has_token': True,
            'expires_at': self._token_expires_at,
            'issued_at': self._token_issued_at,
            'is_expired': self._is_token_expired(),
            'time_until_expiry': time_until_expiry,
            'cached': self._cache_enabled() and self._cache.contains(self._cache_key) if self._cache else False
        }
