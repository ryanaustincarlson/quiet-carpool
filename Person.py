
class Person:
    def __init__(self, name=None, email=None, _id=None, db=None):
        self.name = name
        self.email = email

        self.location = None

        self._id = None
        if _id and db:
            self._id = _id
            db_person = db.people.find({'_id': _id})[0]
            self.name = db_person['name']
            self.email = db_person['email']
        elif db:
            self._id = db.people.insert(
                {'name': self.name,
                 'email': self.email
                 })

    def __eq__(self, other):
        return self.email == other.email

    def __ne__(self, other):
        return self.email != other.email

    def __hash__(self):
        return self.email.__hash__()
