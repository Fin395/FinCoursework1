import json
import re
import logging
from typing import Any

import pandas as pd

from config import LOGS_FILE_SERVICES, DATA_DIR

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOGS_FILE_SERVICES, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transfers(list_of_transaction: list[dict]) -> Any:
    """ Выбираем из списка транзакций переводы физическим лица """
    filtered_transactions_by_category = []
    filtered_transactions_by_description = []
    pattern = re.compile(r"\b[А-Я][а-я]+\s[А-Я]\.")

    for transaction in list_of_transaction:
        try:
            if transaction["Категория"] == "Переводы":
                logger.info("Транзакция добавлена в список")
                filtered_transactions_by_category.append(transaction)
        except Exception as e:
            logger.error("Ошибка: неверно указаны данные")
            print(f"Ошибка {e}: не удалось обработать данные")
            return []

    for each_transaction in filtered_transactions_by_category:
        try:
            description = each_transaction["Описание"]
        except Exception as e:
            logger.error("Ошибка: неверно указаны данные")
            print(f"Ошибка {e}: не удалось обработать данные")
            return []
        else:
            match = pattern.search(f"{description}")
            if match:
                logger.info("Транзакция добавлена в список")
                filtered_transactions_by_description.append(each_transaction)

    return json.dumps(filtered_transactions_by_description, indent=4, ensure_ascii=False)


transactions_data = pd.read_excel(DATA_DIR) # Получаем данные транзакций из operations.xlsx
#print(transactions_data.to_dict(orient="records"))
transactions = transactions_data.to_dict(orient="records") # Преобразуем данные в список словарей
print(get_transfers(transactions)) # Вызов функции
