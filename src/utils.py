import datetime
import json
import logging
import os
from typing import Any
from config import LOGS_FILE_UTILS, JSON_DIR

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOGS_FILE_UTILS, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_greetings() -> str:
    """Определяем приветствие по времени суток"""
    logger.info("Определяются текущие дата и время")
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
    logger.info("Определяется начало месяца")
    start_of_period = end_of_period.replace(day=1, hour=0, minute=0, second=0)
    df = pd.DataFrame(transactions)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    logger.info("Происходит выборка транзакций в заданный период времени")
    filtered_transactions = df.loc[(df["Дата операции"] >= start_of_period) & (df["Дата операции"] <= end_of_period)]
    return filtered_transactions


def get_cards(transactions: pd.DataFrame) -> list[dict]:
    """Группирует данные транзакций по номерам карт"""
    logger.info("Происходит выборка успешных транзакций, связанных с расходами")
    transactions_filtered = transactions.loc[(transactions["Сумма платежа"] < 0) & (transactions["Статус"] == "OK")]
    transactions_filtered.loc[transactions_filtered["Кэшбэк"].isna(), "Кэшбэк"] = 0
    for index, row in transactions_filtered.iterrows():
        if row["Кэшбэк"] == 0:
            logger.info("Происходит расчет кэшбека")
            transactions_filtered.at[index, "Кэшбэк"] = (
                transactions_filtered.at[index, "Сумма операции с округлением"] // 100
            )
    logger.info("Происходит группировка транзакций по номерам карт")
    transactions_grouped_by_card = transactions_filtered.groupby("Номер карты", as_index=False).agg(
        {"Сумма платежа": "sum", "Кэшбэк": "sum"}
    )
    logger.info("Происходит переименование позиций")
    transactions_grouped_by_card.rename(
        columns={"Номер карты": "last_digits", "Сумма платежа": "total_spent", "Кэшбэк": "cashback"}, inplace=True
    )
    return transactions_grouped_by_card.to_dict(orient="records")


def get_top_transactions(list_of_transactions: pd.DataFrame) -> list[dict]:
    """Выбираем топ-5 транзакций по сумме платежа"""
    logger.info("Происходит сортировка транзакций по сумме платежа")
    transactions_sorted_by_amount = list_of_transactions.sort_values("Сумма платежа")
    top_transactions = transactions_sorted_by_amount[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ].head()
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%d.%m.%Y")
    logger.info("Происходит переименование позиций")
    top_transactions.rename(
        columns={
            "Дата операции": "date",
            "Сумма платежа": "amount",
            "Категория": "category",
            "Описание": "description",
        },
        inplace=True,
    )
    return top_transactions.to_dict(orient="records")


def get_currencies(path_to_json_file: str) -> Any:
    """Получаем список наименований валют из JSON-файла"""
    try:
        logger.info(f"Получаем наименования валюты и акций из файла {path_to_json_file}")
        with open(path_to_json_file, encoding="utf-8") as user_settings_data:
            currencies_and_stocks = json.load(user_settings_data)
            currencies = currencies_and_stocks["user_currencies"]

    except FileNotFoundError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")
        return []

    except json.decoder.JSONDecodeError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")
        return []

    except KeyError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")
        return []

    else:
        return currencies

#print(get_currencies(JSON_DIR))

def get_stocks(path_to_json_file: str) -> Any:
    """Получаем список наименований акций из JSON-файла"""
    try:
        logger.info(f"Получаем наименования валюты и акций из файла {path_to_json_file}")
        with open(path_to_json_file, encoding="utf-8") as user_settings_data:
            currencies_and_stocks = json.load(user_settings_data)
            stocks = currencies_and_stocks["user_stocks"]

    except FileNotFoundError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")
        return []

    except json.decoder.JSONDecodeError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")
        return []

    except KeyError as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")
        return []

    else:
        return stocks

#print(get_stocks(JSON_DIR))


def get_currency_rate(currencies: list[str], date: str) -> list[dict]:
    """Получаем курсы валют из списка"""
    rates_list = []
    formatted_rates_list = []
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    logger.info("Устанавливаем необходимый формат даты")
    required_date = date_obj.strftime("%Y-%m-%d")

    for curr in currencies:
        url = f"https://api.apilayer.com/exchangerates_data/{required_date}?symbols=rub&base={curr}"
        payload = {}
        headers = {"apikey": API_KEY_CURRENCY}
        logger.info("Получаем данные о курсе валюты")
        response = requests.get(url, headers=headers, data=payload)
        status_code = response.status_code
        if status_code == 200:
            logger.info("Добавляем информацию о курсе валюты")
            rates_list.append(response.json())
        else:
            logger.error(f"Ошибка: {response.reason}")
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

    try:
        for each_rate in rates_list:
            currency_name = each_rate["base"]
            rate = round(each_rate["rates"]["RUB"], 2)
            rate_dict = dict(currency=currency_name, rate=rate)
            logger.info("Добавляем курс валюты в список с измененными позициями")
            formatted_rates_list.append(rate_dict)
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")
    else:
        return formatted_rates_list


#print(get_currency_rate(["USD", "EUR"], "2021-12-20 23:59:59"))


def get_stock_price(stocks: list[str], date: str) -> list[dict]:
    """Получаем наименования акций из списка"""
    stocks_list = []
    formatted_stocks_list = []
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    logger.info("Устанавливаем необходимый формат даты")
    formatted_date = date_obj.strftime("%Y-%m-%d")

    for stock in stocks:
        url = f"https://api.marketstack.com/v1/eod/{formatted_date}?access_key={API_KEY_STOCK}"
        querystring = {"symbols": stock}
        logger.info("Получаем данные о стоимости акции")
        response = requests.get(url, params=querystring)
        status_code = response.status_code
        if status_code == 200:
            logger.info("Добавляем информацию о стоимости акции")
            stocks_list.append(response.json())
        else:
            logger.error(f"Ошибка: {response.reason}")
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

    try:
        for each_stock in stocks_list:
            data_values = each_stock["data"]
            for data_value in data_values:
                price = data_value["close"]
                stock_name = data_value["symbol"]
                stock_dict = dict(stock=stock_name, price=price)
                formatted_stocks_list.append(stock_dict)
    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")
    else:
        return formatted_stocks_list


#print(get_stock_price(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"], "2024-12-20 23:59:59"))
