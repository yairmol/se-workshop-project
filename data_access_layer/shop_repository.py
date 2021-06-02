from typing import TypeVar

from sqlalchemy import delete

from domain.commerce_system.category import Category
from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import Condition
from domain.commerce_system.shop import Shop
from domain.discount_module.discount_calculator import Discount
from init_tables import engine
from sqlalchemy.orm import Session

T = TypeVar('T')
TYPE = TypeVar('TYPE')
FIELD = TypeVar('FIELD')


def save_x(x: T):
    with Session(engine) as session:
        session.add(x)
        session.commit()


def get_x(x_id: T, type: TYPE, field: FIELD):
    with Session(engine) as session:
        x = session.query(TYPE).filter_by(FIELD=x_id).first()
        return x


def remove_x(x_id: T, type: TYPE, field: FIELD):
    with Session(engine) as session:
        x = session.query(TYPE).filter_by(FIELD=x_id).first()
        session.delete(x)
        session.commit()


def save_shop(shop: Shop):
    save_x(shop)
    # with Session(engine) as session:
    #     session.add(shop)
    #     session.commit()


def get_shop(shop_name: str):
    # get_x(shop_name, Shop, name)
    with Session(engine) as session:
        shop = session.query(Shop).filter_by(name=shop_name).first()
        return shop


def remove_shop(shop_id: int):
    # remove_x(shop_id, Shop, id)
    with Session(engine) as session:
        shop = session.query(Shop).filter_by(id=shop_id).first()
        session.delete(shop)
        session.commit()


def save_product(product: Product):
    save_x(product)
    # with Session(engine) as session:
    #     session.add(product)
    #     session.commit()


def remove_product(product_id: int):
    # remove_x(product_id, Product, product_id)
    with Session(engine) as session:
        product = session.query(Product).filter_by(product_id=product_id).first()
        session.delete(product)
        session.commit()


def get_product(product_id: int):
    # get_x(product_id, Product, product_id)
    with Session(engine) as session:
        product = session.query(Product).filter_by(product_id=product_id).first()
        return product


def save_policy(policy: Condition):
    save_x(policy)
    # with Session(engine) as session:
    #     session.add(policy)
    #     session.commit()


def get_policy(policy_id: int):
    # get_x(policy_id, Condition, policy_id)
    with Session(engine) as session:
        policy = session.query(Condition).filter_by(id=policy_id).first()
        return policy


def remove_policy(policy_id: int):
    # remove_x(policy_id, Condition, policy_id)
    with Session(engine) as session:
        policy = session.query(Condition).filter_by(id=policy_id).first()
        session.delete(policy)
        session.commit()


def save_discount(discount: Discount):
    save_x(discount)
    # with Session(engine) as session:
    #     session.add(discount)
    #     session.commit()


def get_discount(discount_id: int):
    # get_x(discount_id, Discount, discount_id)
    with Session(engine) as session:
        discount = session.query(Discount).filter_by(discount_id=discount_id).first()
        return discount


def remove_discount(discount_id: int):
    # get_x(discount_id, Discount, discount_id)
    with Session(engine) as session:
        discount = session.query(Discount).filter_by(discount_id=discount_id).first()
        session.delete(discount)
        session.commit()


def save_category(category: Category):
    save_x(category)


def get_category(category_id: str):
    with Session(engine) as session:
        category = session.query(Category).filter_by(category=category_id).first()
        return category


def remove_category(category_id: str):
    with Session(engine) as session:
        category = session.query(Category).filter_by(category=category_id).first()
        session.delete(category)
        session.commit()
