import pytest
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from files_reader import csv_reader, json_reader

FILES_PATH = "../files"


@pytest.fixture(scope="module")
def process_data():
    files = os.listdir(FILES_PATH)

    def _specify_type(file_name_or_type):
        for f in files:
            if file_name_or_type in f:
                if file_name_or_type != ".json":
                    data = csv_reader(f"{FILES_PATH}/{file_name_or_type}")
                else:
                    data = json_reader(f"{FILES_PATH}/{file_name_or_type}")
        return data
    yield _specify_type
