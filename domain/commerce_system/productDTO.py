from data_model import ProductModel as Pm
from domain.commerce_system.product import Product
from domain.commerce_system.shopping_cart import ProductInBag


class ProductDTO:

    def __init__(self, product: Product, bag_info: ProductInBag):
        self.product_id = product.product_id
        self.name = product.product_name
        self.price = product.price
        self.description = product.description
        self.amount = bag_info.amount
        self.purchase_type = bag_info.purchase_type

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
            Pm.AMOUNT: self.amount,
            Pm.PURCHASE_TYPE: self.purchase_type.to_dict()
        }
