import os
import time
from collections import namedtuple
from datetime import date

# Tuple for the timestamp
Timestamp = namedtuple('Timestamp', ['date', 'time'])

# Get the path to the current log file
file_path = os.path.dirname(os.path.abspath(__file__))
log_folder = os.path.join(file_path, 'logs')
log_file = os.path.join(log_folder, f'logs-{date.today()}.txt')

def stream_lines(file):
    """Generator that yields the lines of a file"""
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue

        yield line

def filter_errors(lines):
    """Generator that yields and filters errors"""
    for line in lines:
        if "ERROR" in line:
            yield line

def find_timestamps(lines):
    """Generator that yields and filters timestamps"""
    for line in lines:
        timestamp = Timestamp(line.split()[0], line.split()[1])
        yield timestamp

# Constantly watch a log file
with open(log_file) as file:
    lines = stream_lines(file)
    errors = filter_errors(lines)
    timestamps = find_timestamps(errors)

    for timestamp in timestamps:
        print(f'Error on {timestamp.date} at {timestamp.time}')
