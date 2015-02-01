
class Rideshare:
    def __init__(self, ride_sharer, number_seats):
        """
            ride_sharer is a Person offering a ride
        """
        self.ride_sharer = ride_sharer
        self.number_seats = number_seats

        self._seats_taken = set()

    def reserve_seat(self, reserver):
        seats_available = len(self._seats_taken) < self.number_seats
        if seats_available:
            self._seats_taken.add(reserver)
        return seats_available

    def seats_available(self):
        return self.number_seats - len(self._seats_taken)
