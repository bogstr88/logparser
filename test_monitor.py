import unittest
from datetime import datetime, timedelta
from monitor import analyze_durations

class TestMonitor(unittest.TestCase):
    def test_warning_and_error_thresholds(self):
        durations = [
            {
                "description": "scheduled task test",
                "pid": "12345",
                "start": datetime.strptime("11:00:00", "%H:%M:%S"),
                "end": datetime.strptime("11:06:00", "%H:%M:%S"),
                "duration": timedelta(minutes=6)
            },
            {
                "description": "scheduled task long",
                "pid": "67890",
                "start": datetime.strptime("11:00:00", "%H:%M:%S"),
                "end": datetime.strptime("11:12:00", "%H:%M:%S"),
                "duration": timedelta(minutes=12)
            },
            {
                "description": "duration should be negative when end < start",
                "pid": "9990",
                "start": datetime.strptime("12:00:00", "%H:%M:%S"),
                "end": datetime.strptime("11:12:00", "%H:%M:%S"),
                "duration": timedelta(minutes=48)
            }
        ]
        analyze_durations(durations, [])

if __name__ == '__main__':
    unittest.main()
