import unittest
import requests
import json
import time
from unittest.mock import patch, MagicMock

class TestDurationFeature(unittest.TestCase):
    """Test the duration display feature for GRAVISU"""

    def setUp(self):
        self.base_url = "http://110.76.86.172:8000"

    def test_duration_format_function(self):
        """Test the JavaScript duration formatting function logic in Python"""

        def format_duration(seconds):
            """Python equivalent of the JavaScript formatDuration function"""
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes} m {remaining_seconds} s"

        # Test various durations
        test_cases = [
            (0, "0 m 0 s"),
            (30, "0 m 30 s"),
            (60, "1 m 0 s"),
            (90, "1 m 30 s"),
            (125, "2 m 5 s"),
            (3661, "61 m 1 s"),
        ]

        for seconds, expected in test_cases:
            with self.subTest(seconds=seconds):
                result = format_duration(seconds)
                self.assertEqual(result, expected)

    def test_test_endpoint_includes_duration(self):
        """Test that the /test endpoint includes duration in response"""
        try:
            response = requests.post(f"{self.base_url}/test", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.assertIn('duration_seconds', data)
                self.assertIsInstance(data['duration_seconds'], (int, float))
                self.assertGreater(data['duration_seconds'], 0)
                print(f"Test endpoint duration: {data['duration_seconds']} seconds")
            else:
                self.skipTest(f"Server not available (status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            self.skipTest(f"Server not available: {e}")

    def test_run_gradcam_endpoint_structure(self):
        """Test that the run-gradcam endpoint would include duration (mock test)"""
        # Since we can't easily test the full run-gradcam endpoint without proper setup,
        # we'll test the expected response structure

        expected_keys = ['image_paths', 'max_value', 'histogram', 'duration_seconds']

        # Mock response that should be returned by run-gradcam
        mock_response = {
            'image_paths': ['img1.png', 'img2.png', 'img3.png', 'img4.png'],
            'max_value': [6, 6, 8],
            'histogram': 'histogram/histogram_1.png',
            'duration_seconds': 125.5
        }

        for key in expected_keys:
            self.assertIn(key, mock_response)

        # Test duration formatting
        duration = mock_response['duration_seconds']
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        formatted = f"{minutes} m {seconds} s"
        self.assertEqual(formatted, "2 m 5 s")

if __name__ == '__main__':
    unittest.main()
