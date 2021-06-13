from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DATE, FLOAT, TIME
from sqlalchemy.orm import registry, relationship, backref, polymorphic_union
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DATE, FLOAT
from sqlalchemy.orm import registry, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.orm.collections import attribute_mapped_collection

# from domain.authentication_module.authenticator import Password
from domain.commerce_system.appointment import ShopManager, ShopOwner
from domain.commerce_system.category import Category
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.commerce_system.appointment import ShopManager, ShopOwner
from domain.commerce_system.category import Category
from domain.commerce_system.purchase_conditions import Policy, MaxQuantityForProductCondition, \
    DateWindowForProductCondition, DateWindowForCategoryCondition, TimeWindowForProductCondition, \
    TimeWindowForCategoryCondition, CompositePurchaseCondition, ANDPolicy, ORPolicy
from domain.commerce_system.shopping_cart import ShoppingCart, ShoppingBag
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.product import Product, ProductInBag
from domain.commerce_system.product import Product
from domain.commerce_system.transaction import Transaction
from domain.commerce_system.user import Subscribed
from domain.commerce_system.shop import Shop
from domain.commerce_system.product import Product, ProductInBag
from data_access_layer.engine import engine
from domain.discount_module.discount_calculator import Discount, Condition, ProductQuantityCondition, \
    CategoryQuantityCondition, SumSimpleCondition, TotalSumCondition, CategorySumCondition, AdditiveDiscount, \
    MaxDiscount, XorDiscount, StoreDiscount, CategoryDiscount, ProductDiscount, ANDCondition, ORCondition, \
    SimpleCondition, QuantitySimpleCondition, ConditionalDiscount, CompositeDiscount

# Engine

meta = MetaData()
mapper_registry = registry()

# Tables

# subscribed = Table(
#     'subscribed',
#     mapper_registry.metadata,
#     Column('username', String, primary_key=True),
# )
#
# passwords = Table(
#     'password',
#     mapper_registry.metadata,
#     Column('username', String, ForeignKey("subscribed.username"), primary_key=True),
#     Column('password_hash', String),
#     Column('salt', String),
# )
#
# transaction = Table(
#     'transaction',
#     mapper_registry.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('username', String, ForeignKey("subscribed.username")),
#     Column('shop_id', Integer, ForeignKey("shop.shop_id")),
#     Column('date', DATE),
#     Column('price', FLOAT),
# )

shop = Table(
    'shop',
    mapper_registry.metadata,
    Column('shop_id', Integer, primary_key=True),
    Column('name', String),
    Column('description', String),
    Column('image_url', String),
)

categories_product_mtm = Table(
    'product_categories_mtm',
    mapper_registry.metadata,
    Column('product_category_id', Integer, primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id', ondelete='CASCADE')),
    Column('product_id', Integer, ForeignKey("products.product_id", ondelete='CASCADE')),
)

product = Table(
    'products',
    mapper_registry.metadata,
    Column('product_id', Integer, primary_key=True),
    Column('product_name', String),
    Column('price', Integer),
    Column('description', String),
    Column('quantity', Integer),
    Column('shop_id', Integer, ForeignKey('shop.shop_id', ondelete='CASCADE')),
)

categories = Table(
    'categories',
    mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True),
    Column('name', String),
)

# shop_manager_appointments = Table(
#     'shop_manager_appointments',
#     mapper_registry.metadata,
#     Column('appointee', String, ForeignKey("subscribed.username", ondelete='CASCADE'), primary_key=True),
#     Column('shop_id', Integer, ForeignKey("shop.id")),
#     Column('appointer', String, ForeignKey("subscribed.username", ondelete='CASCADE')),
#     Column('delete_product', Integer),
#     Column('edit_product', Integer),
#     Column('add_product', Integer),
#     Column('discount', Integer),
#     Column('purchase_condition', Integer),
#     Column('get_trans_history', Integer),
#     Column('get_staff_permission', Integer),
# )
#
# shop_owner_appointments = Table(
#     'shop_owner_appointments',
#     mapper_registry.metadata,
#     Column('appointee', String, ForeignKey("subscribed.username", ondelete='CASCADE'), primary_key=True),
#     Column('shop_id', Integer, ForeignKey("shop.id", ondelete='CASCADE')),
#     Column('appointer', String, ForeignKey("subscribed.username", ondelete='CASCADE')),
# )

shopping_cart = Table(
    'shopping_cart',
    mapper_registry.metadata,
    Column('cart_id', Integer, primary_key=True),
    # Column('username', String, ForeignKey('subscribed.name')),
)

