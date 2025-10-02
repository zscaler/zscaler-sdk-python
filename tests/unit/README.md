# Rate Limiting and Retry Logic Tests

This directory contains comprehensive unit tests for the rate limiting and retry logic implemented in the Zscaler SDK. The tests are designed to ensure robust handling of rate limiting scenarios across all SDK components.

## Test Structure

### Test Files

- **`test_rate_limiting.py`** - General rate limiting tests covering core functionality
- **`test_request_executor_rate_limiting.py`** - RequestExecutor-specific rate limiting tests
- **`test_legacy_client_rate_limiting.py`** - Legacy client helper rate limiting tests
- **`test_retry_decorator.py`** - Retry decorator functionality tests
- **`mocks.py`** - Mock utilities for simulating rate limiting responses
- **`run_rate_limiting_tests.py`** - Test runner script

### Test Coverage

The tests cover the following scenarios:

#### Rate Limiting Scenarios
- ✅ **429 Too Many Requests** responses
- ✅ **Retry-After header** handling
- ✅ **X-RateLimit-Reset header** handling
- ✅ **ZCC-specific headers** (X-Rate-Limit-Retry-After-Seconds, X-Rate-Limit-Remaining)
- ✅ **Missing rate limit headers** error handling
- ✅ **Invalid header values** error handling
- ✅ **Multiple X-RateLimit-Reset headers** (uses minimum value)
- ✅ **Concurrent rate limiting** (ZCC-specific)
- ✅ **Proactive rate limiting** (backoff before hitting limits)

#### Retry Logic Scenarios
- ✅ **Exponential backoff** with jitter
- ✅ **Maximum retry attempts** enforcement
- ✅ **Retryable vs non-retryable** status codes
- ✅ **Method-specific retry limits** (GET vs POST/PUT/DELETE)
- ✅ **Success after retries** scenarios
- ✅ **Max retries exceeded** scenarios
- ✅ **Custom backoff configuration**

#### Status Code Handling
- ✅ **Success codes** (200-299) - no retry
- ✅ **Client error codes** (400-499) - no retry (except 429)
- ✅ **Server error codes** (500-599) - retry
- ✅ **Rate limiting code** (429) - retry
- ✅ **Boundary conditions** (299, 300)

## Running the Tests

### Prerequisites

```bash
# Install required dependencies
pip install pytest pytest-cov

# Ensure you're in the project root
cd /path/to/zscaler-sdk-python
```

### Running All Tests

```bash
# Run all rate limiting tests
python tests/unit/run_rate_limiting_tests.py

# Run with verbose output
python tests/unit/run_rate_limiting_tests.py --verbose

# Run with coverage reporting
python tests/unit/run_rate_limiting_tests.py --coverage
```

### Running Specific Test Suites

```bash
# Run general rate limiting tests
python tests/unit/run_rate_limiting_tests.py --suite rate_limiting

# Run RequestExecutor tests
python tests/unit/run_rate_limiting_tests.py --suite request_executor

# Run legacy client tests
python tests/unit/run_rate_limiting_tests.py --suite legacy_clients

# Run retry decorator tests
python tests/unit/run_rate_limiting_tests.py --suite retry_decorator
```

### Running Individual Test Files

```bash
# Run specific test file
python -m pytest tests/unit/test_rate_limiting.py -v

# Run with coverage
python -m pytest tests/unit/test_rate_limiting.py --cov=zscaler --cov-report=html
```

## Test Scenarios

### 1. RequestExecutor Rate Limiting

Tests the core rate limiting functionality in the `RequestExecutor` class:

```python
def test_get_retry_after_retry_after_header(self):
    """Test retry after calculation with Retry-After header."""
    headers = {"Retry-After": "60"}
    retry_after = self.request_executor.get_retry_after(headers, Mock())
    assert retry_after == 61  # 60 + 1 second padding
```

**Key Test Cases:**
- Header priority order (Retry-After > X-RateLimit-Reset > RateLimit-Reset)
- Case-insensitive header handling
- Invalid header value handling
- Max retry seconds configuration
- Multiple header scenarios

### 2. Legacy Client Helper Rate Limiting

Tests rate limiting in legacy client helpers:

```python
@patch('requests.Session.get')
def test_proactive_rate_limiting_below_threshold(self, mock_get):
    """Test proactive rate limiting when remaining requests are below threshold."""
    mock_response = MockRateLimitApproachingResponse(remaining=1, limit=100)
    mock_get.return_value = mock_response
    
    with patch('time.sleep') as mock_sleep:
        response = self.helper._get_with_rate_limiting(helper.session, url)
        mock_sleep.assert_called()  # Should have slept due to proactive backoff
```

**Key Test Cases:**
- Proactive rate limiting (backoff before hitting limits)
- 429 response handling with retry logic
- Different header formats (Retry-After, RateLimit-Reset, X-RateLimit-Reset)
- ZCC-specific rate limiting (download endpoints)
- ZWA-specific rate limiting
- ZTW-specific rate limiting

