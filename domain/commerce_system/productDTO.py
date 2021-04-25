from data_model import ProductModel as Pm
from domain.commerce_system.product import Product


class ProductDTO:

    def __init__(self, product: Product, amount_to_buy: int):
        self.product_id = product.product_id
        self.name = product.product_name
        self.price = product.price
        self.description = product.description
        self.amount = amount_to_buy

    def __eq__(self, other):
        return (
            isinstance(other, ProductDTO) and
            self.product_id == other.product_id and
            self.amount == other.amount
        )

    def __hash__(self):
        return hash((self.product_id, self.amount))

    def to_dict(self):
        return {
            Pm.PRODUCT_ID: self.product_id,
            Pm.PRODUCT_NAME: self.name,
            Pm.PRICE: self.price,
            Pm.PRODUCT_DESC: self.description,
            Pm.AMOUNT: self.amount
        }
