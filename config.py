import os

ROOT_DIR = os.path.dirname(__file__)
LOGS_FILE_SERVICES = os.path.join(ROOT_DIR, "logs", "services.log")
LOGS_FILE_UTILS = os.path.join(ROOT_DIR, "logs", "utils.log")
LOGS_FILE_VIEWS = os.path.join(ROOT_DIR, "logs", "views.log")
LOGS_FILE_REPORTS = os.path.join(ROOT_DIR, "logs", "reports.log")

DATA_DIR = os.path.join(ROOT_DIR, "data", "operations.xlsx")
JSON_DIR = os.path.join(ROOT_DIR, "user_settings.json")

REPORTS_DEFAULT_JSON = os.path.join(ROOT_DIR, "data", "default_reports.json")
REPORTS_SPECIFIED_JSON = os.path.join(ROOT_DIR, "data", "specified_reports.json")
