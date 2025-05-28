import csv
import sys
from datetime import datetime
from collections import defaultdict

TIME_FORMAT = '%H:%M:%S'

def parse_log(file_path):
    jobs = defaultdict(dict)
    durations = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            timestamp_str, description, event, pid = row
            timestamp = datetime.strptime(timestamp_str.strip(), TIME_FORMAT)

            if event.lstrip() == "START":
                jobs[pid]["start"] = timestamp
                jobs[pid]["desc"] = description
            elif event.lstrip() == "END":
                if pid in jobs and "start" in jobs[pid]:
                    start_time = jobs[pid]["start"]
                    if timestamp < start_time:
                        print(f"ERROR - END time earlier than START time for PID {pid}: {timestamp.time()} < {start_time.time()}")
                        continue  # Skip this invalid entry

                    duration = timestamp - start_time
                    durations.append({
                        "description": jobs[pid]["desc"],
                        "pid": pid,
                        "start": start_time,
                        "end": timestamp,
                        "duration": duration
                    })
                    del jobs[pid]
                else:
                    print(f"Unmatched END for PID {pid} at {timestamp_str}")
    return durations

def analyze_durations(durations):
    for job in durations:
        minutes = job["duration"].total_seconds() / 60
        status = ""
        if minutes > 10:
            status = "ERROR"
        elif minutes > 5:
            status = "WARNING"

        status_line = f"{status} - " if status else ""
        print(
            f"{status_line}{job['description']} (PID {job['pid']}) "
            f"took {job['duration']} from {job['start'].time()} to {job['end'].time()}"
        )

if __name__ == "__main__":
    LOG_FILE_PATH = sys.argv[1]
    durations = parse_log(LOG_FILE_PATH)
    analyze_durations(durations)
