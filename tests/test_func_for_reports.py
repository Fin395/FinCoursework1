from math import nan

import pandas as pd

from config import DATA_DIR
from src.func_for_reports import spending_by_category


def test_spending_by_category_incorrect_data() -> None:
    """ Проверяем работу функции при некорректной дате """
    all_transactions = pd.read_excel(DATA_DIR, na_filter=True)
    result = spending_by_category(all_transactions, "Цветы", "2019.12-10 23:30:12")
    assert result is None


def test_spending_by_category() -> None:
    """ Проверяем корректность работы функции """
    all_transactions = pd.read_excel(DATA_DIR, na_filter=True)
    result = spending_by_category(all_transactions, "Цветы", "2019-11-10 23:30:12")
    assert result == [{'MCC': 5992.0,
    'Бонусы (включая кэшбэк)': 13,
    'Валюта операции': 'RUB',
    'Валюта платежа': 'RUB',
    'Дата операции': '16.09.2019',
    'Дата платежа': '19.09.2019',
    'Категория': 'Цветы',
    'Кэшбэк': nan,
    'Номер карты': '*7197',
    'Округление на инвесткопилку': 0,
    'Описание': 'Cvety Opt Roznica',
    'Статус': 'OK',
    'Сумма операции': -650.0,
    'Сумма операции с округлением': 650.0,
    'Сумма платежа': -650.0},
    {'MCC': 5992.0,
    'Бонусы (включая кэшбэк)': 2,
    'Валюта операции': 'RUB',
    'Валюта платежа': 'RUB',
    'Дата операции': '04.09.2019',
    'Дата платежа': '07.09.2019',
    'Категория': 'Цветы',
    'Кэшбэк': nan,
    'Номер карты': '*7197',
    'Округление на инвесткопилку': 0,
    'Описание': 'Cvety Opt Roznica',
    'Статус': 'OK',
    'Сумма операции': -120.0,
    'Сумма операции с округлением': 120.0,
    'Сумма платежа': -120.0}]


def test_spending_by_category_without_date() -> None:
    """ Проверяем работу функции, если дата не передана """
    all_transactions = pd.read_excel(DATA_DIR, na_filter=True)
    result = spending_by_category(all_transactions, "Цветы")
    assert result == "В указанном периоде транзакции отсутствуют"