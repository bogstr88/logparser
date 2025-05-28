import csv
import sys
from datetime import datetime
from collections import defaultdict

TIME_FORMAT = '%H:%M:%S'

def parse_log(file_path):
    jobs = defaultdict(dict)
    durations = []
    unmatched_starts = []

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
                        continue 

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

    # Any jobs without END time
    for pid, info in jobs.items():
        unmatched_starts.append({
            "description": info["desc"],
            "pid": pid,
            "start": info["start"]
        })

    return durations, unmatched_starts

def analyze_durations(durations, unmatched_starts):
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

    if unmatched_starts:
        print("\n  Tasks that started but did not end:")
        for job in unmatched_starts:
            print(
                f"INCOMPLETE - {job['description']} (PID {job['pid']}) started at {job['start'].time()}"
            )

if __name__ == "__main__":
    LOG_FILE_PATH = sys.argv[1]
    durations, unmatched_starts = parse_log(LOG_FILE_PATH)
    analyze_durations(durations, unmatched_starts)
