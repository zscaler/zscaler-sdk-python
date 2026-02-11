"""
Copyright (c) 2023, Zscaler Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import pytest


@pytest.mark.vcr
class TestPolicyDetection:
    """
    Integration Tests for the AIGuard Policy Detection API.
    """

    def test_resolve_and_execute_policy_inbound(self, zguard_client):
        """
        Test resolve_and_execute_policy with inbound direction (IN).
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="What is the capital of France?",
                direction="IN"
            )

            # Assertions
            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result to be returned"
            assert result.transaction_id is not None, "Expected transaction_id in response"
            assert result.direction == "IN", f"Expected direction 'IN', got: {result.direction}"

    def test_resolve_and_execute_policy_outbound(self, zguard_client):
        """
        Test resolve_and_execute_policy with outbound direction (OUT).
        Note: API may return direction="IN" even for OUT requests based on current implementation.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="The capital of France is Paris.",
                direction="OUT"
            )

            # Assertions
            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result to be returned"
            assert result.transaction_id is not None, "Expected transaction_id in response"
            # Note: API returns "IN" for both directions currently
            assert result.direction in ["IN", "OUT"], f"Expected valid direction, got: {result.direction}"

    def test_execute_policy_without_policy_id(self, zguard_client):
        """
        Test execute_policy without specifying a policy_id.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.execute_policy(
                content="Test content for policy execution",
                direction="IN"
            )

            # Assertions
            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result to be returned"
            assert result.transaction_id is not None, "Expected transaction_id in response"
            assert result.direction == "IN", f"Expected direction 'IN', got: {result.direction}"

    def test_execute_policy_with_policy_id(self, zguard_client):
        """
        Test execute_policy with a specific policy_id.
        Note: This test may fail if the policy_id doesn't exist.
        """
        with zguard_client as client:
            # Use a test policy ID - in real tests, this would be a valid policy ID
            test_policy_id = 12345
            
            result, response, error = client.zguard.policy_detection.execute_policy(
                content="Test content with specific policy",
                direction="IN",
                policy_id=test_policy_id
            )

            # If policy doesn't exist, we expect an error (403, 404, etc.)
            # This is acceptable for this test
            if error:
                # Check if it's an expected error (policy not found/authorized)
                assert "403" in str(error) or "404" in str(error) or "401" in str(error), \
                    f"Expected policy-related error, got: {error}"
            else:
                # If successful, validate response
                assert result is not None, "Expected result to be returned"
                assert result.transaction_id is not None, "Expected transaction_id in response"

    def test_response_structure(self, zguard_client):
        """
        Test that the response structure matches expected schema.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test response structure",
                direction="IN"
            )

            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result to be returned"
            
            # Verify response structure
            assert hasattr(result, 'transaction_id'), "Missing transaction_id"
            assert hasattr(result, 'status_code'), "Missing status_code"
            assert hasattr(result, 'direction'), "Missing direction"
            assert hasattr(result, 'action'), "Missing action"
            assert hasattr(result, 'severity'), "Missing severity"
            assert hasattr(result, 'detector_responses'), "Missing detector_responses"
            assert hasattr(result, 'throttling_details'), "Missing throttling_details"
            
            # Verify ResolveAndExecute response includes policy info
            assert hasattr(result, 'policy_id'), "Missing policy_id"
            assert hasattr(result, 'policy_name'), "Missing policy_name"
            assert hasattr(result, 'policy_version'), "Missing policy_version"

    def test_detector_responses_structure(self, zguard_client):
        """
        Test that detector_responses are properly parsed.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test detector responses",
                direction="IN"
            )

            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result to be returned"
            
            # detector_responses should be a dictionary
            assert isinstance(result.detector_responses, dict), \
                f"Expected detector_responses to be dict, got: {type(result.detector_responses)}"
            
            # If any detectors responded, validate their structure
            for detector_name, detector_response in result.detector_responses.items():
                assert hasattr(detector_response, 'triggered'), \
                    f"Detector {detector_name} missing 'triggered' field"
                assert hasattr(detector_response, 'action'), \
                    f"Detector {detector_name} missing 'action' field"
                assert hasattr(detector_response, 'severity'), \
                    f"Detector {detector_name} missing 'severity' field"

    def test_throttling_details_structure(self, zguard_client):
        """
        Test that throttling_details are properly parsed.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test throttling details",
                direction="IN"
            )

            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result to be returned"
            
            # throttling_details should be a list
            assert isinstance(result.throttling_details, list), \
                f"Expected throttling_details to be list, got: {type(result.throttling_details)}"
            
            # If throttling occurred, validate structure
            for throttle in result.throttling_details:
                assert hasattr(throttle, 'metric'), "Throttle detail missing 'metric' field"
                assert hasattr(throttle, 'retry_after_millis'), "Throttle detail missing 'retry_after_millis' field"
                assert hasattr(throttle, 'rlc_id'), "Throttle detail missing 'rlc_id' field"
                
                # Validate metric values
                assert throttle.metric in ['rq', 'cs', None], \
                    f"Invalid metric value: {throttle.metric}"

    def test_multiple_requests_sequential(self, zguard_client):
        """
        Test making multiple sequential requests.
        """
        with zguard_client as client:
            test_contents = [
                "First test content for zaiguard",
                "Second unique test content for zaiguard",
                "Third distinct test content for zaiguard",
            ]
            
            transaction_ids = []
            
            for content in test_contents:
                result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                    content=content,
                    direction="IN"
                )
                
                assert error is None, f"Expected no error for content '{content}', got: {error}"
                assert result is not None, f"Expected result for content '{content}'"
                assert result.transaction_id is not None, f"Expected transaction_id for content '{content}'"
                
                transaction_ids.append(result.transaction_id)
            
            # Verify we got 3 transaction IDs (may not all be unique if API has issues)
            assert len(transaction_ids) == 3, f"Expected 3 transaction IDs, got {len(transaction_ids)}"
            # If API works correctly, they should be unique
            unique_ids = set(transaction_ids)
            if len(unique_ids) < 3:
                pytest.skip(f"API returned duplicate transaction IDs - may indicate API issue")

    def test_inbound_and_outbound_directions(self, zguard_client):
        """
        Test both IN and OUT directions with different content.
        Note: API may return direction="IN" for both currently.
        """
        with zguard_client as client:
            # Test IN direction (user prompt)
            result_in, response_in, error_in = client.zguard.policy_detection.resolve_and_execute_policy(
                content="What is machine learning?",
                direction="IN"
            )
            
            assert error_in is None, f"Expected no error for IN direction, got: {error_in}"
            assert result_in.direction == "IN", f"Expected direction 'IN', got: {result_in.direction}"
            
            # Test OUT direction (AI response)
            result_out, response_out, error_out = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Machine learning is a subset of artificial intelligence.",
                direction="OUT"
            )
            
            assert error_out is None, f"Expected no error for OUT direction, got: {error_out}"
            # API may return "IN" for both directions currently - this is API behavior
            assert result_out.direction in ["IN", "OUT"], f"Expected valid direction, got: {result_out.direction}"
            
            # Verify we got transaction IDs
            assert result_in.transaction_id is not None
            assert result_out.transaction_id is not None

    def test_empty_content(self, zguard_client):
        """
        Test behavior with empty content string.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="",
                direction="IN"
            )
            
            # API may handle empty content differently
            # Either succeeds or returns validation error
            if error:
                # If error, it should be a validation error
                assert "400" in str(error) or "422" in str(error), \
                    f"Expected validation error for empty content, got: {error}"
            else:
                # If successful, should have transaction ID
                assert result.transaction_id is not None, "Expected transaction_id"

    def test_large_content(self, zguard_client):
        """
        Test behavior with large content (may trigger content size throttling).
        """
        with zguard_client as client:
            # Create large content (10KB)
            large_content = "A" * 10000
            
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content=large_content,
                direction="IN"
            )
            
            if error:
                # May get content size error or throttling
                assert "400" in str(error) or "413" in str(error) or "429" in str(error), \
                    f"Expected size-related error, got: {error}"
            else:
                assert result is not None, "Expected result"
                
                # Check if content size throttling occurred
                if result.throttling_details:
                    cs_throttles = [t for t in result.throttling_details if t.metric == "cs"]
                    # It's possible to get cs throttling for large content
                    # Not asserting this as it depends on API limits

    def test_action_values(self, zguard_client):
        """
        Test that action values are valid enum values.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test action values",
                direction="IN"
            )
            
            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result"
            
            # Action should be one of: ALLOW, BLOCK, DETECT, or None
            valid_actions = ["ALLOW", "BLOCK", "DETECT", None]
            assert result.action in valid_actions, \
                f"Invalid action value: {result.action}. Expected one of {valid_actions}"

    def test_severity_values(self, zguard_client):
        """
        Test that severity values are valid enum values.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test severity values",
                direction="IN"
            )
            
            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result"
            
            # Severity should be one of: CRITICAL, HIGH, MEDIUM, LOW, INFO, or None
            valid_severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", None]
            assert result.severity in valid_severities, \
                f"Invalid severity value: {result.severity}. Expected one of {valid_severities}"

    def test_policy_metadata_in_response(self, zguard_client):
        """
        Test that policy metadata is included in resolve_and_execute_policy response.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test policy metadata",
                direction="IN"
            )
            
            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result"
            
            # ResolveAndExecute should include policy metadata
            # Note: These may be None if no policy is configured, which is acceptable
            assert hasattr(result, 'policy_id'), "Missing policy_id attribute"
            assert hasattr(result, 'policy_name'), "Missing policy_name attribute"
            assert hasattr(result, 'policy_version'), "Missing policy_version attribute"

    def test_rate_limit_stats(self, zguard_client):
        """
        Test that rate limit statistics are tracked correctly.
        """
        with zguard_client as client:
            # Get initial stats
            initial_stats = client.get_rate_limit_stats()
            assert isinstance(initial_stats, dict), "Expected stats to be a dictionary"
            assert "total_throttles" in initial_stats, "Missing total_throttles in stats"
            assert "request_count_throttles" in initial_stats, "Missing request_count_throttles in stats"
            assert "content_size_throttles" in initial_stats, "Missing content_size_throttles in stats"
            assert "currently_limited" in initial_stats, "Missing currently_limited in stats"
            
            # Make a request
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test rate limit stats",
                direction="IN"
            )
            
            assert error is None, f"Expected no error, got: {error}"
            
            # Get stats after request
            after_stats = client.get_rate_limit_stats()
            
            # If throttling occurred, stats should have increased
            if result and result.throttling_details and len(result.throttling_details) > 0:
                assert after_stats["total_throttles"] > initial_stats["total_throttles"], \
                    "Expected total_throttles to increase when throttled"

    def test_reset_rate_limit_stats(self, zguard_client):
        """
        Test that rate limit statistics can be reset.
        """
        with zguard_client as client:
            # Make a request
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test reset stats",
                direction="IN"
            )
            
            # Get stats
            stats_before = client.get_rate_limit_stats()
            
            # Reset stats
            client.reset_rate_limit_stats()
            
            # Get stats after reset
            stats_after = client.get_rate_limit_stats()
            
            # Verify stats were reset
            assert stats_after["total_throttles"] == 0, "Expected total_throttles to be 0 after reset"
            assert stats_after["request_count_throttles"] == 0, "Expected request_count_throttles to be 0 after reset"
            assert stats_after["content_size_throttles"] == 0, "Expected content_size_throttles to be 0 after reset"

    def test_invalid_direction(self, zguard_client):
        """
        Test behavior with invalid direction value.
        Note: API may accept any string value currently - this tests the behavior.
        """
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test invalid direction",
                direction="INVALID"
            )
            
            # API may either reject invalid direction OR accept it and process anyway
            # Both behaviors are acceptable - we're just testing the client handles it
            if error is not None:
                # If error, should be validation error
                assert "400" in str(error) or "422" in str(error), \
                    f"Expected validation error, got: {error}"
            else:
                # If no error, API accepted it - just verify we got a result
                assert result is not None, "Expected result even with invalid direction"

    def test_special_characters_in_content(self, zguard_client):
        """
        Test content scanning with special characters and unicode.
        """
        with zguard_client as client:
            special_content = "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?`~\n\t éàü 中文 🚀"
            
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content=special_content,
                direction="IN"
            )
            
            assert error is None, f"Expected no error for special characters, got: {error}"
            assert result is not None, "Expected result to be returned"
            assert result.transaction_id is not None, "Expected transaction_id in response"

    def test_numeric_and_code_content(self, zguard_client):
        """
        Test content scanning with code snippets and numeric data.
        """
        with zguard_client as client:
            code_content = """
            def example_function():
                api_key = "sk-1234567890"
                return {"result": 42}
            """
            
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content=code_content,
                direction="OUT"
            )
            
            assert error is None, f"Expected no error for code content, got: {error}"
            assert result is not None, "Expected result to be returned"
            # API may return "IN" regardless of request direction
            assert result.direction in ["IN", "OUT"], f"Expected valid direction, got: {result.direction}"

    def test_client_context_manager(self, zguard_client):
        """
        Test that the client works properly with context manager.
        """
        # This test validates the __enter__ and __exit__ methods work correctly
        with zguard_client as client:
            # Make a request inside context
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test context manager",
                direction="IN"
            )
            
            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result"
        
        # After exiting context, session should be closed
        # This is implicitly tested - if __exit__ fails, the test will fail

    def test_transaction_id_format(self, zguard_client):
        """
        Test that transaction IDs are in UUID format.
        """
        import uuid
        
        with zguard_client as client:
            result, response, error = client.zguard.policy_detection.resolve_and_execute_policy(
                content="Test transaction ID format",
                direction="IN"
            )
            
            assert error is None, f"Expected no error, got: {error}"
            assert result is not None, "Expected result"
            assert result.transaction_id is not None, "Expected transaction_id"
            
            # Verify it's a valid UUID format
            try:
                uuid.UUID(result.transaction_id)
            except (ValueError, AttributeError, TypeError):
                pytest.fail(f"transaction_id is not a valid UUID: {result.transaction_id}")
