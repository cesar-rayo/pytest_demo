import logging

import pytest
from pytest import approx, raises


def test_IntAssert():
    assert 1 == 1


def test_StrAssert():
    assert "str" == "str"


def test_FloatAssert():
    assert 1.0 == 1.0


@pytest.mark.smoke
def test_FloatSum():
    answer = (0.1 + 0.2)
    logging.info(answer)
#    assert answer == 0.3
    assert answer == approx(0.3)


@pytest.mark.regression
def test_ArrayAssert():
    assert [1, 2, 3] == [1, 2, 3]


@pytest.mark.regression
def test_DictAssert():
    assert {"one": 1} == {"one": 1}


def raisesValueException():
    logging.info("Raise Exception")
    raise ValueError("Value Error")


def test_ExceptionRaise():
    # Validate ValueError is raised
    with raises(ValueError):
        raisesValueException()
