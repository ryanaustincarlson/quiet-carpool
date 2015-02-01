
class Event:
    def __init__(self, name, organizer):
        self.name = name
        self.organizer = organizer
        self.starttime = None
        self.endtime = None
        self.location = None

    def __eq__(self, other):
        return self.name == other.name and \
            self.organizer == other.organizer

    def __ne__(self, other):
        return self.name != other.name or \
            self.organizer != other.organizer
