import time
max_retries = 15
delay = 1
exception = Exception
def validate_with_retry(max_retries = max_retries, delay=delay, exceptions=exception):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Exception thrown when attempting to run {func.__name__}, attempt {attempt + 1} of {max_retries}: {e}")
                    time.sleep(delay)
            raise Exception("Maximum retries exceeded. Function failed.")
        return wrapper
    return decorator