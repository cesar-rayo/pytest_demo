import pytest
import sys
import os
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)
from main import is_prime, get_weather, save_user


@pytest.mark.parametrize("num, expected", [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (18, False),
    (19, True),
    (25, False),
])
def test_is_prime(num, expected):
    assert is_prime(num) == expected


def test_get_weather(mocker):
    logging.info("Mocking get request")
    # mock any get method from requests in main fail
    mock_get = mocker.patch("main.requests.get")
    # here we can set the value for the specific attribute 'status_code'
    mock_get.return_value.status_code = 200
    # return_value is used here since json is a function
    mock_get.return_value.json.return_value = {"temperature": 25, "condition": "Sunny"}

    result = get_weather("Dubai")
    logging.info(result)
    assert result == {"temperature": 25, "condition": "Sunny"}
    mock_get.assert_called_once_with("https://api.weather.com/v1/Dubai")


def test_save_user(mocker):
    logging.info("Mocking bd connection")
    mock_conn = mocker.patch("sqlite3.connect")
    logging.info("Mocking cursor")
    mock_cursor = mock_conn.return_value.cursor.return_value

    save_user("Alice", 30)

    mock_conn.assert_called_once_with("users.db")
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (name, age) VALUE (?, ¿)", ("Alice", 30)
    )

