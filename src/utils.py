import datetime
import json
import logging
import os
import re
from typing import Any

import numpy as np
import pandas as pd

from config import DATA_DIR


def get_transactions_from_excel(path_to_excel_file: str) -> list[dict[Any, Any]]:
    """ Получаем список транзакций из excel-файла """
    try:
        df = pd.read_excel(path_to_excel_file, na_filter=True)
        df_as_dict = df.to_dict(orient="records")
        return df_as_dict
    except Exception:
        print("Ошибка, не удалось получить данные")
    return []


def get_greetings() -> str:
    """ Определяем приветствие по времени суток """
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


def filter_transactions_by_period(transactions: list[dict], date: str) -> pd.DataFrame:
    """ Выбираем транзакции с начала месяца, на который выпадает входящая дата, по входящую дату """
    end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_of_period = end_of_period.replace(day=1, hour=0, minute=0, second=0)
    df = pd.DataFrame(transactions)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    filtered_transactions = df.loc[(df["Дата операции"] >= start_of_period) & (df["Дата операции"] <= end_of_period)]

    return filtered_transactions

#print(filter_transactions_by_period(get_transactions_from_excel(DATA_DIR), "2021-09-26 23:59:59"))


def get_cards(transactions: pd.DataFrame) -> list[dict]:
    """ Группирует данные транзакций по номерам карт """
    transactions_filtered = transactions.loc[(transactions["Сумма операции"] < 0) & (transactions["Статус"] == "OK")]
    transactions_filtered.loc[transactions_filtered["Кэшбэк"].isna(), "Кэшбэк"] = 0
    for index, row in transactions_filtered.iterrows():
        if row["Кэшбэк"] == 0:
            transactions_filtered.at[index, "Кэшбэк"] = transactions_filtered.at[index, "Сумма операции с округлением"] // 100
    transactions_grouped_by_card = transactions_filtered.groupby("Номер карты", as_index=False).agg(
        {"Сумма операции": "sum", "Кэшбэк": "sum"}
    )
    transactions_grouped_by_card.rename(columns={"Номер карты": "last_digits", "Сумма операции": "total_spent", "Кэшбэк": "cashback"}, inplace=True)
    return transactions_grouped_by_card.to_dict(orient="records")

#print(get_cards(filter_transactions_by_period(get_transactions_from_excel(DATA_DIR), "2021-06-02 23:59:59")))


def get_top_transactions(list_of_transactions: pd.DataFrame) -> list[dict]:
    """ Выбираем топ-5 транзакций по сумме платежа """
    transactions_sorted_by_amount = list_of_transactions.sort_values("Сумма операции")
    top_transactions = transactions_sorted_by_amount[
        ["Дата операции", "Сумма операции", "Категория", "Описание"]
    ].head()
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%d.%m.%Y")
    top_transactions.rename(columns={"Дата операции": "date", "Сумма операции": "amount", "Категория": "category", "Описание": "description"}, inplace=True)
    return top_transactions.to_dict(orient="records")


#def get_currency_rate(transactions) -> Any:
#    """Функцию принимает на вход транзакцию и конвертирует сумму транзакции в рубли"""
#
# Обработать рубль
#
#    transactions_grouped_by_currency = transactions.groupby("Валюта операции", as_index=False)
#
#
#print(get_currency_rate(filter_transactions_by_period(get_transactions_from_excel(DATA_DIR), "2021-09-30 23:59:59")))
#
#
#    if transaction_info["operationAmount"]["currency"]["code"] == "RUB":
#        return transaction_info["operationAmount"]["amount"]
#    else:
#        url = "https://api.apilayer.com/exchangerates_data/convert"
#        payload = {
#            "amount": transaction_info["operationAmount"]["amount"],
#            "from": transaction_info["operationAmount"]["currency"]["code"],
#            "to": "RUB",
#        }
#        headers = {"apikey": API_KEY}
#        response = requests.get(url, headers=headers, params=payload)
#        if response.status_code == 200:
#            transaction_amount = response.json()
#           return float(transaction_amount["result"])
#        else:
#            print(f"Запрос не был успешным. Возможная причина: {response.reason}")