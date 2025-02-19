import datetime
import json
import logging
import os
import re
from typing import Any
import pandas as pd

from config import DATA_DIR

dir_path = os.path.dirname(os.path.realpath(__file__))
excel_file_path = os.path.join(dir_path, "..", "data", "operations.xlsx")


def get_transactions_from_excel(path_to_excel_file: str) -> list[dict]:
    """Получаем список транзакций из excel-файла"""
    try:
        transactions_reader = pd.read_excel(path_to_excel_file)
        transactions_reader_as_dict = transactions_reader.to_dict(orient="records")
        return transactions_reader_as_dict
    except Exception:
        print("Ошибка, не удалось получить данные")
    return []



def get_day_period() -> str:
    """ Определяем время суток для приветствия """
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


def get_cards(date):
    """ Фильтруем транзакции за определенный период времени """
    end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_of_period = end_of_period.replace(year=end_of_period.year, month=end_of_period.month, day=1) - datetime.timedelta(hours=end_of_period.hour, minutes=end_of_period.minute, seconds=end_of_period.second)
    df = pd.read_excel(excel_file_path)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    filtered_transactions = df.loc[(df['Дата операции'] >= start_of_period)
                         & (df['Дата операции'] <= end_of_period)]

    filtered_transactions_grouped_by_card = filtered_transactions.groupby("Номер карты",as_index=False).agg({"Сумма операции": "sum", "Кэшбэк": "sum"})
    return filtered_transactions_grouped_by_card.to_dict(orient="records")

print(get_cards("2021-12-03 01:53:34"))


def get_top_transactions(date):
    """ Фильтруем транзакции за определенный период времени """
    end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_of_period = end_of_period.replace(year=end_of_period.year, month=end_of_period.month, day=1) - datetime.timedelta(hours=end_of_period.hour, minutes=end_of_period.minute, seconds=end_of_period.second)
    df = pd.read_excel(excel_file_path)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
    filtered_transactions = df.loc[(df['Дата операции'] >= start_of_period)
                         & (df['Дата операции'] <= end_of_period)]

    filtered_transactions_grouped_by_amount = filtered_transactions.groupby("Номер карты",as_index=False).agg({"Сумма операции": "sum", "Кэшбэк": "sum"})
    return filtered_transactions_grouped_by_card.to_dict(orient="records")

print(filter_by_period_of_time("2021-12-03 01:53:34"))


    #    end_of_period = date_obj.strftime("%d-%m-%Y %H:%M:%S").replace("-", ".")

    #    reformatted_date_obj = date_obj.strftime("%d-%m-%Y %H:%M:%S").replace("-", ".")
#    end_of_period = reformatted_date_obj
#    start_of_period =    reformatted_date = date_obj.strftime("%d-%m-%Y %H:%M:%S").replace("-", ".")
#    end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
#    start_of_period = end_of_period.replace(year=end_of_period.year, month=end_of_period.month, day=1) - datetime.timedelta(hours=end_of_period.hour, minutes=end_of_period.minute, seconds=end_of_period.second)
#    print(start_of_period)
#    print(end_of_period)
#    df = pd.read_excel(excel_file_path)
#    filtered_transactions = df[df["Дата операции"].between(start_of_period, end_of_period)]
#    return filtered_transactions


#date_objects = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
#reformatted_date = date_objects.strftime("%d-%m-%Y").replace("-", ".")
#end_of_period =
#    current_date_in_required_format = current_date.replace("-", ".")
#begining_date = datetime.datetime.strptime(date_string, "%d-%m-%Y %H:%M:%S")
#print(reformatted_date)

#date_obj = datetime.datetime(2022, 3, 8)
#new_date_obj = date_obj.replace(year=2023, month=3, day=8)
#print(new_date_obj)





#date_string = date.strftime("%d-%m-%Y %H:%M:%S")

#    print(date_string)

#filter_by_period_of_time("2018-01-01 01:53:34")

#    filtered_transactions = []
#    current_date_time_objects = datetime.datetime.strptime(current_date_time, "%Y-%m-%d %H:%M:%S")
#    current_date = current_date_time_objects.strftime("%d-%m-%Y")
#    current_date_in_required_format = current_date.replace("-", ".")
#    for transaction in list_of_transactions:
#            if current_date_in_required_format in transaction["Дата операции"].split():
#                filtered_transactions.append(transaction)
#    return filtered_transactions

#result = get_transactions_from_excel(excel_file_path)
#print (filter_by_period_of_time(result, "2018-01-01 01:53:34"))


