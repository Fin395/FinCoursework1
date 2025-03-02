import datetime
import json
from typing import Optional

import pandas as pd

from config import DATA_DIR, REPORTS_DEFAULT_JSON, REPORTS_SPECIFIED_JSON
from src.reports import record_to_file


def test_record_to_default_file() -> None:
    """Проверяем, что результат выводится в файл по умолчанию"""

    @record_to_file()
    def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
        """Функция отбирает транзакции по тратам по определенной категории"""
        if date:
            end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            end_of_period = datetime.datetime.now()
        start_of_period = end_of_period - pd.DateOffset(months=3)
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        trans_filtered_by_period = transactions.loc[
            (transactions["Дата операции"] >= start_of_period) & (transactions["Дата операции"] <= end_of_period)
        ]
        trans_filtered_by_spent = trans_filtered_by_period.loc[
            (trans_filtered_by_period["Сумма платежа"] < 0) & (trans_filtered_by_period["Статус"] == "OK")
        ]
        trans_filtered_by_category = trans_filtered_by_spent.loc[
            (trans_filtered_by_spent["Категория"] == category)
        ].copy()
        trans_filtered_by_category["Дата операции"] = trans_filtered_by_category["Дата операции"].dt.strftime(
            "%d.%m.%Y"
        )
        return trans_filtered_by_category

    transactions_info = pd.read_excel(DATA_DIR, na_filter=True)
    spending_by_category(transactions_info, "Цветы", "2019-12-10 23:30:12")
    with open(REPORTS_DEFAULT_JSON) as f:
        data = json.load(f)
    assert bool(data) is True


def test_record_to_specified_file() -> None:
    """Проверяем, что результат выводится в файл, переданный в декоратор по умолчанию"""

    @record_to_file(REPORTS_SPECIFIED_JSON)
    def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
        """Функция отбирает транзакции по тратам по определенной категории"""
        if date:
            end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            end_of_period = datetime.datetime.now()
        start_of_period = end_of_period - pd.DateOffset(months=3)
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        trans_filtered_by_period = transactions.loc[
            (transactions["Дата операции"] >= start_of_period) & (transactions["Дата операции"] <= end_of_period)
        ]
        trans_filtered_by_spent = trans_filtered_by_period.loc[
            (trans_filtered_by_period["Сумма платежа"] < 0) & (trans_filtered_by_period["Статус"] == "OK")
        ]
        trans_filtered_by_category = trans_filtered_by_spent.loc[
            (trans_filtered_by_spent["Категория"] == category)
        ].copy()
        trans_filtered_by_category["Дата операции"] = trans_filtered_by_category["Дата операции"].dt.strftime(
            "%d.%m.%Y"
        )
        return trans_filtered_by_category

    transactions_data = pd.read_excel(DATA_DIR, na_filter=True)
    spending_by_category(transactions_data, "Цветы", "2019-12-10 23:30:12")
    with open(REPORTS_SPECIFIED_JSON) as file:
        content = json.load(file)
    assert bool(content) is True
