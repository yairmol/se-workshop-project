from typing import TypeVar

from sqlalchemy import delete

from domain.commerce_system.category import Category
from domain.commerce_system.product import Product
from domain.commerce_system.purchase_conditions import Policy
from domain.commerce_system.shop import Shop
from domain.discount_module.discount_calculator import Discount
# from init_tables import engine
from sqlalchemy.orm import Session

from sqlalchemy import delete

from domain.commerce_system.shop import Shop
from data_access_layer.init_tables import engine
from sqlalchemy.orm import Session

from functools import wraps

from sqlalchemy import create_engine, MetaData, delete
from sqlalchemy.orm import Session, registry

T = TypeVar('T')
TYPE = TypeVar('TYPE')
FIELD = TypeVar('FIELD')

# path = '/'.join(_file_.split('\\')[:-1])
#
# engine = create_engine('sqlite:///{}/ahla_super.db'.format(path), echo=True)

meta = MetaData()
mapper_registry = registry()


# def add_to_session(func, objects_to_add=None, self=None):
#     if not objects_to_add:
#         objects_to_add = []
#
#     def inner(*args, **kwargs):
#         with Session(engine) as session:
#             if self:
#                 session.add(self)
#             for obj in objects_to_add:
#                 session.add(obj)
#             func(*args, **kwargs)
#     return inner

# def add_to_session(self=None):
#     def inner(func):
#         with Session(engine) as session:
#             if self:
#                 session.add(self)
#             return func
#     return inner
def add_to_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            session.add(args[0])
            func(*args, **kwargs)

    return wrapper


def add_shop_to_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.of_subscribed:
            with Session(engine) as session:
                session.add(self)
                func(*args, **kwargs)
        else:
            func(*args, **kwargs)

    return wrapper


def get_first(obj_type, **kwargs):
    with Session(engine) as session:
        obj = session.query(obj_type).filter_by(**kwargs).first()
        return obj


def save(obj):
    with Session(engine) as session:
        session.add(obj)
        session.commit()


def delete(obj_type, **kwargs):
    with Session(engine) as session:
        obj = session.query(obj_type).filter_by(**kwargs).first()
        session.delete(obj)
        session.commit()


def delete_all(obj_type):
    with Session(engine) as session:
        session.query(obj_type).delete()
        session.commit()


def get_all(obj_type):
    with Session(engine) as session:
        obj = session.query(obj_type).all()
        return obj


def get_all_of_field(obj_type, func):
    with Session(engine) as session:
        return map(func, session.query(obj_type).all())


def delete_all_rows_from_tables():
    with Session(engine) as session:
        for table in mapper_registry.metadata.tables:
            session.query(mapper_registry.metadata.tables[table]).delete()
            session.commit()


def drop_all_tables():
    for name in mapper_registry.metadata.tables:
        mapper_registry.metadata.tables[name].drop(engine, checkfirst=True)

# def save_x(x: T):
#     with Session(engine) as session:
#         session.add(x)
#         session.commit()
#
#
# def get_x(x_id: T, type: TYPE, field: FIELD):
#     with Session(engine) as session:
#         x = session.query(TYPE).filter_by(FIELD=x_id).first()
#         return x
#
#
# def remove_x(x: T):
#     with Session(engine) as session:
#         session.delete(x)
#         session.commit()
#
#
# def remove_x_by_id(x_id: T, type: TYPE, field: FIELD):
#     with Session(engine) as session:
#         x = session.query(TYPE).filter_by(FIELD=x_id).first()
#         session.delete(x)
#         session.commit()
#
#
# def save_shop(shop: Shop):
#     save_x(shop)
#     # with Session(engine) as session:
#     #     session.add(shop)
#     #     session.commit()
#
#
# def save_shop(shop: Shop):
#     with Session(engine) as session:
#         session.add(shop)
#         session.commit()
#
#
# def get_shop(shop_name: str, shop_type):
#     with Session(engine) as session:
#         shop = session.query(shop_type).filter_by(name=shop_name).first()
#         return shop
#
#
# def remove_shop(shop_id: int, shop_type):
#     with Session(engine) as session:
#         shop = session.query(shop_type).filter_by(id=shop_id).first()
#         session.delete(shop)
#         session.commit()
#
#
# def get_product(prod_name: str, product_type):
#     with Session(engine) as session:
#         shop = session.query(product_type).filter_by(product_name=prod_name).first()
#         return shop
#
#
# def save_product(product: Product):
#     save_x(product)
#     # with Session(engine) as session:
#     #     session.add(product)
#     #     session.commit()
#
#
# def remove_product(product_id: int):
#     # remove_x(product_id, Product, product_id)
#     with Session(engine) as session:
#         product = session.query(Product).filter_by(product_id=product_id).first()
#         session.delete(product)
#         session.commit()
#
#
# def get_product(product_id: int):
#     # get_x(product_id, Product, product_id)
#     with Session(engine) as session:
#         product = session.query(Product).filter_by(product_id=product_id).first()
#         return product
#
#
# def save_policy(policy: Policy):
#     save_x(policy)
#
#
# def get_policy(policy_id: int):
#     # get_x(policy_id, Condition, policy_id)
#     with Session(engine) as session:
#         policy = session.query(Policy).filter_by(id=policy_id).first()
#         return policy
#
#
# def remove_policy(policy_id: int):
#     # remove_x(policy_id, Condition, policy_id)
#     with Session(engine) as session:
#         policy = session.query(Policy).filter_by(id=policy_id).first()
#         session.delete(policy)
#         session.commit()
#
#
# def save_discount(discount: Discount):
#     save_x(discount)
#     # with Session(engine) as session:
#     #     session.add(discount)
#     #     session.commit()
#
#
# def get_discount(discount_id: int):
#     # get_x(discount_id, Discount, discount_id)
#     with Session(engine) as session:
#         discount = session.query(Discount).filter_by(discount_id=discount_id).first()
#         return discount
#
#
# def remove_discount(discount_id: int):
#     # get_x(discount_id, Discount, discount_id)
#     with Session(engine) as session:
#         discount = session.query(Discount).filter_by(discount_id=discount_id).first()
#         session.delete(discount)
#         session.commit()
#
#
# def save_category(category: Category):
#     save_x(category)
#
#
# def get_category(category_id: str):
#     with Session(engine) as session:
#         category = session.query(Category).filter_by(category=category_id).first()
#         return category
#
#
# def remove_category(category_id: str):
#     with Session(engine) as session:
#         category = session.query(Category).filter_by(category=category_id).first()
#         session.delete(category)
#         session.commit()
