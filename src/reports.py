import datetime
import logging
from functools import wraps
from typing import Optional, Callable, Any
import json
import pandas as pd

from config import DATA_DIR, LOGS_FILE_REPORTS, REPORTS_DEFAULT_JSON

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOGS_FILE_REPORTS, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def record_to_file(filename: Optional[str] = REPORTS_DEFAULT_JSON) -> Callable:
    """ Создаем декоратор с параметром для функции-отчета """
    def decorator(func: Callable) -> Any:
        """ Создаем вспомогательную функцию для формирования замыкания """
        @wraps(func)
        def wrapper(*args: tuple[tuple, ...], **kwargs: dict[str, Any]) -> Any:
            """ Создаем замыкание """
            result = func(*args, **kwargs)
            with open(filename, "w", encoding='utf-8') as file:
                logger.info(f"Функция {func.__name__} записывает выбранные транзакции в файл {filename}")
                json.dump(result.to_dict(orient="records"), file, indent=4, ensure_ascii=False)
            return result
        return wrapper
    return decorator


@record_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame | str:
    """ Функция отбирает транзакции по тратам по определенной категории """
    try:
        if date:
            end_of_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            end_of_period = datetime.datetime.now()

        logger.info("Рассчитываем 3-х месячный период")
        start_of_period = end_of_period - pd.DateOffset(months=3)
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        logger.info("Происходит выборка транзакций за 3 месяца")
        trans_filtered_by_period = transactions.loc[(transactions["Дата операции"] >= start_of_period) & (transactions["Дата операции"] <= end_of_period)]
        if len(trans_filtered_by_period.to_dict(orient="records")) == 0:
            return "В указанном периоде транзакции отсутствуют"
        logger.info("Отбираем успешные траты")
        trans_filtered_by_spent = trans_filtered_by_period.loc[(trans_filtered_by_period["Сумма платежа"] < 0) & (trans_filtered_by_period["Статус"] == "OK")]
        logger.info(f"Происходит выборка трат по категории: {category}")
        trans_filtered_by_category = trans_filtered_by_spent.loc[(trans_filtered_by_spent["Категория"] == category)].copy()
        trans_filtered_by_category["Дата операции"] = trans_filtered_by_category["Дата операции"].dt.strftime("%d.%m.%Y")

        return trans_filtered_by_category

    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        print(f"Произошла ошибка: {ex}")


transactions_data = pd.read_excel(DATA_DIR, na_filter=True)
spending_by_category(transactions_data, "Цветы", "2019-12-10 23:30:12")
