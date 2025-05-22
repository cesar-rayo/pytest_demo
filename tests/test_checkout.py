import pytest
import sys
import os
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from checkout import Checkout


@pytest.fixture()
def checkout():
    checkout = Checkout()
    checkout.addItemPrice("a", 1)
    checkout.addItemPrice("b", 3)
    checkout.addItemPrice("c", 4)
    return checkout


class TestCheckout:
    @pytest.mark.skip
    def test_CanInstantiateCheckout(self, checkout):
        logging.info("Skipped test case")
        assert True

    def test_CanCalculateTotal(self, checkout):
        checkout.addItem("a")
        assert checkout.calculateTotal() == 1

    def test_GetCorrectTotalWithMultipleItems(self, checkout):
        checkout.addItem("a")
        checkout.addItem("b")
        checkout.addItem("c")
        assert checkout.calculateTotal() == 8

    def test_CanAddDiscountRule(self, checkout):
        checkout.addDiscount("a", 3, 2)

    def test_canApplyDiscountRule(self, checkout):
        checkout.addDiscount("a", 3, 2)
        checkout.addItem("a")
        checkout.addItem("a")
        checkout.addItem("a")
        assert checkout.calculateTotal() == 2

    def test_ExceptionWithBadItem(self, checkout):
        with pytest.raises(Exception):
            checkout.addItem("d")

