from domain.commerce_system.shop import Shop


class TransactionDTO:
    def __init__(self, shops_products, payment_details, date, price):
        self.shops_products = shops_products
        self.payment_details = payment_details
        self.date = date
        self.price = price

