import os

from sqlalchemy import create_engine

path = '/'.join(__file__.split('\\')[:-1])

engine = create_engine('sqlite:///{}/ahla_super.db'.format(path), echo=True)
