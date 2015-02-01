
class Rideshare:
    def __init__(self, ride_sharer, number_seats):
        """
            ride_sharer is a Person offering a ride
        """
        self.ride_sharer = ride_sharer
        self.number_seats = number_seats

        self.riders = set()

    def reserve_seat(self, rider):
        seats_available = len(self.riders) < self.number_seats
        if seats_available:
            self.riders.add(rider)
        return seats_available

    def seats_available(self):
        return self.number_seats - len(self.riders)
