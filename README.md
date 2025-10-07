# time_lock_decorator_task
A Python decorator (time_lock) challenge for rate-limiting function execution. Implements caching and checks the time interval between calls.

Python Task: Декоратор time_lock
🎯 Завдання
Напишіть декоратор Python під назвою time_lock, який обмежує частоту виклику декорованої функції. Якщо функцію викликано занадто швидко (до закінчення встановленого ліміту часу), вона повинна повернути останній відомий результат або спеціальне повідомлення, але НЕ виконувати основну логіку знову.

Ця задача перевіряє ваше знання про Декоратори, Замикання (Closure), керування Станом та використання модуля time.

🛠️ Вимоги до реалізації
Декоратор з аргументами: Декоратор time_lock повинен приймати один позиційний аргумент — seconds (число з рухомою комою або ціле число), що вказує мінімальний інтервал між успішними виконаннями функції.

Замикання та Стан: Декоратор має використовувати замикання для зберігання двох внутрішніх змінних:

last_run: Мітка часу (timestamp) останнього успішного виконання функції.

last_result: Результат останнього успішного виконання.

Логіка виконання:

Якщо з моменту last_run минуло більше ніж seconds, функція виконується, last_result та last_run оновлюються, і повертається новий результат.

Якщо з моменту last_run минуло менше ніж seconds, функція НЕ виконується. Вона повертає спеціальний кортеж: (False, last_result).

Початковий стан: Перший виклик функції завжди повинен призводити до виконання.

Повідомлення:

При успішному виконанні: Друк Running function and updating result...

При блокуванні: Друк Function is locked. Returning last cached result.

🚀 Приклад використання та очікуваний вивід
import time

# --- Ваш декоратор 'time_lock' тут ---

@time_lock(seconds=3)
def fetch_data(user_id: int) -> str:
    # Імітація тривалої операції або мережевого запиту
    time.sleep(0.5) 
    return f"Data for user {user_id} fetched at {time.time()}"

# 1. Перший виклик (Завжди успішно)
print(f"Call 1: {fetch_data(101)}\n")

# 2. Другий виклик (Блокування, менше 3 секунд)
print(f"Call 2: {fetch_data(101)}\n")

# 3. Чекаємо, щоб інтервал минув
print("--- Waiting 3.5 seconds ---\n")
time.sleep(3.5)

# 4. Третій виклик (Успішно)
print(f"Call 3: {fetch_data(101)}\n")

Очікуваний вивід (Приблизно):

Running function and updating result...
Call 1: Data for user 101 fetched at 1678886400.123
Function is locked. Returning last cached result.
Call 2: (False, 'Data for user 101 fetched at 1678886400.123')

--- Waiting 3.5 seconds ---

Running function and updating result...
Call 3: Data for user 101 fetched at 1678886403.678

📝 Поради
Використовуйте time.time() для отримання поточної мітки часу.

Змінні last_run та last_result повинні бути визначені у зовнішньому обсязі (всередині time_lock) та змінені у внутрішньому обсязі (всередині wrapper) за допомогою ключового слова nonlocal.
-------------------------------------------
Time Lock Decorator
Task Description
Create a Python decorator named time_lock(seconds) that imposes a rate limit on the calls to the decorated function.

The decorator must accept one argument:

seconds (integer): The minimum time (in seconds) that must elapse between consecutive successful calls of the decorated function.

Requirements
Limitation: If the function is called before seconds have passed since its last successful execution, the decorator must prevent the new execution.

Blocked Behavior: If the call is blocked, the function should return None and print a warning message to the console, for example:

"Call blocked. Please try again in X seconds."

Successful Behavior: If the required time has elapsed, the function executes normally, and the time of its last call is updated.

Initial Call: The very first call to the function must always be successful.

Example Usage
import time

@time_lock(seconds=5)
def send_notification(user, message):
    print(f"[{time.strftime('%H:%M:%S')}] Notification sent to user {user}: {message}")
    return True # Successful execution signal

# First call (successful)
send_notification("Alice", "Hello")

# Attempt second call after 2 seconds (blocked)
time.sleep(2)
send_notification("Alice", "How are you?")

# Attempt third call after 6 seconds (successful)
time.sleep(4)
send_notification("Bob", "This is a new notification")
