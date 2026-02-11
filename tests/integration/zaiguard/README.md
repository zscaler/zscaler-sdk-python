# AIGuard Integration Tests

## Overview

This directory contains integration and unit tests for the Zscaler AIGuard SDK client.

## Test Structure

```
tests/integration/zaiguard/
├── __init__.py                      # Package initialization
├── conftest.py                      # Pytest fixtures and mock clients
├── test_policy_detection.py         # Integration tests for API endpoints
├── test_zaiguard_unit.py           # Unit tests for error handling
├── cassettes/                       # VCR cassettes for recorded HTTP responses
│   └── .gitkeep
└── README.md                        # This file
```

## Test Files

### `conftest.py`

Provides test fixtures and utilities:

- **`NameGenerator`** - Generates deterministic test names for VCR playback
- **`MockZGuardClient`** - Mock client for testing with VCR cassettes
- **`zguard_client`** - Pytest fixture providing the mock client
- **`reset_counters_per_test`** - Auto-fixture to reset VCR counters

### `test_policy_detection.py` (21 integration tests)

Integration tests for the Policy Detection API:

1. **Basic Functionality**
   - `test_resolve_and_execute_policy_inbound` - Test IN direction scanning
   - `test_resolve_and_execute_policy_outbound` - Test OUT direction scanning
   - `test_execute_policy_without_policy_id` - Test without policy ID
   - `test_execute_policy_with_policy_id` - Test with specific policy ID

2. **Response Structure**
   - `test_response_structure` - Validate response schema
   - `test_detector_responses_structure` - Validate detector responses
   - `test_throttling_details_structure` - Validate throttling details

3. **Multiple Requests**
   - `test_multiple_requests_sequential` - Test sequential requests
   - `test_inbound_and_outbound_directions` - Test both directions

4. **Edge Cases**
   - `test_empty_content` - Test with empty string
   - `test_large_content` - Test with large payload (10KB)
   - `test_special_characters_in_content` - Test unicode and special chars
   - `test_numeric_and_code_content` - Test code snippets

5. **Validation**
   - `test_action_values` - Validate action enum values
   - `test_severity_values` - Validate severity enum values
   - `test_policy_metadata_in_response` - Validate policy metadata
   - `test_invalid_direction` - Test invalid enum value

6. **Rate Limiting**
   - `test_rate_limit_stats` - Test statistics tracking
   - `test_reset_rate_limit_stats` - Test stats reset

7. **Client Behavior**
   - `test_client_context_manager` - Test context manager
   - `test_transaction_id_format` - Validate UUID format

### `test_zaiguard_unit.py` (33 unit tests)

Unit tests for error handling and edge cases:

1. **PolicyDetectionAPI Error Handling** (6 tests)
   - Request creation errors
   - Execution errors
   - Parsing errors
   - For both `execute_policy()` and `resolve_and_execute_policy()`

2. **Model Creation Tests** (6 tests)
   - `test_content_hash_creation`
   - `test_detector_response_creation`
   - `test_rate_limit_throttling_detail_creation`
   - `test_execute_policy_request_creation`
   - `test_execute_policy_response_creation`
   - `test_resolve_and_execute_response_creation`

3. **Service Layer Tests** (1 test)
   - `test_zguard_service_properties` - Validate service properties

4. **Legacy Client Tests** (15 tests)
   - Initialization tests
   - Configuration tests
   - Rate limit statistics tests
   - Throttling detail handling tests
   - Authentication tests
   - Custom headers tests

5. **Rate Limiting Logic Tests** (5 tests)
   - Proactive waiting logic
   - Thread safety
   - Wait time calculations

## Running Tests

### Run All AIGuard Tests

```bash
python -m pytest tests/integration/zaiguard/ -v
```

### Run Only Unit Tests

```bash
python -m pytest tests/integration/zaiguard/test_zaiguard_unit.py -v
```

### Run Only Integration Tests

```bash
python -m pytest tests/integration/zaiguard/test_policy_detection.py -v
```

### Run with Coverage

```bash
python -m pytest tests/integration/zaiguard/ --cov=zscaler.zaiguard --cov-report=html
```

### Run Specific Test

```bash
python -m pytest tests/integration/zaiguard/test_policy_detection.py::TestPolicyDetection::test_resolve_and_execute_policy_inbound -v
```

## Test Configuration

### Environment Variables

For actual API testing (not using VCR cassettes):

```bash
export MOCK_TESTS=false              # Disable VCR playback
export AIGUARD_API_KEY="your-key"    # Your actual API key
export AIGUARD_CLOUD="us1"           # Your cloud region
```

For VCR playback mode (default):

