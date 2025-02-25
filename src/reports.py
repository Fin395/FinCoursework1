import datetime
import logging
from typing import Optional

import pandas as pd

from config import DATA_DIR, LOGS_FILE_REPORTS

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOGS_FILE_REPORTS, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:

    if date:
        end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        end_of_period = datetime.datetime.now()
    logger.info("Рассчитываем 3-х месячный период")
    start_of_period = end_of_period - pd.DateOffset(months=3)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    logger.info("Происходит выборка транзакций за 3 месяца")
    trans_filtered_by_period = transactions.loc[(transactions["Дата операции"] >= start_of_period) & (transactions["Дата операции"] <= end_of_period)]
    logger.info("Отбираем успешные траты")
    trans_filtered_by_spent = trans_filtered_by_period.loc[(trans_filtered_by_period["Сумма платежа"] < 0) & (trans_filtered_by_period["Статус"] == "OK")]
    logger.info(f"Происходит выборка трат по категории: {category}")
    trans_filtered_by_category = trans_filtered_by_spent.loc[(trans_filtered_by_spent["Категория"] == category)]
    trans_filtered_by_category["Дата операции"] = trans_filtered_by_category["Дата операции"].dt.strftime("%d.%m.%Y")

    return trans_filtered_by_category.to_dict(orient="records")

#all_operations = pd.read_excel(DATA_DIR, na_filter=True)
#print(spending_by_category(all_operations, "Цветы", "2019-12-10 23:30:12"))
