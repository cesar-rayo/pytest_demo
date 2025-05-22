import logging
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.extra.pandas import column, data_frames
from hypothesis.strategies import floats, integers, from_regex
import numpy as np


def relu(n):
    if n < 0:
        return 0
    return n


def first_digit(n):
    return str(n)[0]


def first_digit_freq(values):
    """
    Calculate frequency: If the digit '1' appears as the first digit 50 times in your data, its frequency is 50.
    Calculate proportion: If the digit '1' appeared 50 times in a list of 1000 numbers, its proportion would be
    50/1000 = 0.05 (or 5%).
    """
    first_digits = [first_digit(n) for n in values]
    # count the occurrences of each unique integer in first_digits
    freq = np.bincount(first_digits, minlength=10)
    return freq/len(values)


first_digit_freq_strategy = arrays(
    # each element in array will be a 64-bit signed integer.
    dtype=np.int64,
    # arrays lengths (shapes) between 1 and 10,000 elements
    # c = 10_000_000_000
    # print(c) # Output: 10000000000
    # _ introduced in python 3.6 to improve readability
    shape=integers(min_value=1, max_value=10_000),
    # strategy for generating the individual elements from 0 till 9223372036854775806
    elements=integers(min_value=0, max_value=np.iinfo(np.int64).max-1)
)


def max_drop(stocks):
    df = stocks.copy()
    # Calculate the daily difference between 'high' and 'low' prices
    df['diff'] = df['high'] - df['low']
    # Group by stock symbol and find the maximum 'diff' for each group
    return df.groupby('symbol')['diff'].max()


stocks_strategy = data_frames([
    # generate random symbols using regex i.e. 'ZMANXVA', 'HRE', 'BANA'
    column('symbol', elements=from_regex(r'[A-Z]{2,7}', fullmatch=True)),
    # generate random floats from 1 to 10.000
    column('high', elements=floats(min_value=1, max_value=10_000)),
    column('low', elements=floats(min_value=1, max_value=10_000))
])


class TestHypothesis:
    # Runs several test cases using floats() strategy
    # Its primary use is to automatically generate a wide range of floating-point numbers (including positive, negative,
    # zero, very small, very large, and potentially special floating-point values like NaN and infinity) to test your
    # code's robustness when dealing with real numbers.
    @given(floats())
    def test_relu(self, n):
        v = relu(n)
        if not np.isnan(n):
            logging.info(f"n: {n}, v: {v}")
            assert v >= 0
        else:
            logging.info(f"Nan value generated, n: {n}")

    @given(first_digit_freq_strategy)
    def test_first_digit_feq(self, values):
        freq = first_digit_freq(values)
        # validate the shape (length) is 10 numbers
        assert freq.shape == (10,)
        # assert len(freq) == 10

        # validate each number is between 0 and 1
        assert ((freq >= 0) & (freq <= 1)).all()

        # the sum of all frequencies is closer to 1
        logging.info(freq)
        logging.info(freq.sum())
        assert np.allclose(freq.sum(), 1)

    @given(stocks_strategy)
    def test_max_drop(self, df):
        out = max_drop(df)
        logging.info(out)
        unknown = set(out.index) - set(df['symbol'])
        # Asserts that no symbols appeared in the output of max_drop that weren't already in the input df
        assert not unknown
