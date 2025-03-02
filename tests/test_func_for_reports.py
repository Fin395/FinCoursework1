from typing import Any

import pandas as pd

from config import DATA_DIR
from src.func_for_reports import spending_by_category


def test_spending_by_category_incorrect_data() -> None:
    """Проверяем работу функции при некорректной дате"""
    all_transactions = pd.read_excel(DATA_DIR, na_filter=True)
    result = spending_by_category(all_transactions, "Цветы", "2019.12-10 23:30:12")
    assert result is None


def test_spending_by_category() -> None:
    """Проверяем корректность работы функции"""
    all_transactions = pd.read_excel(DATA_DIR, na_filter=True)
    result = spending_by_category(all_transactions, "Цветы", "2019-11-10 23:30:12")
    result = result.to_dict(orient="records")

    def replace_nan_with_none(obj: list) -> dict[Any, list] | list[list] | None | list:
        """Рекурсивно заменяет все NaN на None для удобства сравнения"""
        if isinstance(obj, dict):
            return {k: replace_nan_with_none(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_nan_with_none(i) for i in obj]
        elif isinstance(obj, float) and pd.isna(obj):
            return None
        return obj

    result = replace_nan_with_none(result)
    assert result == [
        {
            "Дата операции": "16.09.2019",
            "Дата платежа": "19.09.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -650.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -650.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Цветы",
            "MCC": 5992.0,
            "Описание": "Cvety Opt Roznica",
            "Бонусы (включая кэшбэк)": 13,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 650.0,
        },
        {
            "Дата операции": "04.09.2019",
            "Дата платежа": "07.09.2019",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -120.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -120.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": None,
            "Категория": "Цветы",
            "MCC": 5992.0,
            "Описание": "Cvety Opt Roznica",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 120.0,
        },
    ]


def test_spending_by_category_without_date() -> None:
    """Проверяем работу функции, если дата не передана"""
    all_transactions = pd.read_excel(DATA_DIR, na_filter=True)
    result = spending_by_category(all_transactions, "Цветы")
    assert result == "В указанном периоде транзакции отсутствуют"
