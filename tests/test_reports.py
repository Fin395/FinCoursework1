import json
import datetime
from math import nan
import pandas as pd

from config import DATA_DIR, REPORTS_DEFAULT_JSON, REPORTS_SPECIFIED_JSON
from src.reports import spending_by_category, record_to_file

all_operations = pd.read_excel(DATA_DIR, na_filter=True)

from typing import Optional


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


def test_record_to_default_file() -> None:
    """ Проверяем, что результат выводится в файл по умолчанию """
    @record_to_file()
    def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
        """ Функция отбирает транзакции по тратам по определенной категории """
        if date:
            end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            end_of_period = datetime.datetime.now()
        start_of_period = end_of_period - pd.DateOffset(months=3)
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        trans_filtered_by_period = transactions.loc[
            (transactions["Дата операции"] >= start_of_period) & (transactions["Дата операции"] <= end_of_period)]
        trans_filtered_by_spent = trans_filtered_by_period.loc[
            (trans_filtered_by_period["Сумма платежа"] < 0) & (trans_filtered_by_period["Статус"] == "OK")]
        trans_filtered_by_category = trans_filtered_by_spent.loc[
            (trans_filtered_by_spent["Категория"] == category)].copy()
        trans_filtered_by_category["Дата операции"] = trans_filtered_by_category["Дата операции"].dt.strftime(
            "%d.%m.%Y")
        return trans_filtered_by_category

    transactions_info = pd.read_excel(DATA_DIR, na_filter=True)
    spending_by_category(transactions_info, "Цветы","2019-12-10 23:30:12")
    with open(REPORTS_DEFAULT_JSON) as f:
        data = json.load(f)
    assert bool(data) is True

def test_record_to_specified_file() -> None:
    """ Проверяем, что результат выводится в файл, переданный в декоратор по умолчанию """
    @record_to_file(REPORTS_SPECIFIED_JSON)
    def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
        """ Функция отбирает транзакции по тратам по определенной категории """
        if date:
            end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            end_of_period = datetime.datetime.now()
        start_of_period = end_of_period - pd.DateOffset(months=3)
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        trans_filtered_by_period = transactions.loc[
            (transactions["Дата операции"] >= start_of_period) & (transactions["Дата операции"] <= end_of_period)]
        trans_filtered_by_spent = trans_filtered_by_period.loc[
            (trans_filtered_by_period["Сумма платежа"] < 0) & (trans_filtered_by_period["Статус"] == "OK")]
        trans_filtered_by_category = trans_filtered_by_spent.loc[
             (trans_filtered_by_spent["Категория"] == category)].copy()
        trans_filtered_by_category["Дата операции"] = trans_filtered_by_category["Дата операции"].dt.strftime(
            "%d.%m.%Y")
        return trans_filtered_by_category

    transactions_data = pd.read_excel(DATA_DIR, na_filter=True)
    spending_by_category(transactions_data, "Цветы", "2019-12-10 23:30:12")
    with open(REPORTS_SPECIFIED_JSON) as file:
            content = json.load(file)
    assert bool(content) is True
