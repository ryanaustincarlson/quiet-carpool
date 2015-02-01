
import random


class Reservation:
    def __init__(self, event):
        self.event = event
        self.rideshares = {}
        self.rideshare_requests = {}

    def get_open_rideshares(self, seats_needed):
        return set([rideshare for rideshare in self.rideshares.values() if
                    rideshare.seats_available() >= seats_needed])

    def make_reservation(self, rideshare, reserver):
        rideshare.reserve_seat(reserver)

    def register_rideshare(self, rideshare):
        rideshare_id = Reservation.generate_uuid()
        self.rideshares[rideshare_id] = rideshare
        return rideshare_id

    def register_rideshare_request(self, rideshare_request):
        request_id = Reservation.generate_uuid()
        self.rideshare_requests[request_id] = rideshare_request
        return request_id

    def people(self):  # TODO: test that this works..
        people = set()
        for rideshare in self.rideshares:
            people.add(rideshare.ride_sharer)
            for rider in rideshare.riders:
                people.add(rider)
        return people

    @staticmethod
    def generate_uuid():
        return str(random.randint(10, 10000))
