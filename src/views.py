import json

from config import DATA_DIR, JSON_DIR
from src.utils import (filter_transactions_by_period, get_cards, get_currencies, get_currency_rate, get_greetings,
                       get_stock_price, get_stocks, get_top_transactions)


def get_main_page(transactions, date: str) -> str:
    """Получаем информацию для главной страницы"""
    main_page_dict = dict()
    transactions_in_timeframe = filter_transactions_by_period(transactions, date)
    greetings = get_greetings()
    cards = get_cards(transactions_in_timeframe)
    top_transactions = get_top_transactions(transactions_in_timeframe)
#    currency_rates = get_currency_rate(get_currencies(JSON_DIR), date)
#    stock_price = get_stock_price(get_stocks(JSON_DIR), date)
    main_page_dict["greetings"] = greetings
    main_page_dict["cards"] = cards
    main_page_dict["top_transactions"] = top_transactions
#    main_page_dict["currency_rates"] = currency_rates
#    main_page_dict["stock_prices"] = stock_price
    main_page_data = json.dumps(main_page_dict, indent=4, ensure_ascii=False)

    return main_page_data


