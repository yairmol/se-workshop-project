from sqlalchemy import delete

from data_access_layer.engine import engine

from sqlalchemy.orm import Session


def save_shop(shop):
    with Session(engine) as session:
        session.add(shop)
        session.commit()


def get_shop(shop_name: str, shop_type):
    with Session(engine) as session:
        shop = session.query(shop_type).filter_by(name=shop_name).first()
        return shop


def remove_shop(shop_id: int, shop_type):
    with Session(engine) as session:
        shop = session.query(shop_type).filter_by(id=shop_id).first()
        session.delete(shop)
        session.commit()


def get_product(prod_name: str, product_type):
    with Session(engine) as session:
        shop = session.query(product_type).filter_by(product_name=prod_name).first()
        return shop


def save_product():
    pass


def save_discount():
    pass


def save_policy():
    pass
