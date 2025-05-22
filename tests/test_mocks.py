import logging
import sys
import os
from unittest.mock import MagicMock, mock_open

import pytest
from pytest import raises

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from linereader import readFromFile


@pytest.fixture()
def mock_opener(monkeypatch):
    mock_file = MagicMock()
    mock_file.readline = MagicMock(return_value="test line")
    mock_opener = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_opener)
    return mock_opener


@pytest.fixture()
def mock_mocker_opener(mocker):
    mock_opener = mock_open(read_data="test line")
    mocker.patch("builtins.open", mock_opener)
    return mock_opener


class DummyClass:
    def __init__(self, city):
        if not isinstance(city, str):
            raise TypeError(f"Invalid type for city {type(city)}")
        else:
            self.city = city


class TestLineReader:
    def test_returnsCorrectString(self, mock_opener, monkeypatch):
        mock_exists = MagicMock(return_value=True)
        monkeypatch.setattr("os.path.exists", mock_exists)
        result = readFromFile("filename.txt")
        mock_opener.assert_called_once_with("filename.txt", "r")
        assert result == "test line"

    def test_throwsExceptionWithBadFile(self, mock_opener, monkeypatch):
        mock_exists = MagicMock(return_value=False)
        monkeypatch.setattr("os.path.exists", mock_exists)

        with raises(Exception):
            result = readFromFile("filename.txt")
            logging.info(result)
        mock_exists.assert_called_once_with("filename.txt")
        mock_opener.assert_not_called()

    def test_returnsCorrectStringMocker(self, mock_mocker_opener, mocker):
        mock_exists = MagicMock(return_value=True)
        mocker.patch("os.path.exists", mock_exists)
        result = readFromFile("filename.txt")
        mock_mocker_opener.assert_called_once_with("filename.txt", "r")
        assert result == "test line"

    def test_throwsExceptionWithBadFileMocker(self, mock_mocker_opener, mocker):
        mock_exists = mocker.patch("os.path.exists", return_value=False)
        mock_file = MagicMock()
        mock_file.readline.return_value = "test line"

        with raises(Exception) as exp:
            result = readFromFile("filename.txt")
            logging.info(result)
#        breakpoint()
#        {k: v for k, v in locals().items() if '__' not in k and 'pdb' not in k}
#        print(exp)
#        print(exp.value)
        assert str(exp.value) == "File does not exists"
        mock_exists.assert_called_once_with("filename.txt")
        mock_mocker_opener.assert_not_called()

    def test_throwsTypeErrorException(self):
        with raises(TypeError) as exp:
            dummy = DummyClass(1)
            logging.info(dummy)
        assert "Invalid type for city" in str(exp.value)
