
import os
import sys
import pytest
from io import StringIO

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from files_reader import altitude_stat_per_country, csv_writer


class TestCSVReader:
    # Loads fixture from conftest.py
    @pytest.mark.parametrize("country,stat,expected", [
        ("Andorra", "Mean", 1641.42),
        ("Andorra", "Median", 1538.02),
        ("Argentina", "Median", 125.0)
    ])
    def test_altitude_stat_per_country(self, process_data, country, stat, expected):
        data = process_data(file_name_or_type="clean_map.csv")
        actual_stat = altitude_stat_per_country(data, country, stat)
        assert actual_stat == {'Country': country, stat: expected}

    # Loads fixture from conftest.py
    @pytest.mark.parametrize("country,stat,expected", [
        ("Andorra", "Mean", 1641.42),
        ("Andorra", "Median", 1538.02),
        ("Argentina", "Median", 125.0)
    ])
    def test_canWriteMultipleDataInFile(self, process_data, country, stat, expected):
        data = process_data(file_name_or_type="clean_map.csv")
        country_median_res = altitude_stat_per_country(data, country, stat)
        output_location = StringIO()
        csv_writer(country_median_res, output_location)
        answer = output_location.getvalue().strip('\r\n')
        assert answer == f"Country,{stat}\r\n{country},{expected}"
