
class Person:
    def __init__(self, name=None, email=None, _id=None, db=None):
        self.name = name
        self.email = email

        self.location = None

        self.db = db
        self._id = _id
        if self.db:
            if self._id:
                self._init_with_query({'_id': _id})
            else:
                db_person = {'name': self.name,
                             'email': self.email
                             }
                success = self._init_with_query(db_person)
                if not success:
                    self._id = self.db.people.insert(db_person)

    def _init_with_query(self, query):
        result = self.db.people.find_one(query)
        if result:
            self._id = result['_id']
            self.name = result['name']
            self.email = result['email']
        return result is not None

    def __eq__(self, other):
        return self.email == other.email

    def __ne__(self, other):
        return self.email != other.email

    def __hash__(self):
        return self.email.__hash__()
