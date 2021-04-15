from typing import List


class Product:
    def __init__(
            self, name: str, base_price: float, description: str = "",
            quantity: int = 1, categories=None
    ):
        if categories is None:
            categories = []
        self.name = name
        self.price = base_price
        self.description = description
        self.quantity = quantity
        self.categories = categories
