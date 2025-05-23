import os
import sys
import pandas as pd
import pandera as pa
from pandera import check_output
from ipaddress import IPv4Address
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)


FILES_PATH = "../files"


def load_sales(file_name):
    return pd.read_csv(f"{FILES_PATH}/{file_name}", parse_dates=['time'])


def is_ipv4(address):
    try:
        IPv4Address(address)
        return True
    except ValueError:
        return False


# time,value,ip
# 2022-08-05T07:17:23,150,172.27.219.236
# 2022-08-05T07:19:39,114,242.112.145.134
SALES_SCHEMA = pa.DataFrameSchema({
    'time': pa.Column(pd.Timestamp),
    'value': pa.Column(pd.Int64Dtype, checks=pa.Check.greater_than(0)),
    # If element_wise is True, fn is applied to each row in the dataframe
    'ip': pa.Column(str, checks=pa.Check(is_ipv4, element_wise=True))
})


@check_output(SALES_SCHEMA)
def load_sales_and_check_data(file_name):
    return pd.read_csv(f"{FILES_PATH}/{file_name}", parse_dates=['time'])


class TestSchemas:
    def test_load_sales(self):
        df = load_sales("sales.csv")
        SALES_SCHEMA.validate(df)

    def test_load_sales_and_check_data(self):
        load_sales_and_check_data("sales.csv")
