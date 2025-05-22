import logging
import pytest
import sys
from os import environ
import numpy as np

# Check if CI in environment variables, often when running on CI the variable is present and set with 1 or True values
in_ci = 'CI' in environ
ci_only = pytest.mark.skipif(
    not in_ci,
    reason="not in CI"
)
windows_only = pytest.mark.skipif(
    sys.platform != "win32",
    reason="Intended to run on Windows only"
)


def scale(v, cutoff, factor):
    """
    Scale values above cutoff by factor
    data = np.array([5, 10, 15, 20, 25])

    my_cutoff = 15
    my_factor = 2

    scaled_data = scale(data, my_cutoff, my_factor)
    Original data: [ 5 10 15 20 25]
    Scaled data: [ 5 10 30 40 50]
    """
    v = v.copy()
    # Iterates numpy array and compares if value >= cutoff
    v[v >= cutoff] *= factor
    return v


VECTOR = np.array([0.1, 1.0, 1.1])
SCALE_CASES = [
    [VECTOR, 1, 1.1, [0.1, 1.1, 1.21]],
    [VECTOR, VECTOR.max() + 1, 0, VECTOR]
]


class TestTransformers:
    def test_scale(self):
        out = scale(VECTOR, 1, 1.1)
        logging.info(f"out: {out}")
        expected = np.array([0.1, 1.1, 1.21])
        logging.info(f"expected: {expected}")
        assert np.allclose(expected, out)

    @pytest.mark.parametrize(
        'vector, cutoff, factor, expected',
        SCALE_CASES,
        ids=[
            "test_vector_1",
            "test_vector_2"
        ])
    def test_scale_several_cases(self, vector, cutoff, factor, expected):
        out = scale(vector, cutoff, factor)
        assert np.allclose(expected, out)

    def test_always(self):
        pass

    @ci_only
    def test_in_ci(self):
        pass

    @windows_only
    def test_on_windows(self):
        pass

    @pytest.mark.web
    def test_web(self):
        pass

    @pytest.mark.regression
    def test_ArrayAssert(self):
        assert [1, 2, 3] == [1, 2, 3]
