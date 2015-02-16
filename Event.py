
from Person import Person


class Event:
    def __init__(self, name=None, organizer=None, _id=None, db=None):
        self.name = name
        self.organizer = organizer
        self.starttime = None
        self.endtime = None
        self.location = None

        self._id = None
        if _id and db:
            self._id = _id

            db_event = db.events.find({'_id': self._id})[0]
            self.name = db_event['name']
            self.organizer = Person(_id=db_event['organizer_id'], db=db)
        elif db:
            self._id = db.events.insert(
                {'name': self.name,
                 'organizer_id': self.organizer._id
                 })

    def __eq__(self, other):
        return self.name == other.name and \
            self.organizer == other.organizer

    def __ne__(self, other):
        return self.name != other.name or \
            self.organizer != other.organizer
