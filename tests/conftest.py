# import os
import sys

# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(ROOT_DIR)
sys.path.append("..")

# from tests.conftest_files import process_data

# OR

# Imports fixtures from tests.conftest_files.py
pytest_plugins = [
    "tests.conftest_files"
]