shopping_bag = Table(
    'shopping_bag',
    mapper_registry.metadata,
    Column('bag_id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey("shop.shop_id", ondelete='CASCADE')),
    Column('cart_id', String, ForeignKey("shopping_cart.cart_id", ondelete="CASCADE")),
)

shopping_bag_products = Table(
    'shopping_bag_products',
    mapper_registry.metadata,
    Column('bag_id', Integer, ForeignKey("shopping_bag.bag_id", ondelete='CASCADE'), primary_key=True),
    Column('product_id', Integer, ForeignKey("products.product_id"), nullable=False),
    Column('amount', Integer)
)

purchase_policies = Table(
    'purchase_policies',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shop.shop_id', ondelete='CASCADE')),
    Column('condition_type', String),
    Column('category', String, ForeignKey('categories.name', ondelete='CASCADE')),
    Column('min_time', TIME),
    Column('max_time', TIME),
    Column('min_date', DATE),
    Column('max_date', DATE),
    Column('product_id', Integer, ForeignKey('products.product_id', ondelete='CASCADE')),
    Column('max_quantity', Integer),
    Column('parent_policy', Integer, ForeignKey('purchase_policies.id', ondelete='CASCADE')),
)

discount_condition = Table(
    'discount_condition',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String),
    Column('minimum', Integer),
    Column('conditioned_product_id', Integer),
    Column('conditioned_category', String),
    Column('parent_condition', Integer, ForeignKey('discount_condition.id', ondelete='CASCADE')),
)

discount = Table(
    'discount',
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('shop_id', Integer, ForeignKey('shop.shop_id', ondelete='CASCADE')),
    Column('condition', Integer, ForeignKey('discount_condition.id', ondelete='CASCADE')),
    Column('parent_discount', Integer, ForeignKey('discount.id', ondelete='CASCADE')),
)


# Mappings

mapper_registry.map_imperatively(Condition, discount_condition)
mapper_registry.map_imperatively(SimpleCondition, discount_condition, inherits=Condition)
mapper_registry.map_imperatively(QuantitySimpleCondition, discount_condition, inherits=SimpleCondition)
mapper_registry.map_imperatively(ProductQuantityCondition, discount_condition, inherits=QuantitySimpleCondition)
mapper_registry.map_imperatively(CategoryQuantityCondition, discount_condition, inherits=QuantitySimpleCondition)
mapper_registry.map_imperatively(SumSimpleCondition, discount_condition, inherits=SimpleCondition)
mapper_registry.map_imperatively(TotalSumCondition, discount_condition, inherits=SumSimpleCondition)
mapper_registry.map_imperatively(CategorySumCondition, discount_condition, inherits=SumSimpleCondition)
mapper_registry.map_imperatively(
    ANDCondition,
    discount_condition,
    inherits=Condition,
    properties={
        "conditions": relationship(
            Condition,
            backref=backref('and_conditions', remote_side=[discount_condition.c.id]),
            cascade='all, delete, delete-orphan')
    }
)
mapper_registry.map_imperatively(
    ORCondition,
    discount_condition,
    inherits=Condition,
    properties={
        "conditions": relationship(
            Condition,
            backref=backref('or_conditions', remote_side=[discount_condition.c.id]),
            cascade='all, delete, delete-orphan')
    }
)
mapper_registry.map_imperatively(Discount, discount)
mapper_registry.map_imperatively(ConditionalDiscount, discount, inherits=Discount)
mapper_registry.map_imperatively(ProductDiscount, discount, inherits=ConditionalDiscount)
mapper_registry.map_imperatively(CategoryDiscount, discount, inherits=ConditionalDiscount)
mapper_registry.map_imperatively(StoreDiscount, discount, inherits=ConditionalDiscount)
mapper_registry.map_imperatively(
    CompositeDiscount,
    discount,
    inherits=Discount,
    properties={
        "discounts": relationship(Discount, backref=backref('composite_discounts', remote_side=[discount.c.id]),
                                  cascade='all, delete, delete-orphan')
    }
)
mapper_registry.map_imperatively(XorDiscount, discount, inherits=CompositeDiscount)
mapper_registry.map_imperatively(MaxDiscount, discount, inherits=CompositeDiscount)
mapper_registry.map_imperatively(AdditiveDiscount, discount, inherits=CompositeDiscount)

#
# mapper_registry.map_imperatively(Discount, discount, properties={
#     "condition": relationship(Condition)
# })

