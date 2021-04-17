from domain.commerce_system.product import Product


class Shop:
    def __init__(self, shop_id: int):
        self.shop_id = shop_id
        self.products = {}
        self.transaction_history = []

    """ quantity has to be no more than available product quantity"""
    def sell_product(self, product_id: str, quantity: int, payment_details: dict) -> bool: # add payment
        available_quantity = self.products[product_id].quantity
        if available_quantity < quantity:
            return False
        return True

    """ returns product_id if successful"""
    def add_product(self, product: Product) -> int:
        product_id = self.get_free_id()
        self.products[product_id] = product
        return product_id

    def delete_product(self, product_id: int) -> bool:
        res = self.products.pop(product_id, 0)
        return res != 0

    """ edit product receives product id and a dict of fields to alter and the new values.
        MAKE SURE THE FIELD NAMES ARE ACCURATE"""
    def edit_product(self, product_id, **to_edit) -> bool:
        if product_id not in self.products:
            raise Exception("no product with id=", product_id)
        product = self.products[product_id]
        for field, new_value in to_edit.items():
            if field not in product.__dict__:
                raise Exception("product has no field ", field)
            product.__dict__[field] = new_value

    def get_shop_info(self) -> str:
        s = ""
        for p_id, p_val in self.products:
            s += "store product id: ", p_id, "\nproduct id: ", p_val.product_id, "\nproduct name: ",\
                 p_val.name, "\nprice: ", p_val.price
        return s

    def get_free_id(self) -> int:
        last_id = 1
        for product_id in sorted(self.products.keys()):
            if product_id > last_id + 1:
                return last_id + 1
            last_id = product_id
        return last_id + 1

    """ return true if shop has product named product_name"""
    def has_product(self, product_name: str):
        found = False
        for supply_product in self.products.values():
            found = found or supply_product.name == product_name
        return found

    """ returns id of first product named product_name"""
    def get_id(self, product_name: str):
        product_id = -1
        for p_id, supply_product in self.products.items():
            if supply_product.name == product_name:
                product_id = p_id
        return product_id

    def add_transaction(self, transaction):
        pass