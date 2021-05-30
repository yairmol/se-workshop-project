from sqlalchemy import delete

from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import Condition
from domain.commerce_system.shop import Shop
from init_tables import engine
from sqlalchemy.orm import Session


def save_shop(shop: Shop):
    with Session(engine) as session:
        session.add(shop)
        session.commit()


def get_shop(shop_name: str):
    with Session(engine) as session:
        shop = session.query(Shop).filter_by(name=shop_name).first()
        return shop


def remove_shop(shop_id: int):
    with Session(engine) as session:
        shop = session.query(Shop).filter_by(id=shop_id).first()
        session.delete(shop)
        session.commit()


def save_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()


def remove_product(product_id: int):
    with Session(engine) as session:
        product = session.query(Product).filter_by(product_id=product_id).first()
        session.delete(product)
        session.commit()


def get_product(product_id: int):
    with Session(engine) as session:
        product = session.query(Product).filter_by(product_id=product_id).first()
        return product


def save_policy(policy: Condition):
    with Session(engine) as session:
        session.add(policy)
        session.commit()


def get_policy(policy_id: int):
    with Session(engine) as session:
        policy = session.query(Condition).filter_by(policy_id=policy_id).first()
        return policy


def remove_policy(policy_id: int):
    with Session(engine) as session:
        policy = session.query(Condition).filter_by(policy_id=policy_id).first()
        session.delete(policy)
        session.commit()


def save_discount():
    # TODO: implement
    pass


def get_discount():
    # TODO: implement
    pass


def remove_discount():
    # TODO: implement
    pass
