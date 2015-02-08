
class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

        self.location = None

    def __eq__(self, other):
        return self.email == other.email

    def __ne__(self, other):
        return self.email != other.email

    def __hash__(self):
        return self.email.__hash__()
