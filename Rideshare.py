
from Person import Person
from Event import Event


class Rideshare:
    def __init__(self, ride_sharer=None, number_seats=None, event=None, _id=None, db=None):
        """
            ride_sharer is a Person offering a ride
        """
        self.ride_sharer = ride_sharer
        self.number_seats = number_seats
        self.event = event

        self.riders = set()

        self.db = db
        self._id = _id

        if self.db:
            if self._id:
                self._init_with_query({'_id': self._id})
            else:
                db_rideshare = {'ride_sharer_id': self.ride_sharer._id,
                                'number_seats': self.number_seats,
                                'event_id': self.event._id
                                }
                success = self._init_with_query(db_rideshare)
                if not success:
                    db_rideshare['rider_ids'] = []
                    self._id = self.db.rideshares.insert(db_rideshare)

    def _init_with_query(self, query):
        result = self.db.rideshares.find_one(query)
        if result:
            self._id = result['_id']
            self.ride_sharer = Person(_id=result['ride_sharer_id'], db=self.db)
            self.number_seats = result['number_seats']
            self.event = Event(_id=result['event_id'], db=self.db)
            self.riders = {Person(_id=pid, db=self.db) for pid in result['rider_ids']}
        return result is not None

    def reserve_seat(self, rider):
        seats_available = len(self.riders) < self.number_seats
        if seats_available:
            before_len = len(self.riders)
            self.riders.add(rider)

            if len(self.riders) > before_len:
                self.db.rideshares.update({'_id': self._id},
                                          {'$set': {'rider_ids': [r._id for r in self.riders]}})

        return seats_available

    def seats_available(self):
        return self.number_seats - len(self.riders)

    def __eq__(self, other):
        return self.ride_sharer == other.ride_sharer and \
            self.number_seats == other.number_seats

    def __ne__(self, other):
        return self.ride_sharer != other.ride_sharer or \
            self.number_seats != other.number_seats

    def __hash__(self):
        hashable = '{}~{}'.format(self.ride_sharer.__hash__(), self.number_seats)
        return hashable.__hash__()
