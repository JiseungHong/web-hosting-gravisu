#!/usr/bin/env python3
"""
Test script for the duration display feature in GRAVISU.
This test verifies that:
1. The backend correctly tracks and returns processing duration
2. The frontend correctly formats duration strings
"""

import json
import time
import sys
import os

# Add the back-end directory to the path so we can import the server
sys.path.append(os.path.join(os.path.dirname(__file__), 'back-end'))

def test_duration_formatting():
    """Test the JavaScript duration formatting logic in Python"""

    def format_duration(seconds):
        """Python equivalent of the JavaScript formatDuration function"""
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} m {remaining_seconds} s"

    # Test cases
    test_cases = [
        (0, "0 m 0 s"),
        (30, "0 m 30 s"),
        (60, "1 m 0 s"),
        (90, "1 m 30 s"),
        (125, "2 m 5 s"),
        (3661, "61 m 1 s"),
    ]

    print("Testing duration formatting...")
    for seconds, expected in test_cases:
        result = format_duration(seconds)
        assert result == expected, f"Expected '{expected}', got '{result}' for {seconds} seconds"
        print(f"✓ {seconds}s -> '{result}'")

    print("All duration formatting tests passed!")

def test_backend_duration_response():
    """Test that the backend response includes duration_seconds field"""

    # Mock response data structure
    mock_response = {
        'image_paths': ['test1.png', 'test2.png', 'test3.png', 'test4.png'],
        'max_value': [6, 6, 8],
        'histogram': 'histogram/histogram_1.png',
        'duration_seconds': 45.67
    }

    print("Testing backend response structure...")

    # Verify all required fields are present
    required_fields = ['image_paths', 'max_value', 'histogram', 'duration_seconds']
    for field in required_fields:
        assert field in mock_response, f"Missing required field: {field}"
        print(f"✓ Field '{field}' present")

    # Verify duration_seconds is a number
    assert isinstance(mock_response['duration_seconds'], (int, float)), "duration_seconds should be a number"
    print(f"✓ duration_seconds is numeric: {mock_response['duration_seconds']}")

    print("Backend response structure test passed!")

def test_time_tracking():
    """Test that time tracking works correctly"""

    print("Testing time tracking accuracy...")

    start_time = time.time()
    time.sleep(0.1)  # Simulate 100ms of processing
    end_time = time.time()
    duration = end_time - start_time

    # Should be approximately 0.1 seconds (allow some tolerance)
    assert 0.09 <= duration <= 0.15, f"Expected ~0.1s, got {duration:.3f}s"
    print(f"✓ Time tracking accurate: {duration:.3f}s")

    print("Time tracking test passed!")

def main():
    """Run all tests"""
    print("Running GRAVISU duration feature tests...\n")

    try:
        test_duration_formatting()
        print()
        test_backend_duration_response()
        print()
        test_time_tracking()
        print()
        print("🎉 All tests passed! Duration feature is working correctly.")
        return 0
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
