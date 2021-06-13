from data_access_layer.engine import engine
from sqlalchemy.orm import Session


def save_shopping_cart(shopping_cart):
    with Session(engine) as session:
        session.add(shopping_cart)
        session.commit()


def get_shopping_cart(username: str, shopping_cart_type):
    with Session(engine) as session:
        shopping_cart = session.query(shopping_cart_type).filter_by(username=username).first()
        return shopping_cart


def remove_shopping_cart(username: str, shopping_cart_type):
    with Session(engine) as session:
        shopping_cart = session.query(shopping_cart_type).filter_by(username=username).first()
        session.delete(shopping_cart)
        session.commit()


def save_shopping_bag(shoppingBag):
    with Session(engine) as session:
        session.add(shoppingBag)
        session.commit()


def get_all_shopping_bags(cart_id: int, shopping_bag_type):
    with Session(engine) as session:
        shopping_bags = session.query(shopping_bag_type).filter_by(cart_id=cart_id)
        return shopping_bags


def remove_shopping_bag(shop_id: int, shopping_bag_type):
    with Session(engine) as session:
        shopping_bag = session.query(shopping_bag_type).filter_by(shop_id=shop_id).first()
        session.delete(shopping_bag)
        session.commit()

def save_transaction(transaction):
    with Session(engine) as session:
        session.add(transaction)
        session.commit()

def get_all_transactions(username: str, transaction_type):
    with Session(engine) as session:
        transactions = session.query(transaction_type).filter_by(username=username)
        return transactions


# def remove_shopping_bar(shopping_bag_id: ShoppingBag): # Dont need to remove transactons
#     with Session(engine) as session:
#         shop = session.query(ShoppingBag).filter_by(id=shopping_bag_id).first()
#         session.delete(shop)
#         session.commit()
