import unittest
import time

class TestProcessingTime(unittest.TestCase):
    """Test the processing time feature of the GRAVISU application."""
    
    def test_processing_time_format(self):
        """Test that the processing time format is correct."""
        # Simulate a processing time
        start_time = time.time() - 65  # 1 minute and 5 seconds ago
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Format the time as required
        minutes = int(processing_time // 60)
        seconds = int(processing_time % 60)
        time_str = f"{minutes} m {seconds} s"
        
        # Check if the format is correct
        self.assertRegex(time_str, r'\d+ m \d+ s')
        self.assertTrue(minutes >= 1)  # At least 1 minute
        self.assertTrue(0 <= seconds < 60)  # Between 0 and 59 seconds
        
        print(f"Processing time: {time_str}")
        
if __name__ == '__main__':
    unittest.main()
