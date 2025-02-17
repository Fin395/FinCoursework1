import datetime
import json
import logging
import os
import re
from typing import Any
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
excel_file_path = os.path.join(dir_path, "..", "data", "operations.xls")


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
    """ Определяем время суток """
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

def filter_by_period_of_time(list_of_transactions, current_date_time):
    filtered_transactions = []
    current_date_time_objects = datetime.datetime.strptime(current_date_time, "%Y-%m-%d %H:%M:%S")
    current_date = current_date_time_objects.strftime("%d-%m-%Y")
    current_date_in_required_format = current_date.replace("-", ".")
    for transaction in list_of_transactions:
            if current_date_in_required_format in transaction["Дата операции"].split():
                filtered_transactions.append(transaction)
    return filtered_transactions

result = get_transactions_from_excel(r"C:\Users\Sergei\Downloads\operations.xlsx")
print (filter_by_period_of_time(result, "2018-01-01 01:53:34"))
