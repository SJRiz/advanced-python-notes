import functools
import logging
import os

# Gets the path to the logging-framework folder
script_dir = os.path.dirname(os.path.abspath(__file__))
# Put the logs.txt in this folder
log_path = os.path.join(script_dir, "logs.txt")

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', filename=log_path, encoding='utf-8', level=logging.DEBUG)

# Clear the logs.txt or make a new one if it doesnt exist
if __name__ == "__main__":
    with open(log_path, "w") as logs:
        logs.write("")

# Decorator to log the function call
def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Running function \'{func.__name__}\' with arguments {args} and keyword arguments {kwargs}')
        return_val = func(*args, **kwargs)
        logger.info(f'Function \'{func.__name__}\' finished and returned {return_val}')
    return wrapper

@log_function_call
def add(x, y):
    return x + y

add(3,4)