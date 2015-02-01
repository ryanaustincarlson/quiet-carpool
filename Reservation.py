
class Reservation:
    def __init__(self, event):
        self.event = event
        self.rideshares = set()

    def get_open_rideshares(self, seats_needed):
        return set([rideshare for rideshare in self.rideshares if
                    rideshare.seats_available() >= seats_needed])

    def make_reservation(self, rideshare, reserver):
        rideshare.reserve_seat(reserver)

    def people(self):  # TODO: test that this works..
        people = set()
        for rideshare in self.rideshares:
            people.add(rideshare.ride_sharer)
            for rider in rideshare.riders:
                people.add(rider)
        return people
