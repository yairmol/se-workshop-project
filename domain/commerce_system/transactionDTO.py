from domain.commerce_system.productDTO import ProductDTO


class TransactionDTO:
    def __init__(self, shop, products: list[ProductDTO], payment_details, date, price):
        self.shop = shop
        self.products = products
        self.payment_details = payment_details
        self.date = date
        self.price = price

# class CartTransactionDTO:
#     def __init__(self, transactions: list[TransactionDTO], payment_details, date, price):
#         self.transactions = transactions
#         self.payment_details = payment_details
#         self.date = date
#         self.price = price
