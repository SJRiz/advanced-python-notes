import logging
import os
import time
from functools import wraps
from datetime import date

if __name__ == "__main__":

    # Gets the path to the logs folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_folder = os.path.join(script_dir, "logs")

    # Create a new txt file path in the folder
    log_file_path = os.path.join(logs_folder, f'logs-{date.today()}.txt')

    # Configure the logger to write in the new logs file
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', filename=log_file_path, encoding='utf-8', level=logging.DEBUG)

    with open(log_file_path, "a") as logs:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        logs.write(f'\n--------------- Execution Started at {current_time} -----------------\n')

# Decorator to log the function call
def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Running function \'{func.__name__}\' with arguments {args} and keyword arguments {kwargs}')
        start_time = time.time()

        try:
            return_val = func(*args, **kwargs)
            logger.info(f'Function \'{func.__name__}\' returned {return_val}.')
        except Exception as err:
            logger.critical(f'Function \'{func.__name__}\' failed with error message: {err}.')
        finally:
            logger.info(f'Function \'{func.__name__}\' finished with {time.time() - start_time}s runtime.')

    return wrapper

########################################################################################################

@log_function_call
def add(x, y):
    for _ in range(10000000):
        pass
    return x + y

@log_function_call
def add2(x, y):
    for i in range(10000000):
        pass
    return x + y

add(3,4)
add2(3)