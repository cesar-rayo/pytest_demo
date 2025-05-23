import logging
import os
import sys
import numpy as np
import pandas as pd
import pandera as pa
from pandera import check_output
from random import random, seed
from pandas.testing import assert_frame_equal
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

FILES_PATH = "../files"


# {"time":"2021-07-13T14:36:52.380Z","metric":"mem","value":227542823.0}
# {"time":"2021-07-13T14:36:52.380Z","metric":"cpu","value":30.3}
def load_metrics(json_file_name):
    return pd.read_json(
        f"{FILES_PATH}/{json_file_name}",
        orient='records',
        lines=True,
        convert_dates=['time']
    )


METRICS_SCHEMA = pa.DataFrameSchema({
    # "time": pa.Column(dtype="datetime64[ns, UTC]"), # time in nanoseconds and UTC
    # element_wise is a boolean that indicates that the lambda/function should be applied to the data in the column.
    # "metric": pa.Column(str, checks=(pa.Check(lambda name: name in ['cpu', 'mem'], element_wise=True))),
    # "value": pa.Column(pd.Float64Dtype, checks=pa.Check.greater_than(0))
    "time": pa.Column(pd.DatetimeTZDtype('ns', 'UTC')),
    "metric": pa.Column(pa.String, checks=pa.Check.isin({"cpu", "mem"})),
    "value": pa.Column(pa.Float, checks=pa.Check.greater_than(0))
})


# @pa.check_output(METRICS_SCHEMA)
@check_output(METRICS_SCHEMA)
def load_metrics_and_check(json_file_name):
    return pd.read_json(
        f"{FILES_PATH}/{json_file_name}",
        orient='records',
        lines=True,
        convert_dates=['time']
    )


class TestComplexNumbers:
    def test_random(self):
        seed(1)
        # r1: 0.13436424411240122, r2: 0.8474337369372327, r3: 0.763774618976614
        logging.info(f"r1: {random()}, r2: {random()}, r3: {random()}")

    def test_numbers(self):
        v1 = np.array([0.1, np.nan, 1.1])
        n = 1.1
        output = v1 * n
        expected = np.array([0.11, np.nan, 1.21])
        # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        # assert output == expected
        assert np.allclose(expected, output, equal_nan=True)

    def test_model(self):
        output = pd.DataFrame({
            "id": [1, 2, 3, 4],
            "is_fraud": [0.1, 0.97, 0.3, 0.2]
        })

        expected = pd.DataFrame({
            "id": [1, 2, 3, 4],
            "is_fraud": [0.1, 0.972, 0.3, 0.2]
        })
        # ValueError: The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all()
        # assert output == expected
        assert_frame_equal(output, expected, atol=0.01)

    def test_load_metrics(self):
        data = load_metrics("metrics.jsonl")
        METRICS_SCHEMA.validate(data)

    def test_load_metrics_and_check(self):
        load_metrics("metrics.jsonl")
