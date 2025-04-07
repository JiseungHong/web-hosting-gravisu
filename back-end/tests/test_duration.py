import unittest
import re

class TestDuration(unittest.TestCase):
    
    def test_duration_format(self):
        """Test that the duration format matches 'XX m XX s'"""
        # Simulate a duration calculation
        elapsed_time = 125  # 2 minutes and 5 seconds
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        duration = f"{minutes} m {seconds} s"
        
        # Check if the duration format is correct (XX m XX s)
        self.assertTrue(re.match(r'\d+ m \d+ s', duration))
        self.assertEqual(minutes, 2)
        self.assertEqual(seconds, 5)
        
        # Test another duration
        elapsed_time = 3723  # 1 hour, 2 minutes, 3 seconds
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        duration = f"{minutes} m {seconds} s"
        
        self.assertTrue(re.match(r'\d+ m \d+ s', duration))
        self.assertEqual(minutes, 62)
        self.assertEqual(seconds, 3)

if __name__ == '__main__':
    unittest.main()

