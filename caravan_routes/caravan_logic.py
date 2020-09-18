from datetime import datetime


class CaravanState():
    def __init__(self, state: str, lattitude, longitude, created=None):
        self.state = state
        self.lattitude = lattitude
        self.longitude = longitude
        self.created = created or datetime.now()


def build_quest():