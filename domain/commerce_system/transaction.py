from datetime import datetime

from domain.commerce_system.productDTO import ProductDTO


SHOP = "shop"
PRODUCTS = "products"
DATE = "date"
PRICE = "price"


class Transaction:
    def __init__(self, shop, products: list[ProductDTO], payment_details, date: datetime, price: float):
        self.shop = shop
        self.products = products
        self.payment_details = payment_details
        self.date = date
        self.price = price

    def to_dict(self):
        return {
            SHOP: self.shop.to_dict(),
            PRODUCTS: list(map(lambda p: p.to_dict(), self.products)),
            DATE: self.date.timestamp(),
            PRICE: self.price,
        }

# class CartTransactionDTO:
#     def __init__(self, transactions: list[TransactionDTO], payment_details, date, price):
#         self.transactions = transactions
#         self.payment_details = payment_details
#         self.date = date
#         self.price = price
