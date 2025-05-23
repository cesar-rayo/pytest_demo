import logging
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.extra.pandas import column, data_frames
from hypothesis.strategies import composite, lists, floats, integers, from_regex
from dataclasses import dataclass
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
    return freq / len(values)


first_digit_freq_strategy = arrays(
    # each element in array will be a 64-bit signed integer.
    dtype=np.int64,
    # arrays lengths (shapes) between 1 and 10,000 elements
    # c = 10_000_000_000
    # print(c) # Output: 10000000000
    # _ introduced in python 3.6 to improve readability
    shape=integers(min_value=1, max_value=10_000),
    # strategy for generating the individual elements from 0 till 9223372036854775806
    elements=integers(min_value=0, max_value=np.iinfo(np.int64).max - 1)
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


@dataclass
class Sale:
    sku: str
    price: int


def sku_sales(sales_list: list[Sale]):
    by_sku = {}
    for sale in sales_list:
        by_sku[sale.sku] = by_sku.get(sale.sku, 0) + sale.price
    return by_sku


@composite
def sales(draw):
    # Generate sku like "1234ABCD", "F00BA7C1", "98765432", "ABCDEF01", "BBBBBBBB", "00000000"
    sku = draw(from_regex(r'[A-F0-9]{8}', fullmatch=True))
    # Generate random prices from 1 till 10.000
    price = draw(integers(min_value=1, max_value=10_000))
    return Sale(sku, price)


EARTH_RADIUS_KM = 6373


def calculate_distance(lat1, lng1, lat2, lng2):
    """Returns distance in km between two coordinates"""
    # co_lat = 90 − latitude (if latitude is measured from the equator, 0 to 90 North/South)

    # phi1: The angular distance from the pole to Point 1.
    phi1 = np.deg2rad((90 - lat1))

    # phi2: The angular distance from the pole to Point 2
    phi2 = np.deg2rad((90 - lat2))

    theta1 = np.deg2rad(lng1)
    theta2 = np.deg2rad(lng2)

    # Spherical Law of Cosines: cos(Δσ) = sin(co_lat1) * sin(co_lat2) * cos(Δλ) + cos(co_lat1) * cos(co_lat2)
    cos = (np.sin(phi1) * np.sin(phi2) * np.cos(theta1 - theta2) + np.cos(phi1) * np.cos(phi2))
    # Trigonometric inverse cosine
    arc = np.arccos(cos)
    return arc * EARTH_RADIUS_KM


@composite
def calculate_distance_inputs(draw):
    test_input = {
        "lat1": draw(floats(min_value=-90, max_value=90, allow_nan=False)),
        "lng1": draw(floats(min_value=-180, max_value=180, allow_nan=False)),
        "lat2": draw(floats(min_value=-90, max_value=90, allow_nan=False)),
        "lng2": draw(floats(min_value=-180, max_value=180, allow_nan=False))
    }
    return test_input


@composite
def generate_lats(draw):
    return draw(floats(min_value=-90, max_value=90, allow_nan=False))


@composite
def generate_lngs(draw):
    return draw(floats(min_value=-180, max_value=180, allow_nan=False))


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

    @given(sale=sales())
    def test_sale_creation(self, sale):
        logging.info(sale)
        assert isinstance(sale, Sale)
        assert len(sale.sku) == 8
        # Check first character in sku is between A - F or 0 - 9 range it uses ASCII char comparison
        assert 'A' <= sale.sku[0] <= 'F' or '0' <= sale.sku[0] <= '9'
        assert 1 <= sale.price <= 10_000

    @given(lists(elements=sales()))
    def test_sku_sales(self, sales_list):
        by_sku = sku_sales(sales_list)
        logging.info(by_sku)
        # get a unique collection of the dictionary keys and check if the key is contained in the first dict.
        unknown = set(by_sku) - set(sale.sku for sale in sales_list)
        assert not unknown

    @given(test_input=calculate_distance_inputs())
    def test_sale_creation(self, test_input):
        distance = calculate_distance(test_input['lat1'], test_input['lng1'], test_input['lat2'], test_input['lng2'])
        logging.info(f"P1: [{test_input['lat1']},{test_input['lng1']}] - "
                     f"P2: [{test_input['lat2']},{test_input['lng2']}]")
        logging.info(f"Distance {distance} km")
        if not np.isnan(distance):
            assert distance >= 0

    @given(generate_lats(), generate_lngs(), generate_lats(), generate_lngs())
    def test_sale_creation_2(self, lat1, lng1, lat2, lng2):
        distance = calculate_distance(lat1, lng1, lat2, lng2)
        logging.info(f"P1: [{lat1},{lng1}] - "
                     f"P2: [{lat2},{lng2}]")
        logging.info(f"Distance {distance} km")
        # We use np.isnan since np.nan == np.nan: False
        if not np.isnan(distance):
            assert distance >= 0