# mapper_registry.map_imperatively(Subscribed, subscribed, properties={
#     "shoppingBag": relationship(ShoppingBag, backref='subscribed', cascade='all, delete, delete-orphan'),
#     "transactions": relationship(Transaction, backref='subscribed', cascade='all, delete, delete-orphan')
# })
mapper_registry.map_imperatively(Shop, shop, properties={
    "products": relationship(Product, backref='shop', collection_class=attribute_mapped_collection('product_id')),
    "shopping_bag": relationship(ShoppingBag, backref='shop'),
    # "transactions_history": relationship(Transaction, backref='shop'),
    "conditions": relationship(Policy, backref='shop', cascade='all, delete, delete-orphan'),
    # "discount": relationship(Discount, backref='shop', cascade='delete, delete-orphan')
})
mapper_registry.map_imperatively(Product, product, properties={
    "categories": relationship(Category, backref='product', secondary=categories_product_mtm),
    "policies": relationship(Policy, backref='product', cascade='all, delete, delete-orphan'),
})
# mapper_registry.map_imperatively(Subscribed, subscribed, properties={
#     "transactions": relationship(Transaction, backref='subscribed'),
# })

# mapper_registry.map_imperatively(Password, passwords)
mapper_registry.map_imperatively(Category, categories, properties={
    "policies": relationship(Policy, backref='categories', cascade='all, delete, delete-orphan')

})
# mapper_registry.map_imperatively(ShopManager, shop_manager_appointments)
# mapper_registry.map_imperatively(ShopOwner, shop_owner_appointments)
# mapper_registry.map_imperatively(ShoppingCart, shopping_cart, properties={
#     "shoppingBags": relationship(ShoppingBag, backref='shopping_cart'),
#     "subscribed": relationship(Subscribed, backref='shopping_cart')
# })
mapper_registry.map_imperatively(ShoppingBag, shopping_bag)

mapper_registry.map_imperatively(
    Policy,
    purchase_policies,
    polymorphic_on=purchase_policies.c.condition_type,
)

mapper_registry.map_imperatively(
    MaxQuantityForProductCondition,
    purchase_policies,
    polymorphic_identity='max_quantity_for_product_condition',
    inherits=Policy,
)

mapper_registry.map_imperatively(
    TimeWindowForCategoryCondition,
    purchase_policies,
    polymorphic_identity='time_window_for_category_condition',
    inherits=Policy,
)

mapper_registry.map_imperatively(
    TimeWindowForProductCondition,
    purchase_policies,
    polymorphic_identity='time_window_for_product_condition',
    inherits=Policy,
)

mapper_registry.map_imperatively(
    DateWindowForCategoryCondition,
    purchase_policies,
    polymorphic_identity="date_window_for_category_condition",
    inherits=Policy,
)

mapper_registry.map_imperatively(
    DateWindowForProductCondition,
    purchase_policies,
    polymorphic_identity="date_window_for_product_condition",
    inherits=Policy,

)

mapper_registry.map_imperatively(
    CompositePurchaseCondition,
    purchase_policies,
    polymorphic_identity="compositeCondition",
    inherits=Policy,
    properties={
        "conditions": relationship(Policy, backref=backref('policies', remote_side=[purchase_policies.c.id]),
                                   cascade='all, delete, delete-orphan')
    }
)

mapper_registry.map_imperatively(
    ANDPolicy,
    purchase_policies,
    polymorphic_identity='and_condition',
    inherits=CompositePurchaseCondition,
)

mapper_registry.map_imperatively(
    ORPolicy,
    purchase_policies,
    polymorphic_identity='or_condition',
    inherits=CompositePurchaseCondition,
)

# mapper_registry.map_imperatively(ShopManager, shop_manager_appointments)
# mapper_registry.map_imperatively(ShopOwner, shop_owner_appointments)
mapper_registry.map_imperatively(ShoppingCart, shopping_cart, properties={
    "shopping_bags": relationship(
        ShoppingBag, backref='shopping_cart', collection_class=attribute_mapped_collection('shop')
    ),
    # "subscribed": relationship(Subscribed, backref='shopping_cart')
})

mapper_registry.map_imperatively(ProductInBag, shopping_bag_products, properties={
    "product": relationship(Product)
})

# mapper_registry.map_imperatively(ShoppingBag, shopping_bag, properties={
#     "products": relationship(ProductInBag, backref='shopping_bag_products',
#                              collection_class=attribute_mapped_collection('product')),
#     # "shop": relationship(Shop, backref='shop'),
# })

mapper_registry.metadata.create_all(engine)
