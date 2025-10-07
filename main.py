from typing import Callable, Any
import time


def time_lock(seconds: int | float) -> Callable:
    last_run = 0.0
    last_result = None

    def inner(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            nonlocal last_run, last_result
            current_time = time.time()
            if last_run > 0 and (current_time - last_run < seconds):
                print("Function is locked. Returning last cached result.")
                return False, last_result
            else:
                last_run = current_time
                print("Running function and updating result...")
                last_result = func(*args, **kwargs)
                return last_result
        return wrapper
    return inner


def fetch_data(user_id: int) -> str:
    return f"Data for user {user_id} fetched at {time.time()}"


if __name__ == "__main__":
    @time_lock(seconds=3)
    def fetch_user_data(user_id: int) -> str:
        return f"Data for user {user_id} fetched at {time.time()}"

    print("-" * 20)
    print("Test 1 (Initial Run):")
    # Перший запуск
    result1 = fetch_user_data(11)
    print(f"Result 1: {result1}")

    time.sleep(1)  # Пройшло 1 секунда

    print("-" * 20)
    print("Test 2 (Blocked Run):")
    # Заблокований запуск
    result2 = fetch_user_data(12)
    print(f"Result 2: {result2}")

    time.sleep(2.1)  # Пройшло 1 + 2.1 = 3.1 секунди (достатньо)

    print("-" * 20)
    print("Test 3 (Successful Run):")
    # Успішний запуск
    result3 = fetch_user_data(11)
    print(f"Result 3: {result3}")
