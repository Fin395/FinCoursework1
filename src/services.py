import json
import re

import pandas as pd

from config import DATA_DIR


def get_transfers(list_of_transaction: list[dict]) -> str:
    filtered_transactions_by_category = []
    filtered_transactions_by_description = []
    pattern = re.compile(r"\b[А-Я][а-я]+\s[А-Я]\.")
    for transaction in list_of_transaction:
        if transaction["Категория"] == "Переводы":
            filtered_transactions_by_category.append(transaction)
    for each_transaction in filtered_transactions_by_category:

        description = each_transaction["Описание"]
        match = pattern.search(f"{description}")
        if match:
            filtered_transactions_by_description.append(each_transaction)

    return json.dumps(filtered_transactions_by_description, indent=4, ensure_ascii=False)


# transactions_data = pd.read_excel(DATA_DIR) # Получаем данные транзакций из operations.xlsx
# transactions = transactions_data.to_dict(orient="records") # Преобразуем данные в список словарей
# print(get_transfers(transactions)) # Вызов функции
