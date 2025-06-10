import os
from collections import namedtuple

Timestamp = namedtuple('Timestamp', ['date', 'time'])

file_path = os.path.dirname(os.path.abspath(__file__))
log_folder = os.path.join(file_path, 'logs')
log_file = os.path.join(log_folder, 'logs-2025-06-10.txt')

def stream_lines(file):
    """Generator that yields the lines of a file"""
    while True:
        line = file.readline()
        if not line:
            continue
        print("yielded line")
        yield line

def filter_errors(lines):
    """Generator that yields and filters errors"""
    for line in lines:
        if "ERROR" in line:
            print("yielded error")
            yield line

def find_timestamps(lines):
    """Generator that yields and filters timestamps"""
    for line in lines:
        timestamp = Timestamp(line.split()[0], line.split()[1])
        print("yielded timestamp")
        yield timestamp

with open(log_file) as file:
    lines = stream_lines(file)
    errors = filter_errors(lines)
    timestamps = find_timestamps(errors)
    for timestamp in timestamps:
        print(f'Error on {timestamp.date} at {timestamp.time}')
