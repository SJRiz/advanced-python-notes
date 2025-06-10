import os
from collections import namedtuple

Timestamp = namedtuple('Timestamp', ['date', 'time'])

file_path = os.path.dirname(os.path.abspath(__file__))
log_folder = os.path.join(file_path, 'logs')
log_file = os.path.join(log_folder, 'logs-2025-06-09.txt')

def stream_lines(file):
    """Generator that yields the lines of a file"""
    while True:
        line = file.readline()
        if not line:
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

