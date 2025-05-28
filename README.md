# Log Monitoring Application

## Description

This Python application reads a `logs.log` file, tracks each job’s start and end time, calculates their duration, and outputs:

- **WARNING** if a job exceeds **5 minutes**
- **ERROR** if a job exceeds **10 minutes**

## File Structure

- `monitor.py` – Main log monitoring script.
- `test_monitor.py` – Basic unit test for validation.
- `logs.log` – Sample input log file.
- `requirements.txt` – Setting up the minimum version for python
- `README.md` – This file.

## Usage

```bash
python monitor.py logs.log
```

Output is printed to the console.

## Run Tests

```bash
python -m unittest test_monitor.py
```

## Output Example

```bash
WARNING - scheduled task 105 (PID 12345) took 0:06:00 from 11:00:00 to 11:06:00
ERROR - scheduled task 999 (PID 67890) took 0:12:00 from 11:00:00 to 11:12:00
ERROR - END time earlier than START time for PID 99999: 12:00:00 <  12:10:00
```

## Requirements

- Python 3.x
