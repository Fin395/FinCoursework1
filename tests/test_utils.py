from math import nan
import pytest
from typing import Any
from unittest.mock import Mock, patch, mock_open
from datetime import datetime
from config import JSON_DIR
from src.utils import get_greetings, filter_transactions_by_period, get_cards, get_top_transactions, get_currencies, \
    get_stocks, get_currency_rate, get_stock_price


@patch("src.utils.datetime")
def test_get_greetings(mock_datetime: Any) -> None:
    """ Проверяем корректность приветствия в зависимости от времени """
    mock_datetime.now.return_value.hour = 10
    assert get_greetings() == "Доброе утро"
    mock_datetime.now.return_value.hour = 15
    assert get_greetings() == "Добрый день"
    mock_datetime.now.return_value.hour = 20
    assert get_greetings() == "Добрый вечер"
    mock_datetime.now.return_value.hour = 23
    assert get_greetings() == "Доброй ночи"


def test_filter_transactions_by_period(sample_transactions):
    result = filter_transactions_by_period(sample_transactions, "2018-01-02 23:59:59")
    assert result == [
        {
            'Дата операции': '01.01.2018',
            'Дата платежа': '01.01.2018',
            'Номер карты': nan,
            'Статус': 'OK',
            'Сумма операции': -3000.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': -3000.0,
            'Валюта платежа': 'RUB',
            'Кэшбэк': nan,
            'Категория': 'Переводы',
            'MCC': nan,
            'Описание': 'Линзомат ТЦ Юность',
            'Бонусы (включая кэшбэк)': 0,
            'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 3000.0
        }
    ]

for elem1, elem2 in zip(result[0], d[0]):
    if type(result[0][elem1]) is float and np.isnan(result[0][elem1]):
        assert np.isnan(result[0][elem1]) == np.isnan(d[0][elem1])
    else:
        assert result[0][elem1] == d[0][elem2]





def test_get_cards(sample_transactions: list[dict]) -> None:
    """ Проверяем корректность группировки по номеру карты """
    assert get_cards(sample_transactions) == [{'cashback': 0.0, 'last_digits': '*7197', 'total_spent': -21.0}]


def test_get_top_transactions(sample_top_transactions: list[dict]) -> None:
    """ Проверяем корректность выборки по сумме траты """
    assert get_top_transactions(sample_top_transactions) == [{'amount': -45658.0,
  'category': 'Красота',
  'date': '03.01.2018',
  'description': 'OOO Balid'},
 {'amount': -3000.0,
  'category': 'Переводы',
  'date': '01.01.2018',
  'description': 'Линзомат ТЦ Юность'},
 {'amount': -745.0,
  'category': 'Красота',
  'date': '04.01.2018',
  'description': 'OOO Balid'},
 {'amount': -50.0,
  'category': 'Переводы',
  'date': '01.01.2018',
  'description': 'Линзомат ТЦ Юность'},
 {'amount': -21.0,
  'category': 'Красота',
  'date': '01.03.2018',
  'description': 'OOO Balid'}]


@pytest.mark.parametrize("sample_path_to_json_file, expected", [(JSON_DIR, ["USD", "EUR"]), ("user_settings", [])])
def test_get_currencies(sample_path_to_json_file: str, expected: str) -> None:
    """Тестирование корректности получения списка валют из файла при верно- и неверно указанном пути"""
    assert get_currencies(sample_path_to_json_file) == expected


@pytest.mark.parametrize("sample_path_to_json_file, expected", [(JSON_DIR, ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]), ("user_settings", [])])
def test_get_stocks(sample_path_to_json_file: str, expected: str) -> None:
    """Тестирование корректности получения списка акций из файла при верно- и неверно указанном пути"""
    assert get_stocks(sample_path_to_json_file) == expected


def test_get_currencies_empty_file() -> None:
    """Тестирование корректного чтения пустого файла"""
    mocked_open = mock_open(read_data=None)
    with patch("builtins.open", mocked_open):
        result = get_currencies(JSON_DIR)
        assert result == []


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
