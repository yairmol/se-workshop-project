from domain.commerce_system.shop import Shop
from init_tables import engine
from sqlalchemy.orm import Session


def save_shop(shop: Shop):
    with Session(engine) as session:
        session.add(shop)
        session.commit()


def save_product():
    pass


def save_discount():
    pass


def save_policy():
    pass
