from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry

from domain.commerce_system.user import Subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.product import Product

mapper_registry = registry()

subscribed = Table(
    'subscribed',
    mapper_registry.metadata,
    Column('username', String, primary_key=True),
)

transaction = Table(
    'transaction',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('shop_id', Integer),
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
    Column('product_category_id', Integer, primary_key=True),
    Column(ForeignKey("products.product_id")),
    Column(ForeignKey("categories.category_id")),
)
appointments = Table(
    'appointments',
    mapper_registry.metadata,
    Column(ForeignKey("subscribed.username"), primary_key=True),
    Column(ForeignKey("shop.id")),
    Column(ForeignKey("subscribed.username")),
)

mapper_registry.map_imperatively(Subscribed, subscribed)
mapper_registry.map_imperatively(Shop, shop)
mapper_registry.map_imperatively(Product, product)