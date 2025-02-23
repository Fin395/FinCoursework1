from math import nan

from src.services import get_transfers


def test_get_transfers(sample_transactions: list[dict]) -> None:
    """Проверяем корректность выборки по описанию и категории """
    result = get_transfers(sample_transactions)
    assert result == {
        "Дата операции": "16.10.2018 20:56:20",
        "Дата платежа": "16.10.2018",
        "Номер карты": NaN,
        "Статус": "OK",
        "Сумма операции": -500.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -500.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": NaN,
        "Категория": "Переводы",
        "MCC": NaN,
        "Описание": "Ксения К.",
        "Бонусы (включая кэшбэк)": 0,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 500.0
    }


def test_search_for_transcations_by_string_no_match(sample_transactions_json: list[dict]) -> None:
    """Проверяем, что функция возвращает пустой список, если шаблон не найден"""
    result = search_for_transcations_by_string(sample_transactions_json, "вклад")
    assert result == []
