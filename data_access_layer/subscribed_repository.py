from domain.commerce_system.appointment import Appointment
# from init_tables import engine

from sqlalchemy.orm import Session
from data_access_layer.engine import engine


def save_subscribed(sub):
    with Session(engine) as session:
        print("adding")
        session.add(sub)
        session.commit()
        print("done")


def get_subscribed(username: str, subscribed_type):
    with Session(engine) as session:
        subscribed = session.query(subscribed_type).filter_by(username=username).first()
        return subscribed


def remove_subscribed(username: str, subscribed_type):
    with Session(engine) as session:
        subscribed = session.query(subscribed_type).filter_by(username=username).first()
        session.delete(subscribed)
        session.commit()

def get_all_subscribed(subscribed_type):
    with Session(engine) as session:
        subscribed = session.query(subscribed_type).all()
        return subscribed

def remove_all_subscribed(subscribed_type):
    with Session(engine) as session:
        # subscribees = session.query(subscribed_type).all()
        # for subscribed in subscribees:
        #     session.delete(subscribed)
        # session.commit()
        session.query(subscribed_type).delete()
        session.commit()
        # session.execute("TRUNCATE TABLE subscribed")
def save_password(password):
    pass


def save_appointment(appointment: Appointment):
    pass

