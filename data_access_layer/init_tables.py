from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry

from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.product import Product

engine = create_engine('sqlite:///ahla_super.db', echo=True)
meta = MetaData()
mapper_registry = registry()

subscribed = Table(
    'subscribed',
    mapper_registry.metadata,
    Column('username', String, primary_key=True),
)

# TODO: save the transaction's products
transaction = Table(
    'transaction',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('shop_id', Integer),
    # Column('date', ), TODO: how to save date?
    # Column('price', ), TODO: how to save double/ float
)

shop = Table(
    'shop',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
)

product = Table(
    'products',
    mapper_registry.metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('price', Integer),
    Column('description', String),
    Column('quantity', Integer),
    Column('shop_id', Integer),
)
categories = Table(
    'categories',
    mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True),
    Column('category', String),
)

categories_product_mtm = Table(
    'product_categories_mtm',
    mapper_registry.metadata,
    Column('product_category_id', Integer, ForeignKey('categories.category_id', ondelete='CASCADE'), primary_key=True),
    Column('product_id', Integer, ForeignKey("products.product_id")),
)

# appointments = Table(
#     'appointments',
#     mapper_registry.metadata,
#     Column(ForeignKey("subscribed.username"), primary_key=True),
#     Column(ForeignKey("shop.id")),
#     Column(ForeignKey("subscribed.username")),
# )

mapper_registry.map_imperatively(Subscribed, subscribed)
mapper_registry.map_imperatively(Shop, shop)
mapper_registry.map_imperatively(Product, product)
mapper_registry.map_imperatively(Transaction, transaction)

mapper_registry.metadata.create_all(engine)
