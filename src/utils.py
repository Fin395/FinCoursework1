import datetime
import json
import logging
import os
import re
from typing import Any

import currencyapicom
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

from config import DATA_DIR, JSON_DIR

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_transactions_from_excel(path_to_excel_file: str) -> list[dict[Any, Any]]:
    """Получаем список транзакций из excel-файла"""
    try:
        df = pd.read_excel(path_to_excel_file, na_filter=True)
        df_as_dict = df.to_dict(orient="records")
        return df_as_dict
    except Exception:
        print("Ошибка, не удалось получить данные")
    return []


def get_greetings() -> str:
    """Определяем приветствие по времени суток"""
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
    """Выбираем транзакции с начала месяца, на который выпадает входящая дата, по входящую дату"""
    end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_of_period = end_of_period.replace(day=1, hour=0, minute=0, second=0)
    df = pd.DataFrame(transactions)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    filtered_transactions = df.loc[(df["Дата операции"] >= start_of_period) & (df["Дата операции"] <= end_of_period)]
    return filtered_transactions


def get_cards(transactions: pd.DataFrame) -> list[dict]:
    """Группирует данные транзакций по номерам карт"""
    transactions_filtered = transactions.loc[(transactions["Сумма операции"] < 0) & (transactions["Статус"] == "OK")]
    transactions_filtered.loc[transactions_filtered["Кэшбэк"].isna(), "Кэшбэк"] = 0
    for index, row in transactions_filtered.iterrows():
        if row["Кэшбэк"] == 0:
            transactions_filtered.at[index, "Кэшбэк"] = (
                transactions_filtered.at[index, "Сумма операции с округлением"] // 100
            )
    transactions_grouped_by_card = transactions_filtered.groupby("Номер карты", as_index=False).agg(
        {"Сумма операции": "sum", "Кэшбэк": "sum"}
    )
    transactions_grouped_by_card.rename(
        columns={"Номер карты": "last_digits", "Сумма операции": "total_spent", "Кэшбэк": "cashback"}, inplace=True
    )
    return transactions_grouped_by_card.to_dict(orient="records")


def get_top_transactions(list_of_transactions: pd.DataFrame) -> list[dict]:
    """Выбираем топ-5 транзакций по сумме платежа"""
    transactions_sorted_by_amount = list_of_transactions.sort_values("Сумма операции")
    top_transactions = transactions_sorted_by_amount[
        ["Дата операции", "Сумма операции", "Категория", "Описание"]
    ].head()
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%d.%m.%Y")
    top_transactions.rename(
        columns={
            "Дата операции": "date",
            "Сумма операции": "amount",
            "Категория": "category",
            "Описание": "description",
        },
        inplace=True,
    )
    return top_transactions.to_dict(orient="records")


def get_currencies(path_to_json_file: str) -> Any:
    """Получаем список наименований валют из JSON-файла"""
    with open(path_to_json_file) as f:
        currencies_and_stocks = json.load(f)
    currencies = currencies_and_stocks["user_currencies"]
    return currencies


def get_stocks() -> Any:
    """Получаем список наименований акций из JSON-файла"""
    with open(JSON_DIR) as f:
        currencies_and_stocks = json.load(f)
    stocks = currencies_and_stocks["user_stocks"]
    return stocks


def get_currency_rate(currencies: list[str], date: str) -> list[dict]:
    """Получаем курсы валют из списка"""
    rates_list = []
    formatted_rates_list = []
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    required_date = date_obj.strftime("%Y-%m-%d")
    for curr in currencies:
        url = f"https://api.apilayer.com/exchangerates_data/{required_date}?symbols=rub&base={curr}"
        payload = {}
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers, data=payload)
        status_code = response.status_code
        if status_code == 200:
            rates_list.append(response.json())
        else:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

    for each_rate in rates_list:
        currency_name = each_rate["base"]
        rate = round(each_rate["rates"]["RUB"], 2)
        rate_dict = dict(currency=currency_name, rate=rate)
        formatted_rates_list.append(rate_dict)
    return formatted_rates_list

#print(get_currency_rate(["USD", "EUR"], "2021-12-20 23:59:59"))