### 3. Retry Decorator Functionality

Tests the `retry_with_backoff` decorator:

```python
@patch('time.sleep')
def test_retry_decorator_exponential_backoff(self, mock_sleep):
    """Test that retry decorator uses exponential backoff with jitter."""
    @retry_with_backoff(method_type="GET", retries=3, backoff_in_seconds=1)
    def mock_request():
        response = Mock()
        response.status_code = 429
        return response
    
    with pytest.raises(Exception):
        mock_request()
    
    # Check exponential backoff: 1s, 2s, 4s + jitter
    assert mock_sleep.call_count == 3
```

**Key Test Cases:**
- Exponential backoff with jitter
- Method-specific retry limits (GET vs POST/PUT/DELETE)
- Status code classification (retryable vs non-retryable)
- Success after retries
- Max retries exceeded
- Custom backoff configuration

## Mock Utilities

The `mocks.py` file provides comprehensive mock utilities for testing:

### Response Mocks
- `MockHTTP429Response` - 429 Too Many Requests
- `MockHTTP429WithRetryAfter` - 429 with Retry-After header
- `MockHTTP429WithXRateLimitReset` - 429 with X-RateLimit-Reset header
- `MockHTTP429ConcurrentLimit` - 429 with concurrent rate limiting
- `MockRateLimitApproachingResponse` - Proactive rate limiting scenarios

### Test Scenarios
- `RATE_LIMIT_SCENARIOS` - Predefined test scenarios
- `DEFAULT_TEST_CONFIG` - Default configuration for tests
- `MockRequestExecutor` - Mock RequestExecutor for testing

## Configuration

### Rate Limiting Configuration

The tests use the following default configuration:

```python
DEFAULT_TEST_CONFIG = {
    "client": {
        "rateLimit": {
            "maxRetries": 3,
            "remainingThreshold": 2,
            "maxRetrySeconds": 300
        }
    }
}
```

### Custom Configuration

Tests can use custom configuration:

```python
custom_config = {
    "client": {
        "rateLimit": {
            "maxRetries": 5,
            "remainingThreshold": 5,
            "maxRetrySeconds": 600
        }
    }
}
```

## Best Practices

### 1. Test Isolation
- Each test is isolated and doesn't depend on others
- Mock external dependencies (HTTP requests, time.sleep)
- Use setup/teardown methods for consistent test state

### 2. Comprehensive Coverage
- Test both success and failure scenarios
- Test edge cases and boundary conditions
- Test different configuration options
- Test error handling and recovery

### 3. Realistic Scenarios
- Use realistic rate limiting headers
- Test with actual HTTP status codes
- Simulate real-world rate limiting scenarios
- Test with different client configurations

### 4. Performance Considerations
- Mock time.sleep to speed up tests
- Use appropriate retry counts for testing
- Test with reasonable backoff values
- Avoid infinite loops in test scenarios

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the project root
   cd /path/to/zscaler-sdk-python
   export PYTHONPATH=$PWD:$PYTHONPATH
   ```

2. **Missing Dependencies**
   ```bash
   pip install pytest pytest-cov
   ```

3. **Test Failures**
   ```bash
   # Run with verbose output to see detailed failure information
   python tests/unit/run_rate_limiting_tests.py --verbose
   ```

4. **Coverage Issues**
   ```bash
   # Run with coverage to see which lines are not covered
   python tests/unit/run_rate_limiting_tests.py --coverage
   ```

### Debug Mode

For debugging specific tests:

```python
# Add debug prints in test methods
def test_specific_scenario(self):
    print("Debug: Starting test")
    # ... test code ...
    print("Debug: Test completed")
```

## Contributing

When adding new rate limiting tests:

1. **Follow the existing pattern** - Use the same structure and naming conventions
2. **Add comprehensive coverage** - Test both success and failure scenarios
3. **Use appropriate mocks** - Leverage existing mock utilities
4. **Document test scenarios** - Add clear docstrings explaining what each test does
5. **Test edge cases** - Include boundary conditions and error scenarios

### Adding New Test Scenarios

1. Create new mock utilities in `mocks.py`
2. Add test methods to appropriate test files
3. Update this README with new scenarios
4. Run tests to ensure they pass
5. Add to CI/CD pipeline if applicable

## References

- [Okta SDK Rate Limiting Tests](https://github.com/okta/okta-sdk-python/tests/unit/test_retry_logic.py) - Inspiration for test structure
- [Zscaler SDK Rate Limiting Implementation](zscaler/request_executor.py) - Core implementation
- [Zscaler SDK Retry Decorator](zscaler/utils.py) - Retry decorator implementation
- [Pytest Documentation](https://docs.pytest.org/) - Testing framework
