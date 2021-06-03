from sqlalchemy import create_engine

engine = create_engine('sqlite:///ahla_super.db', echo=True)
