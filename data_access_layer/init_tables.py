from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DATE, FLOAT
from sqlalchemy.orm import registry, relationship, backref, polymorphic_union

from domain.commerce_system.appointment import ShopManager, ShopOwner
from domain.commerce_system.category import Category
from domain.commerce_system.purchase_conditions import Condition, MaxQuantityForProductCondition, \
    DateWindowForProductCondition, DateWindowForCategoryCondition, TimeWindowForProductCondition, \
    TimeWindowForCategoryCondition
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
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

transaction = Table(
    'transaction',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, ForeignKey('subscribed.username')),
    Column('shop_id', Integer),
    Column('date', DATE),
    Column('price', FLOAT),
)

shop = Table(
    'shop',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('image_url', String),
)

categories_product_mtm = Table(
    'product_categories_mtm',
    mapper_registry.metadata,
    Column('product_category_id', Integer, primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id', ondelete='CASCADE')),
    Column('product_id', Integer, ForeignKey("product.product_id", ondelete='CASCADE')),
)

product = Table(
    'product',
    mapper_registry.metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('price', Integer),
    Column('description', String),
    Column('quantity', Integer),
    Column('shop_id', Integer, ForeignKey('shop.id', ondelete='CASCADE')),
    # Column('shop_id', Integer, ForeignKey('categories.category_id', ondelete='CASCADE')),
    # relationship('categories', secondary=categories_product_mtm)
)

categories = Table(
    'categories',
    mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True),
    Column('name', String),
)

shop_manager_appointments = Table(
    'shop_manager_appointments',
    mapper_registry.metadata,
    Column('appointee', String, ForeignKey("subscribed.username", ondelete='CASCADE'), primary_key=True),
    Column('shop_id', Integer, ForeignKey("shop.id")),
    Column('appointer', String, ForeignKey("subscribed.username", ondelete='CASCADE')),
    Column('delete_product', Integer),
    Column('edit_product', Integer),
    Column('add_product', Integer),
    Column('discount', Integer),
    Column('purchase_condition', Integer),
    Column('get_trans_history', Integer),
    Column('get_staff_permission', Integer),
)

shop_owner_appointments = Table(
    'shop_owner_appointments',
    mapper_registry.metadata,
    Column('appointee', String, ForeignKey("subscribed.username", ondelete='CASCADE'), primary_key=True),
    Column('shop_id', Integer, ForeignKey("shop.id", ondelete='CASCADE')),
    Column('appointer', String, ForeignKey("subscribed.username", ondelete='CASCADE')),
)
# shopping_cart = Table(
#     'shopping_cart',
#     mapper_registry.metadata,
#     Column('cart_id', Integer, primary_key=True),
# )
shopping_bag = Table(
    'shopping_bag',
    mapper_registry.metadata,
    Column('shop_id', Integer, ForeignKey("shop.id", ondelete='CASCADE'), primary_key=True),
    Column('username', String, ForeignKey("subscribed.username", ondelete="CASCADE"), primary_key=True),
    Column('product_id', Integer, ForeignKey("product.product_id", ondelete='CASCADE'))
)

# complex_policies = Table(
#     'complex_policies',
#     mapper_registry.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('parent_policy', Integer, ForeignKey('purchase_policies.policy_id', ondelete='CASCADE')),
#     Column('child_policy', Integer, ForeignKey('purchase_policies.policy_id', ondelete='CASCADE')),
# )

purchase_policies = Table(
    'purchase_policies',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shop.id', ondelete='CASCADE')),
    Column('condition_type', String),
    Column('category', String, ForeignKey('categories.name', ondelete='CASCADE')),
    Column('min_time', String),
    Column('max_time', String),
    Column('min_date', String),
    Column('max_date', String),
    Column('product_id', Integer, ForeignKey('product.product_id', ondelete='CASCADE')),
    Column('max_quantity', Integer),
    Column('parent_policy', Integer, ForeignKey('purchase_policies.id', ondelete='CASCADE'))
)

