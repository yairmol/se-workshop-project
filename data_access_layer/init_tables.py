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

shops = Table(
    'shops',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('image_url', String),
)

products = Table(
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

purchase_policies = Table(
    'purchase_policies',
    mapper_registry.metadata,
    Column('policy_id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shops.id', ondelete='CASCADE')),
    Column('condition_type', String),
    Column('max_quantity', Integer),
    Column('product', Integer, ForeignKey('products.product_id', ondelete='CASCADE')),
    # Column('category', String), TODO: check if category is string or integer
    Column('min_time', String),
    Column('max_time', String),
    Column('min_date', String),
    Column('max_date', String),
    Column('conditions', list),

)

discounts = Table(
    'discounts',
    mapper_registry.metadata,
    Column('discount_id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shops.id', ondelete='CASCADE')),
    # Column('Condition', ) TODO
)

# appointments = Table(
#     'appointments',
#     mapper_registry.metadata,
#     Column(ForeignKey("subscribed.username"), primary_key=True),
#     Column(ForeignKey("shop.id")),
#     Column(ForeignKey("subscribed.username")),
# )

mapper_registry.map_imperatively(Subscribed, subscribed)
mapper_registry.map_imperatively(Shop, shops)
mapper_registry.map_imperatively(Product, products)
mapper_registry.map_imperatively(Transaction, transaction)

mapper_registry.metadata.create_all(engine)
