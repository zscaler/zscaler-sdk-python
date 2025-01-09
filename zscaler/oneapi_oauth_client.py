import logging
import requests
import jwt
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from zscaler.user_agent import UserAgent
from zscaler.oneapi_http_client import HTTPClient

logger = logging.getLogger(__name__)


class OAuth:
    """
    This class contains the OAuth actions for the Zscaler Client.
    """

    _instance = None
    _last_config = None

    def __new__(cls, request_executor, config):
        if cls._instance is None or cls._last_config != config:
            cls._instance = super(OAuth, cls).__new__(cls)
            cls._last_config = config
            cls._instance.__init__(request_executor, config)
        return cls._instance

    def __init__(self, request_executor, config):
        if not hasattr(self, "_initialized"):
            self._request_executor = request_executor
            self._config = config
            self._access_token = None
            # logging.debug("OAuth instance created with provided configuration.")
            self._initialized = True

    def authenticate(self):
        """
        Main authentication function. Determines which authentication
        method to use (Client Secret or JWT Private Key) and retrieves the
        OAuth access token.

        Returns:
            str: OAuth access token.
        """
        # logging.debug("Starting authentication process.")
        client_id = self._config["client"]["clientId"]
        client_secret = self._config["client"].get("clientSecret", "")
        private_key = self._config["client"].get("privateKey", "")

        if not client_id or (not client_secret and not private_key):
            logging.error("No valid client credentials provided.")
            raise ValueError("No valid client credentials provided")

        # Determine whether to authenticate with client secret or JWT
        if private_key:
            logging.info("Authenticating using JWT private key.")
            response = self._authenticate_with_private_key(client_id, private_key)
        else:
            # logging.info("Authenticating using client secret.")
            response = self._authenticate_with_client_secret(client_id, client_secret)

        # logging.debug("Authentication process completed.")
        return response

    def _authenticate_with_client_secret(self, client_id, client_secret):
        """
        Authenticate using client ID and client secret.

        Args:
            client_id (str): Client ID for authentication.
            client_secret (str): Client secret for authentication.

        Returns:
            str: OAuth access token.
        """
        # logging.debug("Preparing to authenticate with client secret.")
        vanity_domain = self._config["client"]["vanityDomain"]
        cloud = self._config["client"].get("cloud", "PRODUCTION").lower()
        auth_url = self._get_auth_url(vanity_domain, cloud)

        # Prepare form data (like in the Go SDK)
        form_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": "https://api.zscaler.com",
        }

        user_agent = UserAgent().get_user_agent_string()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": user_agent,
        }

        # logging.debug(f"Sending authentication request to {auth_url}.")
        # Synchronous HTTP request (with form data in the body)
        response = requests.post(auth_url, data=form_data, headers=headers)

        if response.status_code >= 300:
            logging.error(f"Error authenticating: {response.status_code}, {response.text}")
            raise Exception(f"Error authenticating: {response.status_code}, {response.text}")

        # logging.debug("Authentication with client secret successful.")
        return response

    def _authenticate_with_private_key(self, client_id, private_key_path):
        """
        Authenticate using client ID and JWT private key.

        Args:
            client_id (str): Client ID for authentication.
            private_key_path (str): Path to the private key file.

        Returns:
            str: OAuth access token.
        """
        logging.debug("Preparing to authenticate with JWT private key.")
        vanity_domain = self._config["client"]["vanityDomain"]
        cloud = self._config["client"].get("cloud", "PRODUCTION").lower()
        auth_url = self._get_auth_url(vanity_domain, cloud)

        # Read and load the private key
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())

        # Create JWT for client assertion
        now = int(time.time())
        payload = {
            "iss": client_id,
            "sub": client_id,
            "aud": "https://api.zscaler.com",
            "exp": now + 600,  # 10 minutes expiration
        }

        # Generate the assertion using RS256 algorithm
        assertion = jwt.encode(payload, private_key, algorithm="RS256")

        # Prepare form data
        form_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_assertion": assertion,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "audience": "https://api.zscaler.com",
        }

        user_agent = UserAgent().get_user_agent_string()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": user_agent,
        }

        # logging.debug(f"Sending authentication request to {auth_url} with JWT.")
        # Synchronous HTTP request
        response = requests.post(auth_url, data=form_data, headers=headers)

        if response.status_code >= 300:
            logging.error(f"Error authenticating: {response.status_code}, {response.text}")
            raise Exception(f"Error authenticating: {response.status_code}, {response.text}")

        logging.info("Authentication with JWT private key successful.")
        return response

    def _get_access_token(self):
        """
        Retrieves or generates the OAuth access token for the Zscaler OneAPI Client

        Returns:
            str: OAuth access token.
        """
        # logging.debug("Retrieving access token.")
        # Return token if already generated
        if not self._access_token:
            try:
                # Call the authenticate function, which now returns the response object
                response = self.authenticate()

                # Check the response body for error messages using check_response_for_error
                parsed_response, err = HTTPClient.check_response_for_error(response.url, response, response.text)

                if err:
                    logging.error(f"Error during authentication: {err}")
                    raise ValueError(f"Error during authentication: {err}")

                # Extract access token from the parsed response
                if isinstance(parsed_response, dict):
                    self._access_token = parsed_response.get("access_token")
                    # logging.debug("Access token successfully retrieved.")
                else:
                    logging.error("Parsed response is not a dictionary as expected.")
                    raise ValueError("Parsed response is not a dictionary as expected")

            except Exception as e:
                logging.error(f"Failed to get access token: {e}")
                raise  # Re-raise the exception to handle it outside

        return self._access_token  # Return just the token, not a tuple

    def _get_auth_url(self, vanity_domain, cloud):
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

    def clear_access_token(self):
        """
        Clear the current OAuth access token.
        """
        logging.info("Clearing the current access token.")
        self._access_token = None
        self._request_executor._default_headers.pop("Authorization", None)
