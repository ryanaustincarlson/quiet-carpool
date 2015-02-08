
class RideshareRequest:
    def __init__(self, requester, number_seats):
        self.requester = requester
        self.number_seats = number_seats

        self.acceptable_rideshares = set()

    def add_acceptable_rideshare(self, rideshare):
        self.acceptable_rideshares.add(rideshare)
