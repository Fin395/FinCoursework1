import datetime
import json
import logging
import os
import re
from typing import Any

import pandas as pd

from config import DATA_DIR


def get_transactions_from_excel(path_to_excel_file: str) -> list[dict[Any, Any]]:
    """Получаем список транзакций из excel-файла"""
    try:
        transactions_reader = pd.read_excel(path_to_excel_file)
        transactions_reader_as_dict = transactions_reader.to_dict(orient="records")
        return transactions_reader_as_dict
    except Exception:
        print("Ошибка, не удалось получить данные")
    return []


def get_greetings() -> str:
    """Определяем время суток для приветствия"""
    current_date_and_time = datetime.datetime.now()
    current_hour = current_date_and_time.hour
    if 0 <= current_hour < 6:
        return "Доброй ночи"
    elif 6 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def filter_transactions_by_period(transactions: list[dict], date: str) -> Any:
    """Выбираем транзакции с начала месяца, на который выпадает входящая дата, по входящую дату"""
    end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_of_period = end_of_period.replace(day=1, hour=0, minute=0, second=0)
    df = pd.DataFrame(transactions)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    filtered_transactions = df.loc[(df["Дата операции"] >= start_of_period) & (df["Дата операции"] <= end_of_period)]

    return filtered_transactions


def get_cards(transactions: Any) -> Any:
    """Группирует данные транзакций по номерам карт"""
    transactions_grouped_by_card = transactions.groupby("Номер карты", as_index=False).agg(
        {"Сумма платежа": "sum", "Кэшбэк": "sum"}
    )
    return transactions_grouped_by_card.to_dict(orient="records")


def get_top_transactions(list_of_transactions: Any) -> Any:
    """Выбираем топ-5 транзакций по сумме платежа"""
    transactions_sorted_by_amount = list_of_transactions.sort_values("Сумма платежа")
    top_transactions = transactions_sorted_by_amount[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ].head()
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%d.%m.%Y")
    return top_transactions.to_dict(orient="records")
