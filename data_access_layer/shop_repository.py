from sqlalchemy import delete

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


def save_product():
    pass


def save_discount():
    pass


def save_policy():
    pass
