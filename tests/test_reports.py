import json
import datetime
from math import nan
import pandas as pd

from config import DATA_DIR, REPORTS_DEFAULT_JSON, REPORTS_SPECIFIED_JSON
from src.reports import spending_by_category, record_to_file

all_operations = pd.read_excel(DATA_DIR, na_filter=True)

from typing import Any, Optional

import pytest

#def test_spending_by_category_with_specified_date() -> None:
#    """ Проверяем корректность отбора данных, если дата указана """
#    transactions_info = pd.read_excel(DATA_DIR, na_filter=True)
#    result = spending_by_category(transactions_info, "Цветы", "2019-12-10 23:30:12")
#    assert result.to_dict(orient="records") == [{'Дата операции': '29.11.2019', 'Дата платежа': '01.12.2019', 'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -360.0, 'Валюта операции': 'RUB', 'Сумма платежа': -360.0, 'Валюта платежа': 'RUB', 'Кэшбэк': nan, 'Категория': 'Цветы', 'MCC': 5992.0, 'Описание': 'Cvety Opt Roznica', 'Бонусы (включая кэшбэк)': 7, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 360.0}, {'Дата операции': '16.09.2019', 'Дата платежа': '19.09.2019', 'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -650.0, 'Валюта операции': 'RUB', 'Сумма платежа': -650.0, 'Валюта платежа': 'RUB', 'Кэшбэк': nan, 'Категория': 'Цветы', 'MCC': 5992.0, 'Описание': 'Cvety Opt Roznica', 'Бонусы (включая кэшбэк)': 13, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 650.0}]


#def test_spending_by_category_with_default_date() -> None:
#    """ Проверяем корректность отбора данных, если дата не указана (по умолчанию - текущая дата) """
#    transactions_data = pd.read_excel(DATA_DIR, na_filter=True)
#    result = spending_by_category(transactions_data, "Цветы")
#    assert result.to_dict(orient="records") == []


def test_record_to_specified_file() -> None:
    """ Проверяем, что результат выводится в переданный в декоратор файл """
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
    df = pd.DataFrame(transactions_data)
    spending_by_category(df, "Цветы","2019-12-10 23:30:12")
    with open(REPORTS_SPECIFIED_JSON) as file:
        content = json.load(file)
    assert bool(content) is True


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

    transactions_data = pd.read_excel(DATA_DIR, na_filter=True)
    df = pd.DataFrame(transactions_data)
    spending_by_category(df, "Цветы","2019-12-10 23:30:12")
    with open(REPORTS_DEFAULT_JSON) as file:
        content = json.load(file)
    assert bool(content) is True
