
from Rideshare import Rideshare
from RideshareRequest import RideshareRequest


class EventManager:
    def __init__(self, event, db):
        self.event = event
        self.db = db

    def get_open_rideshares(self, seats_needed):
        all_rideshares = self.get_rideshares()

        open_rideshares = set()
        for rideshare in all_rideshares:
            if rideshare.seats_available() >= seats_needed:
                open_rideshares.add(rideshare)
        return open_rideshares

    def get_rideshare_request_matches(self, rideshare):
        all_rideshare_requests = self.get_rideshare_requests()

        matches = set()
        for rideshare_request in all_rideshare_requests:

            if rideshare_request.requester in rideshare.riders:
                continue

            if rideshare in rideshare_request.acceptable_rideshares:
                matches.add(rideshare_request)

        return matches

    def make_reservation(self, rideshare, reserver):
        rideshare.reserve_seat(reserver)

    def get_rideshares(self):
        db_query = {'event_id': self.event._id}
        rideshares = [Rideshare(_id=r['_id'], db=self.db)
                      for r in self.db.rideshares.find(db_query)]
        return rideshares

    def get_rideshare_requests(self):
        db_query = {'event_id': self.event._id}
        rideshares = [RideshareRequest(_id=r['_id'], db=self.db)
                      for r in self.db.requests.find(db_query)]
        return rideshares

    # def people(self):  # TODO: test that this works..
    #     people = set()
    #     for rideshare in self.rideshares:
    #         people.add(rideshare.ride_sharer)
    #         for rider in rideshare.riders:
    #             people.add(rider)
    #     return people
