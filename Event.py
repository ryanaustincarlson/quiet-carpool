
from Person import Person


class Event:
    def __init__(self, name=None, organizer=None, _id=None, db=None):
        self.name = name
        self.organizer = organizer
        self.starttime = None
        self.endtime = None
        self.location = None

        self.db = db
        self._id = _id
        if self.db:
            if self._id:
                self._init_with_query({'_id': self._id})
            else:
                db_event = {'name': self.name,
                            'organizer_id': self.organizer._id
                            }
                success = self._init_with_query(db_event)
                if not success:
                    self._id = self.db.events.insert(db_event)

    def _init_with_query(self, query):
        result = self.db.events.find_one(query)
        if result:
            self._id = result['_id']
            self.name = result['name']
            self.organizer = Person(_id=result['organizer_id'], db=self.db)
        return result is not None

    def __eq__(self, other):
        return self.name == other.name and \
            self.organizer == other.organizer

    def __ne__(self, other):
        return self.name != other.name or \
            self.organizer != other.organizer