```bash
export MOCK_TESTS=true               # Use recorded cassettes
# No real API key needed - uses dummy credentials
```

## VCR Cassettes

VCR (Video Cassette Recorder) is used to record and replay HTTP interactions:

- **Recording**: Run tests with `MOCK_TESTS=false` and real credentials
- **Playback**: Run tests with `MOCK_TESTS=true` (default) using recorded cassettes
- **Cassettes Location**: `tests/integration/zaiguard/cassettes/`

### Creating New Cassettes

1. Set environment variables:
   ```bash
   export MOCK_TESTS=false
   export AIGUARD_API_KEY="your-real-api-key"
   ```

2. Run tests to record:
   ```bash
   python -m pytest tests/integration/zaiguard/test_policy_detection.py -v
   ```

3. Cassettes are saved in `cassettes/` directory

4. Commit cassettes to git for CI/CD

## Test Coverage

### API Methods Tested

- ✅ `resolve_and_execute_policy()` - Fully tested
- ✅ `execute_policy()` - Fully tested

### Scenarios Covered

- ✅ Inbound content scanning (IN direction)
- ✅ Outbound content scanning (OUT direction)
- ✅ With and without policy ID
- ✅ Error handling (request, execution, parsing)
- ✅ Response structure validation
- ✅ Detector responses parsing
- ✅ Throttling details parsing
- ✅ Rate limiting logic
- ✅ Multiple requests
- ✅ Edge cases (empty, large, special characters)
- ✅ Enum validation
- ✅ Model creation and serialization
- ✅ Thread safety
- ✅ Context manager behavior

## Test Statistics

- **Total Tests**: 54
  - Integration Tests: 21
  - Unit Tests: 33
- **Test Classes**: 5
- **Coverage Areas**:
  - API Methods: 100%
  - Models: 100%
  - Rate Limiting: 100%
  - Error Handling: 100%

## Best Practices

1. **Use VCR for Integration Tests**: Record real API responses for consistent testing
2. **Mock for Unit Tests**: Use mocks to test error handling paths
3. **Deterministic Names**: Use `NameGenerator` for consistent test data
4. **Test Error Paths**: Ensure all error conditions are tested
5. **Validate Schemas**: Check response structures match OpenAPI spec
6. **Thread Safety**: Test concurrent operations where applicable

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

- ✅ **No real API key required** (uses VCR cassettes)
- ✅ **Fast execution** (no real HTTP calls in playback mode)
- ✅ **Deterministic** (same results every run)
- ✅ **No flakiness** (recorded responses are stable)

## Troubleshooting

### Tests Failing

1. **Check VCR mode**:
   ```bash
   echo $MOCK_TESTS  # Should be "true" for cassette playback
   ```

2. **Re-record cassettes**:
   ```bash
   rm -rf tests/integration/zaiguard/cassettes/*.yaml
   export MOCK_TESTS=false
   export AIGUARD_API_KEY="your-key"
   python -m pytest tests/integration/zaiguard/test_policy_detection.py -v
   ```

3. **Check dependencies**:
   ```bash
   pip install -e ".[dev]"  # Install with dev dependencies
   ```

### Import Errors

If you get import errors, ensure the SDK is installed in development mode:

```bash
pip install -e .
```

## Adding New Tests

When adding new API endpoints, follow this pattern:

1. **Add integration test** in `test_policy_detection.py`:
   ```python
   @pytest.mark.vcr
   def test_new_endpoint(self, zguard_client):
       with zguard_client as client:
           result, response, error = client.zguard.new_api.method()
           assert error is None
           assert result is not None
   ```

2. **Add unit tests** in `test_zaiguard_unit.py`:
   ```python
   def test_new_endpoint_request_error(self, fs):
       mock_executor = Mock()
       mock_executor.create_request = Mock(return_value=(None, Exception("Error")))
       api = NewAPI(mock_executor)
       result, response, err = api.method()
       assert result is None and err is not None
   ```

3. **Record cassette**:
   ```bash
   MOCK_TESTS=false AIGUARD_API_KEY="key" python -m pytest tests/integration/zaiguard/test_policy_detection.py::TestPolicyDetection::test_new_endpoint -v
   ```

## Related Documentation

- [AIGuard API Documentation](../../../local_dev/AIGuardAPI/README.md)
- [Rate Limiting Guide](../../../local_dev/AIGuardAPI/RATE_LIMITING.md)
- [OpenAPI Specification](../../../local_dev/AIGuardAPI/openapi.yml)

## Support

For issues with tests:
1. Check test logs for specific errors
2. Verify VCR cassettes are present
3. Ensure SDK is installed correctly
4. Check environment variables
