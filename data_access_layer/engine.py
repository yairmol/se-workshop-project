from functools import wraps

from sqlalchemy import create_engine, MetaData, delete
from sqlalchemy.orm import Session, registry

path = '/'.join(__file__.split('\\')[:-1])

engine = create_engine('sqlite:///{}/ahla_super.db'.format(path), echo=True)

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
           # mapper_registry.metadata.tables[table].delete()
            session.query(mapper_registry.metadata.tables[table]).delete()
            session.commit()

def drop_all_tables():
    for name in mapper_registry.metadata.tables:
        mapper_registry.metadata.tables[name].drop(engine, checkfirst=True)