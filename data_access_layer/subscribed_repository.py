from domain.commerce_system.appointment import Appointment
from domain.commerce_system.user import Subscribed
from init_tables import engine
from sqlalchemy.orm import Session


def save_subscribed(sub: Subscribed):
    with Session(engine) as session:
        session.add(sub)
        session.commit()


def save_password(password):
    pass


def save_appointment(appointment: Appointment):
    pass

