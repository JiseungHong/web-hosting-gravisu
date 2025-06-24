#!/usr/bin/env python3
"""
Integration test for the GRAVISU duration feature.
This test starts the server and tests the actual API endpoints.
"""

import requests
import json
import time
import subprocess
import signal
import os
import sys
from threading import Thread

def start_server():
    """Start the FastAPI server in the background"""
    os.chdir('/workspace')
    # Use the minimal test server
    cmd = [sys.executable, 'test_server_minimal.py']
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def test_api_endpoints():
    """Test the API endpoints to ensure duration is returned"""
    base_url = "http://127.0.0.1:8001"

    # Wait for server to start
    print("Waiting for server to start...")
    for i in range(10):
        try:
            response = requests.get(f"{base_url}/hello", timeout=2)
            if response.status_code == 200:
                print("Server is ready!")
                break
        except requests.exceptions.RequestException:
            time.sleep(1)
    else:
        raise Exception("Server failed to start")

    # Test the /test endpoint
    print("Testing /test endpoint...")
    response = requests.post(f"{base_url}/test")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

    # Verify the response contains duration_seconds
    assert 'duration_seconds' in data, "Response missing duration_seconds field"
    assert isinstance(data['duration_seconds'], (int, float)), "duration_seconds should be numeric"
    assert data['duration_seconds'] == 150.0, f"Expected 150.0, got {data['duration_seconds']}"

    print("✓ /test endpoint returns duration correctly")

    # Test that other required fields are still present
    required_fields = ['image_paths', 'max_value', 'histogram']
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    print("✓ All required fields present in response")

    # Test the /run-gradcam endpoint
    print("Testing /run-gradcam endpoint...")
    response = requests.post(f"{base_url}/run-gradcam")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

    # Verify the response contains duration_seconds
    assert 'duration_seconds' in data, "Response missing duration_seconds field"
    assert isinstance(data['duration_seconds'], (int, float)), "duration_seconds should be numeric"
    assert data['duration_seconds'] > 0, f"Duration should be positive, got {data['duration_seconds']}"

    print("✓ /run-gradcam endpoint returns duration correctly")

    # Test that other required fields are still present
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    print("✓ All required fields present in /run-gradcam response")
    print("Integration test passed!")

def main():
    """Run the integration test"""
    print("Starting GRAVISU duration feature integration test...\n")

    server_process = None
    try:
        # Start the server
        server_process = start_server()

        # Give the server time to start
        time.sleep(3)

        # Run the tests
        test_api_endpoints()

        print("\n🎉 Integration test completed successfully!")
        return 0

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return 1

    finally:
        # Clean up: stop the server
        if server_process:
            server_process.terminate()
            server_process.wait()
            print("Server stopped.")

if __name__ == "__main__":
    exit(main())
