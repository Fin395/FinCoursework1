import datetime
import pytest
from math import nan
from sqlite3 import Timestamp
from typing import Any
from unittest.mock import Mock, patch, mock_open

from config import JSON_DIR
from src.utils import get_greetings, filter_transactions_by_period, get_cards, get_top_transactions, get_currencies, \
    get_stocks, get_currency_rate, get_stock_price

@pytest.mark.parametrize(
    "sample_dates, expected",
    [
        ("2018-01-02 23:59:59", "Добрый вечер"),
        ("2018-01-02 15:59:59", "Добрый день"),
        ("2018-01-02 10:59:59", "Доброе утро"),
        ("2018-01-02 05:59:59", "Доброй ночи"),
    ],
)
def test_get_greetings(sample_dates: str, expected: str) -> None:
    """ Тестирование корректности приветствия """
    assert get_greetings(sample_dates) == expected

#def test_filter_transactions_by_period(sample_transactions):
#    result = filter_transactions_by_period(sample_transactions, "2018-01-02 23:59:59")
#    assert result == [{'MCC': nan,
#  'Бонусы (включая кэшбэк)': 0,
#  'Валюта операции': 'RUB',
#  'Валюта платежа': 'RUB',
#  'Дата операции': '2018-01-01 12:49:53',
#  'Дата платежа': '01.01.2018',
#  'Категория': 'Переводы',
#  'Кэшбэк': nan,
#  'Номер карты': nan,
#  'Округление на инвесткопилку': 0,
#  'Описание': 'Линзомат ТЦ Юность',
#  'Статус': 'OK',
#  'Сумма операции': -3000.0,
#  'Сумма операции с округлением': 3000.0,
#  'Сумма платежа': -3000.0}]


def test_get_cards(sample_transactions: list[dict]) -> None:
    """ Проверяем корректность выборки """
    assert get_cards(sample_transactions) == [{'cashback': 0.0, 'last_digits': '*7197', 'total_spent': -21.0}]


def test_get_top_transactions(sample_top_transactions: list[dict]) -> None:
    """ Проверяем корректность выборки """
    assert get_top_transactions(sample_top_transactions) == [{'amount': -45658.0,
  'category': 'Красота',
  'date': '01.03.2018',
  'description': 'OOO Balid'},
 {'amount': -3000.0,
  'category': 'Переводы',
  'date': '01.01.2018',
  'description': 'Линзомат ТЦ Юность'},
 {'amount': -745.0,
  'category': 'Красота',
  'date': '01.04.2018',
  'description': 'OOO Balid'},
 {'amount': -50.0,
  'category': 'Переводы',
  'date': '01.01.2018',
  'description': 'Линзомат ТЦ Юность'},
 {'amount': -21.0,
  'category': 'Красота',
  'date': '03.01.2018',
  'description': 'OOO Balid'}]


def test_get_currencies() -> None:
    """Тестирование корректного получения наименований валюты"""
    mocked_open = mock_open(read_data='{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}')
    with patch("builtins.open", mocked_open):
        result = get_currencies(JSON_DIR)
        assert result == ["USD", "EUR"]


def test_get_currencies_invalid_path() -> None:
    """Тестирование работы функции при ошибочно указанном пути к файлу"""
    assert get_currencies("user_settings") == []


def test_get_currencies_empty_file() -> None:
    """Тестирование корректного чтения пустого файла"""
    mocked_open = mock_open(read_data=None)
    with patch("builtins.open", mocked_open):
        result = get_currencies(JSON_DIR)
        assert result == []


def test_get_stocks() -> None:
    """Тестирование корректного получения наименований акций"""
    mocked_open = mock_open(read_data='{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}')
    with patch("builtins.open", mocked_open):
        result = get_stocks(JSON_DIR)
        assert result == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def test_get_stocks_invalid_path() -> None:
    """Тестирование работы функции при ошибочно указанном пути к файлу"""
    assert get_stocks("user_settings") == []


def test_get_stocks_empty_file() -> None:
    """Тестирование корректного чтения пустого файла"""
    mocked_open = mock_open(read_data=None)
    with patch("builtins.open", mocked_open):
        result = get_stocks(JSON_DIR)
        assert result == []


@patch("requests.request")
def test_get_currency_rate(mock_request: Any) -> None:
    """ Проверяем корректность получения данных по курсу валют """
    mock_request.return_value.json.return_value = [{'base': 'USD', 'rates': {'RUB': 74.098804}}, {'base': 'EUR', 'date': '2021-12-20', 'rates': {'RUB': 83.567092}}]
    result = get_currency_rate(["USD", "EUR"], "2021-12-20 23:59:59")
    assert result == [{'currency': 'USD', 'rate': 74.1}, {'currency': 'EUR', 'rate': 83.57}]


@patch("requests.request")
def test_get_stock_price(mock_request: Any) -> None:
    """ Проверяем корректность получения данных по цене акций """
    mock_request.return_value.json.return_value = [{'data': [{'close': 254.49, 'symbol': 'AAPL'}]}, {'data': [{'close': 224.92, 'symbol': 'AMZN'}]}, {'data': [{'close': 191.41, 'symbol': 'GOOGL'}]}, {'data': [{'close': 436.6, 'symbol': 'MSFT'}]}, {'data': [{'close': 421.06, 'symbol': 'TSLA'}]}]
    result = get_stock_price(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],"2024-12-20 23:59:59")
    assert result == [{'stock': 'AAPL', 'price': 254.49}, {'stock': 'AMZN', 'price': 224.92}, {'stock': 'GOOGL', 'price': 191.41}, {'stock': 'MSFT', 'price': 436.6}, {'stock': 'TSLA', 'price': 421.06}]


def test_get_currency_rate_if_failed() -> None:
        """Тестирование функции в случае возникновения ошибки"""
        mock_response = Mock()
        mock_response.status_code = 500
        with patch("requests.get", return_value=mock_response):
            assert get_currency_rate(["USD", "EUR"], "2021-12-20 23:59:59") == []


def test_get_stock_price_if_failed() -> None:
    """Тестирование функции в случае возникновения ошибки"""
    mock_response = Mock()
    mock_response.status_code = 500
    with patch("requests.get", return_value=mock_response):
        assert get_stock_price(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],"2024-12-20 23:59:59") == []
