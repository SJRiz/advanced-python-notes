from logger import log_function_call

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
add2(3,6)