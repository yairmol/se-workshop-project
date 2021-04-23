from datetime import datetime
from typing import List, Optional

from domain.commerce_system.action import ActionPool
from domain.commerce_system.productDTO import ProductDTO


SHOP = "shop"
PRODUCTS = "products"
DATE = "date"
PRICE = "price"


class Transaction:
    def __init__(self, shop, products: List[ProductDTO], payment_details, date: datetime, price: float):
        self.shop = shop
        self.products = products
        self.payment_details = payment_details
        self.date = date
        self.price = price
        self._transaction_action_pool: Optional[ActionPool] = None

    def to_dict(self):
        return {
            SHOP: self.shop.to_dict(include_products=False),
            PRODUCTS: list(map(lambda p: p.to_dict(), self.products)),
            DATE: self.date.timestamp(),
            PRICE: self.price,
        }

    def set_transaction_action_pool(self, action_pool: ActionPool):
        self._transaction_action_pool = action_pool

    def cancel_transaction(self):
        self._transaction_action_pool.cancel_actions()

# class CartTransactionDTO:
#     def __init__(self, transactions: list[TransactionDTO], payment_details, date, price):
#         self.transactions = transactions
#         self.payment_details = payment_details
#         self.date = date
#         self.price = price
