from domain.commerce_system.product import Product


class ProductDTO:
    def __init__(self, name: str, base_price: float, description: str, quantity: int):
        self.name = name
        self.price = base_price
        self.description = description
        self.quantity = quantity

    def __init__(self, product: Product, amount_to_buy: int):
        self.name = product.name
        self.price = product.price
        self.description = product.description
        self.amount = amount_to_buy
