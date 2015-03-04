
from Person import Person
from Rideshare import Rideshare


class RideshareRequest:
    def __init__(self, requester=None, number_seats=None, _id=None, db=None):
        self.requester = requester
        self.number_seats = number_seats

        self.acceptable_rideshares = set()

        self.db = db
        self._id = _id

        if self.db:
            if self._id:
                self._init_with_query({'_id': self._id})
            else:
                db_request = {'requester_id': self.requester._id,
                              'number_seats': self.number_seats
                              }
                success = self._init_with_query(db_request)
                if not success:
                    db_request['rideshare_ids'] = []
                    self._id = self.db.requests.insert(db_request)

    def _init_with_query(self, query):
        result = self.db.requests.find_one(query)
        if result:
            self._id = result['_id']
            self.requester = Person(_id=result['requester_id'], db=self.db)
            self.number_seats = result['number_seats']
            self.acceptable_rideshares = {Rideshare(_id=rid, db=self.db) for rid in result['rideshare_ids']}
        return result is not None

    def add_acceptable_rideshare(self, rideshare):
        self.acceptable_rideshares.add(rideshare)

    def __eq__(self, other):
        return self.requester == other.requester and \
            self.number_seats == other.number_seats

    def __ne__(self, other):
        return self.requester != other.requester or \
            self.number_seats != other.number_seats

    def __hash__(self):
        hashable = '{}~{}'.format(self.requester.__hash__(), self.number_seats)
        return hashable.__hash__()
