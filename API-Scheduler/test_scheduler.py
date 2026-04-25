# test_scheduler.py file to test main class and functions

import unittest
from unittest.mock import patch, Mock
import scheduler

class TestScheduler(unittest.TestCase):
    def test_formatting_time(self):
        result = scheduler.Formatting_Time("14:02:05")
        self.assertEqual(result.hour, 14)
        self.assertEqual(result.minute, 2)
        self.assertEqual(result.second, 5)
    
    @patch("scheduler.requests.get")
    def test_hitting_url_works(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_get.return_value = mock_resp
        
        scheduler.Hitting_url("00:00:00")  # Use "00:00:00" so the loop exit immediately
        
        mock_get.assert_called_once_with(scheduler.url)
    
    @patch("scheduler.requests.get")
    def test_hitting_url_fails(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 500
        mock_get.return_value = mock_resp
        
        # checking no exception & request
        scheduler.Hitting_url("00:00:00")
        mock_get.assert_called_once()
    
    @patch("scheduler.requests.get")
    def test_exception_handling(self, mock_get):
        mock_get.side_effect = Exception("Networek connection error")
        try:
            scheduler.Hitting_url("00:00:00")
        except:
            self.fail("exception not raise")
    
    @patch("scheduler.threading.Thread")
    @patch("builtins.input")
    def test_main_creates_threads(self, mock_input, mock_thread):
        
        mock_input.return_value = "14:02:05,14:02:10"  # usser entersing two timestamps
        mock_t = Mock()
        mock_thread.return_value = mock_t
        scheduler.main()
        # expect exasctly two threads createds and started
        self.assertEqual(mock_thread.call_count, 2)
        self.assertEqual(mock_t.start.call_count, 2)

if __name__ == "__main__":
    unittest.main()