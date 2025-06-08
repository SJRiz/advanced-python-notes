import logging
import os
import time
from functools import wraps
from datetime import date

# Gets the path to the logs folder
script_dir = os.path.dirname(os.path.abspath(__file__))
logs_folder = os.path.join(script_dir, "logs")
os.makedirs(logs_folder, exist_ok=True)

# Create a new txt file path in the folder
log_file_path = os.path.join(logs_folder, f'logs-{date.today()}.txt')

# Configure the logger to write in the new logs file, and the console
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

with open(log_file_path, "a") as logs:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    logs.write(f'\n--------------- Execution Started at {current_time} -----------------\n')

# Decorator to log the function call
def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Running function \'{func.__name__}\' with arguments {args} and keyword arguments {kwargs}')
        start_time = time.perf_counter()

        try:
            return_val = func(*args, **kwargs)
            logger.info(f'Function \'{func.__name__}\' returned {return_val}.')
            return return_val
        except Exception as err:
            logger.exception(f'Function \'{func.__name__}\' failed with error message: {err}.')
            raise
        finally:
            logger.info(f'Function \'{func.__name__}\' finished with {time.perf_counter() - start_time}s runtime.')

    return wrapper