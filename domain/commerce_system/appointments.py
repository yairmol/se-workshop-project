from domain.commerce_system.shop import Shop


class Appointment:
    def __init__(self, shop: Shop, state):
        self.shop = shop
        self.state = state
