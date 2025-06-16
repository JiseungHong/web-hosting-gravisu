#!/usr/bin/env python3
"""
Test client to verify the duration feature
"""

import requests
import json

def test_duration_feature():
    base_url = "http://localhost:8000"

    print("Testing GRAVISU Duration Feature")
    print("=" * 40)

    # Test the /test endpoint
    print("\n1. Testing /test endpoint...")
    try:
        response = requests.post(f"{base_url}/test", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Response received: {response.status_code}")
            print(f"✓ Duration included: {'duration_seconds' in data}")
            if 'duration_seconds' in data:
                duration = data['duration_seconds']
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                print(f"✓ Duration: {duration} seconds ({minutes} m {seconds} s)")
            print(f"✓ Response keys: {list(data.keys())}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test the /run-gradcam endpoint
    print("\n2. Testing /run-gradcam endpoint...")
    try:
        response = requests.post(f"{base_url}/run-gradcam", timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Response received: {response.status_code}")
            print(f"✓ Duration included: {'duration_seconds' in data}")
            if 'duration_seconds' in data:
                duration = data['duration_seconds']
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                print(f"✓ Duration: {duration:.2f} seconds ({minutes} m {seconds} s)")
            print(f"✓ Response keys: {list(data.keys())}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_duration_formatting():
    print("\n3. Testing duration formatting...")

    def format_duration(seconds):
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} m {remaining_seconds} s"

    test_cases = [
        (0, "0 m 0 s"),
        (30, "0 m 30 s"),
        (60, "1 m 0 s"),
        (90, "1 m 30 s"),
        (125, "2 m 5 s"),
        (3661, "61 m 1 s"),
    ]

    all_passed = True
    for seconds, expected in test_cases:
        result = format_duration(seconds)
        passed = result == expected
        all_passed = all_passed and passed
        status = "✓" if passed else "✗"
        print(f"{status} {seconds}s → '{result}' (expected: '{expected}')")

    print(f"\n{'✓ All formatting tests passed!' if all_passed else '✗ Some formatting tests failed!'}")

if __name__ == "__main__":
    test_duration_formatting()
    test_duration_feature()
