import json

from config import DATA_DIR
from src.utils import get_greetings, get_cards, filter_transactions_by_period, get_transactions_from_excel, \
    get_top_transactions


def get_main_page(date):
    main_page_dict = dict()
    transactions = get_transactions_from_excel(DATA_DIR)
    transactions_in_timeframe = filter_transactions_by_period(transactions, date)
    greetings = get_greetings()
    cards = get_cards(transactions_in_timeframe)
    top_transactions = get_top_transactions(transactions_in_timeframe)

    main_page_dict["greetings"] = greetings
    main_page_dict["cards"] = cards
    main_page_dict["top_transactions"] = top_transactions

    json_data = json.dumps(main_page_dict, indent=4, ensure_ascii=False)

    return json_data

print(get_main_page("2021-09-30 23:59:59"))