from math import nan

import pandas as pd

from config import DATA_DIR
from src.reports import spending_by_category

all_operations = pd.read_excel(DATA_DIR, na_filter=True)

from typing import Any

import pytest

from src.decorators import log


def test_log_return() -> None:
    """Проверяем, что декоратор корректно возвращает результат функции"""

    @log(filename="mylog.txt")
    def my_function(x: int | float, y: int | float) -> int | float:
        return x + y

    my_function(1, 2)
    assert my_function(1, 2) == 3


def test_log_invalid_parameters() -> None:
    """Проверяем, что декоратор вызывает ошибку при неверно переданных аргументах"""
    with pytest.raises(Exception):

        @log(filename="mylog.txt")
        def my_function(x: int | float, y: int | float) -> int | float:
            return x + y

        my_function(1)


def test_log_console_capture_if_ok(capsys: Any) -> Any:
    """Тестирование вывода результатов в консоль при корректно переданных аргументах"""

    @log()
    def my_function(x: int | float, y: int | float) -> int | float:
        return x + y

    my_function(1, 2)
    captured = capsys.readouterr()
    assert "my_function ok, result: 3" in captured.out


def test_log_printing_to_file() -> None:
    """Тестируем вывод результата в файл"""

    @log(filename="mylog.txt")
    def my_function(x: int | float, y: int | float) -> int | float:
        return x + y

    my_function(1, 2)
    with open("mylog.txt", "r") as file:
        content = file.read()
    assert "my_function ok, result: 3" in content


def test_log_console_capture_if_valid(capsys: Any) -> Any:
    """Тестирование вывода результатов в консоль при некорректно переданных аргументах"""
    with pytest.raises(Exception) as f:

        @log()
        def my_function(x: int | float, y: int | float) -> int | float:
            return x + y

        my_function(1)

        captured = capsys.readouterr()
        assert f in captured.out
