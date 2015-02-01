
class ReservationManager:
    def __init__(self):
        self.people = set()
        self.rideshares = set()

    def get_open_rideshares(self, seats_needed):
        return set([rideshare for rideshare in self.rideshares if
                    rideshare.seats_available() >= seats_needed])

    def make_reservation(self, rideshare, reserver):
        rideshare.reserve_seat(reserver)
