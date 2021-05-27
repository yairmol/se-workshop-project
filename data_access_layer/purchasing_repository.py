from domain.commerce_system.shopping_cart import ShoppingBag, ShoppingCart
from domain.commerce_system.transaction import Transaction
from init_tables import engine
from sqlalchemy.orm import Session


def save_shopping_bag(shopping_bag: ShoppingBag):
    pass


def save_shopping_cart(shopping_cart: ShoppingCart):
    pass


def save_transaction(transaction: Transaction):
    with Session(engine) as session:
        session.add(transaction)
        session.commit()

        # TODO: save transacion's products
