import logging
import sys
import os
import pytest
from io import StringIO
from pytest import raises

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from files_reader import csv_reader, json_reader, altitude_stat_per_country, csv_writer

CLEAN_MAP_PATH = "../files/clean_map.csv"
MALFORMED_MAP_PATH = "../files/malformed_map.csv"
FILES_PATH = "../files"
EXPECTED_HEADERS = [
    "Country",
    "City",
    "State_Or_Province",
    "Lat",
    "Long",
    "Altitude"
]
STRING_FIELDS = [
    "Country",
    "City",
    "State_Or_Province"
]
FLOAT_FIELDS = [
    "Lat",
    "Long",
    "Altitude"
]


# @pytest.fixture(scope="module")
# def city_file_location():
#     return CLEAN_MAP_PATH


@pytest.fixture(scope="module")
def read_csv_file():
    logging.info(f"Reading file from [{CLEAN_MAP_PATH}]")
    yield csv_reader(CLEAN_MAP_PATH)


# Return a function as fixture
@pytest.fixture(scope="module")
def this_file_process_data():
    files = os.listdir(FILES_PATH)

    def _specify_type(file_name_or_type):
        for f in files:
            if file_name_or_type in f:
                if ".json" in file_name_or_type:
                    data = json_reader(f"{FILES_PATH}/{file_name_or_type}")
                else:
                    data = csv_reader(f"{FILES_PATH}/{file_name_or_type}")
        return data
    yield _specify_type


class TestCSVReader:
    def test_canReadCSVData(self, read_csv_file):
        data = read_csv_file
        headers = list(data[0].keys())
        assert headers == EXPECTED_HEADERS

    def test_canReadCSVFile(self, read_csv_file):
        data = read_csv_file
        for row in data:
            for str_field in STRING_FIELDS:
                assert isinstance(row[str_field], str)
            for float_field in FLOAT_FIELDS:
                assert isinstance(row[float_field], float)
        assert len(data) == 180
        assert data[0]['Country'] == "Andorra"
        assert data[179]['Country'] == "United States"

    def test_canReadJsonFile(self, this_file_process_data):
        data = this_file_process_data(file_name_or_type="scooter_data.json")
        assert data[0]['vin_number'] == "WAUVC68E85A398654"
        assert data[-1]['vin_number'] == "1HGCR2E32DA700167"

    def test_canThrowValueErrorException(self):
        with raises(ValueError) as exp:
            data = csv_reader(MALFORMED_MAP_PATH)
            logging.info(f"Never reached {data}")
        assert "could not convert string to float" in str(exp.value)
        assert str(exp.value) == "could not convert string to float: 'not_an_altitude'"

    def test_average_altitude_per_country(self, this_file_process_data):
        data = this_file_process_data(file_name_or_type="clean_map.csv")
        andorran_avg_res = altitude_stat_per_country(data, 'Andorra', 'Mean')

        assert andorran_avg_res == {'Country': 'Andorra', 'Mean': 1641.42}

    def test_median_altitude_per_country(self, this_file_process_data):
        data = this_file_process_data(file_name_or_type="clean_map.csv")
        andorran_median_res = altitude_stat_per_country(data, 'Andorra', 'Median')

        assert andorran_median_res == {'Country': 'Andorra', 'Median': 1538.02}

    @pytest.mark.parametrize("country,stat,expected", [
        ("Andorra", "Mean", 1641.42),
        ("Andorra", "Median", 1538.02),
        ("Argentina", "Median", 125.0)
    ])
    def test_altitude_stat_per_country(self, this_file_process_data, country, stat, expected):
        data = this_file_process_data(file_name_or_type="clean_map.csv")
        actual_stat = altitude_stat_per_country(data, country, stat)
        assert actual_stat == {'Country': country, stat: expected}

    def test_canWriteDataInFile(self, this_file_process_data):
        data = this_file_process_data(file_name_or_type="clean_map.csv")
        country_median_res = altitude_stat_per_country(data, 'Andorra', 'Median')
        output_location = StringIO()
        csv_writer(country_median_res, output_location)
        answer = output_location.getvalue().strip('\r\n')
        assert answer == "Country,Median\r\nAndorra,1538.02"

    @pytest.mark.parametrize("country,stat,expected", [
        ("Andorra", "Mean", 1641.42),
        ("Andorra", "Median", 1538.02),
        ("Argentina", "Median", 125.0)
    ])
    def test_canWriteMultipleDataInFile(self, this_file_process_data, country, stat, expected):
        data = this_file_process_data(file_name_or_type="clean_map.csv")
        country_median_res = altitude_stat_per_country(data, country, stat)
        output_location = StringIO()
        csv_writer(country_median_res, output_location)
        answer = output_location.getvalue().strip('\r\n')
        assert answer == f"Country,{stat}\r\n{country},{expected}"
