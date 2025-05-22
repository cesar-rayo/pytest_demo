import logging


class Checkout:
    class Discount:
        def __init__(self, number_of_items, price):
            self.number_of_items = number_of_items
            self.price = price

    def __init__(self):
        self.prices = {}
        self.discounts = {}
        self.items = {}

    def addDiscount(self, item, number_of_items, price):
        discount = self.Discount(number_of_items, price)
        self.discounts[item] = discount

    def addItemPrice(self, item, price):
        self.prices[item] = price

    def addItem(self, item):
        if item in self.prices:
            if item in self.items:
                self.items[item] += 1
            else:
                self.items[item] = 1
        else:
            raise Exception(f"There is no price for item: {item}")

    def calculateTotal(self):
        total = 0
        for item, count in self.items.items():
            total += self.calculateItemTotal(item, count)
        return total

    def calculateItemTotal(self, item, count):
        total = 0
        if item in self.discounts:
            total = self.calculateItemDiscountedTotal(item, count, self.discounts[item])
        else:
            total += self.prices[item] * count
        return total

    def calculateItemDiscountedTotal(self, item, count, discount):
        total = 0
        if count >= discount.number_of_items:
            number_of_discounts = count / discount.number_of_items
            total += number_of_discounts * discount.price
            remaining = count % discount.number_of_items
            total += remaining * self.prices[item]
        else:
            total += self.prices[item] * count
        return total
