import pytest
import os
import json

from pytest_recording._vcr import use_cassette

PYTEST_MOCK_CLIENT = "pytest_mock_client"
PYTEST_RE_RECORD = "record_mode"
MOCK_TESTS = 'MOCK_TESTS'

# Environment Variable for Mock Tests
def is_mock_tests_flag_true():
    """Return True by default, i.e. variable is not set.
    Return False if env variable `MOCK_TESTS` is set to `false`, `FALSE`, etc.
    Return True in all other cases.
    """
    return os.environ.get('MOCK_TESTS', 'true').strip().lower() != 'false'

# Override vcr fixture from pytest_recording library
@pytest.fixture(autouse=True)
def vcr(request, vcr_markers, vcr_cassette_dir, record_mode, pytestconfig):
    if vcr_markers and is_mock_tests_flag_true():
        config = request.getfixturevalue("vcr_config")
        default_cassette = request.getfixturevalue("default_cassette_name")
        with use_cassette(
            default_cassette,
            vcr_cassette_dir,
            record_mode,
            vcr_markers,
            config,
            pytestconfig
        ) as cassette:
            yield cassette
    else:
        yield None

def pytest_generate_tests(metafunc):
    ''' just to attach the cmd-line args to a test-class that needs them '''
    record_mode = metafunc.config.getoption(PYTEST_RE_RECORD)
    # check if this function is in a test-class that needs the cmd-line args
    if record_mode == "rewrite":
        os.environ[PYTEST_MOCK_CLIENT] = "1"


# @pytest.fixture(scope='module')
# def vcr_config():
#     return {
#         # Remove personal details from Integration Tests
#         "before_record_request": before_record_request,
#         "before_record_response": before_record_response
#     }

# def before_record_request(request):
#     # Sanitize sensitive information in headers
#     # This is generally more relevant for responses, as the token is usually not in the request
#     return request


# def before_record_response(response):
#     # Check if this is a response to the login request
#     if 'signin' in response['url']:
#         # Assuming the token is in the response body as a JSON field
#         if response['body']['string']:
#             body = json.loads(response['body']['string'])
#             if 'access_token' in body:
#                 # Replace the actual token with a placeholder
#                 body['access_token'] = 'BEARER_TOKEN_PLACEHOLDER'
#                 response['body']['string'] = json.dumps(body)

#     # Sanitize other headers or body content as needed

#     return response


# Cleanup function to run at the end of tests
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """
    To run at the end of a test run
    """
    def clean_up_env_vars():
        if PYTEST_MOCK_CLIENT in os.environ:
            del os.environ[PYTEST_MOCK_CLIENT]
    request.addfinalizer(clean_up_env_vars)
