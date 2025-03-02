import pandas as pd

from config import DATA_DIR
from src.reports import spending_by_category
from src.services import get_transfers
from src.views import get_main_page

all_operations = pd.read_excel(DATA_DIR, na_filter=True)
all_operations_as_list_dict = all_operations.to_dict(orient="records")
main_page_json_info = get_main_page(all_operations_as_list_dict, "2021-12-20 23:59:59")
print(main_page_json_info)
services_info = get_transfers(all_operations_as_list_dict)
print(services_info)
spending_by_category(all_operations, "Цветы", "2019-12-10 23:30:12")