mapper_registry.map_imperatively(Subscribed, subscribed, properties={
    "shoppingBag": relationship(ShoppingBag, backref='subscribed', cascade='all, delete, delete-orphan'),
    "transactions": relationship(Transaction, backref='subscribed', cascade='all, delete, delete-orphan')
})
mapper_registry.map_imperatively(Shop, shop, properties={
    "product": relationship(Product, backref='shop', cascade='all, delete, delete-orphan'),
    "shopping_bag": relationship(ShoppingBag, backref='shop', cascade='all, delete, delete-orphan')
})
mapper_registry.map_imperatively(Product, product, properties={
    "categories": relationship(Category, backref='product', secondary=categories_product_mtm),
    "max_policies": relationship(MaxQuantityForProductCondition, back_populates='max_policy_product',
                                 cascade='all, delete, delete-orphan'),
    "p_time_policies": relationship(TimeWindowForProductCondition, back_populates='time_policy_product',
                                    cascade='all, delete, delete-orphan'),
    "p_date_policies": relationship(DateWindowForProductCondition, back_populates='date_policy_product',
                                    cascade='all, delete, delete-orphan')
})
mapper_registry.map_imperatively(Transaction, transaction)
mapper_registry.map_imperatively(Category, categories, properties={
    "c_time_policies": relationship(TimeWindowForCategoryCondition, back_populates='time_policy_category',
                                    cascade='all, delete, delete-orphan'),
    "c_date_policies": relationship(DateWindowForCategoryCondition, back_populates='date_policy_category',
                                    cascade='all, delete, delete-orphan')
})
mapper_registry.map_imperatively(ShopManager, shop_manager_appointments)
mapper_registry.map_imperatively(ShopOwner, shop_owner_appointments)
# mapper_registry.map_imperatively(ShoppingCart, shopping_cart, properties={
#     "shoppingBags": relationship(ShoppingBag, backref='shopping_cart'),
#     "subscribed": relationship(Subscribed, backref='shopping_cart')
# })
mapper_registry.map_imperatively(ShoppingBag, shopping_bag)

mapper_registry.map_imperatively(
    Condition,
    purchase_policies,
    properties={
        "complex_children": relationship(
            Condition,
            backref=backref(
                'purchase_policies',
                remote_side=[purchase_policies.c.id],
            )
        ),
    },
    # polymorphic_on=purchase_policies.c.type,
    # polymorphic_identity='condition',

)

mapper_registry.map_imperatively(
    MaxQuantityForProductCondition,
    purchase_policies,
    # polymorphic_identity='max_quantity_for_product_condition',
    properties={
        "max_policy_product": relationship(
            Product,
            back_populates='max_policies',
            cascade='all, delete'
        )
    }
)

mapper_registry.map_imperatively(
    TimeWindowForCategoryCondition,
    purchase_policies,
    # polymorphic_identity='max_quantity_for_product_condition',
    properties={
        "time_policy_category": relationship(
            Category,
            back_populates='c_time_policies',
            cascade='all, delete'
        )
    }
)

mapper_registry.map_imperatively(
    TimeWindowForProductCondition,
    purchase_policies,
    # polymorphic_identity='max_quantity_for_product_condition',
    properties={
        "time_policy_product": relationship(
            Product,
            back_populates='p_time_policies',
            cascade='all, delete'
        )
    }
)

mapper_registry.map_imperatively(
    DateWindowForCategoryCondition,
    purchase_policies,
    # polymorphic_identity='max_quantity_for_product_condition',
    properties={
        "date_policy_category": relationship(
            Category,
            back_populates='c_date_policies',
            cascade='all, delete'
        )
    }
)

mapper_registry.map_imperatively(
    DateWindowForProductCondition,
    purchase_policies,
    # polymorphic_identity='max_quantity_for_product_condition',
    properties={
        "date_policy_product": relationship(
            Product,
            back_populates='p_date_policies',
            cascade='all, delete'
        )
    }
)

mapper_registry.metadata.create_all(engine)
