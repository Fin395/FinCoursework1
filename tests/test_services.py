from src.services import get_transfers


def test_get_transfers(sample_transactions: list[dict]) -> None:
    """Проверяем корректность выборки по описанию и категории"""
    result = get_transfers(sample_transactions)
    assert result == (
        "[\n"
        "    {\n"
        '        "Дата операции": "16.10.2018 20:56:20",\n'
        '        "Дата платежа": "16.10.2018",\n'
        '        "Номер карты": NaN,\n'
        '        "Статус": "OK",\n'
        '        "Сумма операции": -500.0,\n'
        '        "Валюта операции": "RUB",\n'
        '        "Сумма платежа": -500.0,\n'
        '        "Валюта платежа": "RUB",\n'
        '        "Кэшбэк": NaN,\n'
        '        "Категория": "Переводы",\n'
        '        "MCC": NaN,\n'
        '        "Описание": "Ксения К.",\n'
        '        "Бонусы (включая кэшбэк)": 0,\n'
        '        "Округление на инвесткопилку": 0,\n'
        '        "Сумма операции с округлением": 500.0\n'
        "    }\n"
        "]"
    )


def test_get_transfers_no_description(sample_transactions_no_description: list[dict]) -> None:
    """Проверяем, что функция возвращает пустой список при отсутствии столбца 'категория'"""
    result = get_transfers(sample_transactions_no_description)
    assert result == "[]"


def test_get_transfers_no_category(sample_transactions_no_category: list[dict]) -> None:
    """Проверяем, что функция возвращает пустой список при отсутствии столбца 'описание'"""
    result = get_transfers(sample_transactions_no_category)
    assert result == "[]"
