import pytest
import time
from unittest.mock import patch, MagicMock
# Імпорт основної логіки з файлу main.py
from main import time_lock, fetch_data


# ----------------------------------------------------
# 1. Фікстура для симуляції часу (Mock Time)
# ----------------------------------------------------
@pytest.fixture
def mock_time():
    """Фікстура, що замінює time.time() для контролю часу."""
    # Починаємо з моменту часу 1000.0
    mock_timer = MagicMock(return_value=1000.0)
    with patch('time.time', mock_timer) as mocked_time:
        yield mocked_time


# ----------------------------------------------------
# 2. Тести
# ----------------------------------------------------

def test_initial_success(mock_time):
    """
    Перевірка 1: Перший виклик має бути успішним
    і повернути очікуваний результат функції.
    """
    # Arrange: Ліміт 5 секунд
    decorated_func = time_lock(seconds=5)(fetch_data)

    # Act: Час = 1000.0
    result = decorated_func(1)

    # Assert: Результат має містити початковий час (1000.0)
    assert result == "Data for user 1 fetched at 1000.0"


def test_call_is_blocked(mock_time):
    """
    Перевірка 2: Виклик до закінчення ліміту повертає (False, кеш)
    і не виконує функцію повторно.
    """
    # Arrange: Ліміт 10 секунд
    decorated_func = time_lock(seconds=10)(fetch_data)

    # 1. Успішний перший виклик (Час = 1000.0). Кешуємо результат.
    mock_time.return_value = 1000.0
    first_result = decorated_func(2)

    # 2. Просуваємо час лише на 5 секунд (5 < 10)
    mock_time.return_value = 1005.0

    # Act: Другий виклик (має бути заблокований)
    result_blocked = decorated_func(3)

    # Assert: Має повернути кортеж (False, кешований_результат)
    assert result_blocked[0] is False
    assert result_blocked[1] == first_result


def test_call_after_delay_updates_cache(mock_time):
    """
    Перевірка 3: Виклик після закінчення ліміту успішний,
    повертає новий результат і оновлює кеш.
    """
    # Arrange: Ліміт 10 секунд
    lock_time = 10
    decorated_func = time_lock(seconds=lock_time)(fetch_data)

    # 1. Перший виклик (Час = 1000.0)
    decorated_func(4)

    # 2. Просуваємо час на 10.1 секунд (10.1 > 10)
    new_time = 1000.0 + lock_time + 0.1
    mock_time.return_value = new_time

    # Act 1: Другий виклик (має бути успішним)
    result_success = decorated_func(5)

    # Assert 1: Очікуємо результат з новим часом (1010.1)
    assert result_success == "Data for user 5 fetched at 1010.1"

    # 3. Просуваємо час лише на 1 секунду (для перевірки, чи оновився кеш)
    mock_time.return_value = new_time + 1.0

    # Act 2: Третій виклик (має бути заблокований, повертаючи кеш з Act 1)
    result_check_cache = decorated_func(6)

    # Assert 2: має повернути (False, новий результат, який кешувався в Act 1)
    assert result_check_cache[0] is False
    assert result_check_cache[1] == result_success
