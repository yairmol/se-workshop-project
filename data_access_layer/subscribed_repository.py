from domain.authentication_module.authenticator import Password
from domain.commerce_system.appointment import Appointment
from domain.commerce_system.user import Subscribed
from init_tables import engine
from sqlalchemy.orm import Session

def save_subscribed(sub: Subscribed):
    with Session(engine) as session:
        session.add(sub)
        session.commit()


def get_subscribed(username: str):
    with Session(engine) as session:
        subscribed = session.query(Subscribed).filter_by(username=username).first()
        return subscribed


def remove_subscribed(username: str):
    with Session(engine) as session:
        subscribed = session.query(Subscribed).filter_by(username=username).first()
        session.delete(subscribed)
        session.commit()


def save_password(password):
    with Session(engine) as session:
        session.add(password)
        session.commit()


def get_password(username: str):
    with Session(engine) as session:
        subscribed = session.query(Password).filter_by(username=username).first()
        return subscribed


def save_appointment(appointment: Appointment):
    pass
