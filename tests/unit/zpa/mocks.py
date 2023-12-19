from zscaler.zpa import ZPAClientHelper
import os
import vcr


# Define a VCR fixture
my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='./cassetes',
    record_mode='once',
    match_on=['uri', 'method'],
    # Add any additional VCR configurations here
)

# Define function to get client configuration from environment variables
def get_client_config():
    return {
        'client_id': os.environ.get('ZPA_CLIENT_ID', ''),
        'client_secret': os.environ.get('ZPA_CLIENT_SECRET', ''),
        'customer_id': os.environ.get('ZPA_CUSTOMER_ID', ''),
        'cloud': os.environ.get('ZPA_CLOUD', '')
    }


class MockZPAClient(ZPAClientHelper):
    def __init__(self, client_id=None, client_secret=None, customer_id=None, cloud=None, **kwargs):
        self.mock_mode = os.getenv('MOCK_TESTS', 'false').strip().lower() == 'true'

        # Use provided credentials or environment variables
        client_id = client_id or os.getenv('ZPA_CLIENT_ID')
        client_secret = client_secret or os.getenv('ZPA_CLIENT_SECRET')
        customer_id = customer_id or os.getenv('ZPA_CUSTOMER_ID')
        cloud = cloud or os.getenv('ZPA_CLOUD')

        super().__init__(client_id, client_secret, customer_id, cloud, **kwargs)

        if self.mock_mode:
            # In mock mode, set a mock token and headers
            self.token = 'mock_token'
            self.access_token = 'mock_access_token'
            self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def login(self):
        if self.mock_mode:
            # Return mock response in mock mode
            return MockResponse({'access_token': 'mock_access_token'}, 200)
        else:
            # Perform actual login to get real token
            return super().login()

    def refreshToken(self):
        if not self.mock_mode:
            # Only refresh token in real mode
            super().refreshToken()
        # No action needed in mock mode

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data




    def get_application_segments(self, customer_id):
        # Return the mock response for getting application segments
        return {
        "totalPages": 1,
        "list": [
            {
                "creationTime": "1628211456",
                "modifiedBy": "1",
                "id": "1",
                "domainNames": ["www.example.com"],
                "name": "Test A",
                "description": "Test",
                "serverGroups": [
                    {
                        "id": "1",
                        "creationTime": "1625698796",
                        "modifiedBy": "1",
                        "name": "Test",
                        "enabled": True,
                        "configSpace": "DEFAULT",
                        "dynamicDiscovery": False,
                    }
                ],
                "enabled": True,
                "passiveHealthEnabled": True,
                "tcpPortRanges": ["443", "443", "80", "80"],
                "tcpPortRange": [
                    {"from": "443", "to": "443"},
                    {"from": "80", "to": "80"},
                ],
                "doubleEncrypt": False,
                "configSpace": "DEFAULT",
                "bypassType": "NEVER",
                "healthCheckType": "DEFAULT",
                "icmpAccessType": "NONE",
                "isCnameEnabled": True,
                "ipAnchored": False,
                "healthReporting": "ON_ACCESS",
                "segmentGroupId": "1",
                "segmentGroupName": "Test",
            },
            {
                "creationTime": "1628211456",
                "modifiedBy": "1",
                "id": "2",
                "domainNames": ["test.example.com"],
                "name": "Test B",
                "description": "Test",
                "serverGroups": [
                    {
                        "id": "1",
                        "creationTime": "1625698796",
                        "modifiedBy": "1",
                        "name": "Test",
                        "enabled": True,
                        "configSpace": "DEFAULT",
                        "dynamicDiscovery": False,
                    }
                ],
                "enabled": True,
                "passiveHealthEnabled": True,
                "tcpPortRanges": ["443", "443", "80", "80"],
                "tcpPortRange": [
                    {"from": "443", "to": "443"},
                    {"from": "80", "to": "80"},
                ],
                "doubleEncrypt": False,
                "configSpace": "DEFAULT",
                "bypassType": "NEVER",
                "healthCheckType": "DEFAULT",
                "icmpAccessType": "NONE",
                "isCnameEnabled": True,
                "ipAnchored": False,
                "healthReporting": "ON_ACCESS",
                "segmentGroupId": "1",
                "segmentGroupName": "Test",
            },
        ],
    }

    # Add other methods to handle POST, PUT, DELETE as needed

def assert_responses_exclude_computed(actual_response, expected_response):
    """
    Asserts that the actual response matches the expected response,
    excluding computed attributes like creation_time, modified_by, and modified_time.

    :param actual_response: The actual response (list of dicts)
    :param expected_response: The expected response (list of dicts)
    """
    # Ensure all field names are correctly separated by commas
    computed_fields = {
        'creation_time',
        'modified_by',
        'modified_time',
        'id',
        'certificates',
        'use_custom_sp_metadata',
        'idp_group_id',
        'schema_uri'
    }

    for actual_item, expected_item in zip(actual_response, expected_response):
        for key in expected_item:
            if key not in computed_fields:
                assert actual_item[key] == expected_item[key], f"Mismatch in field: {key}"
