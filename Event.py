
class Event:
    def __init__(self, name, starttime, endtime):
        self.name = name
        self.starttime = starttime
        self.endtime = endtime
        self.location = None

    def __eq__(self, other):
        return self.name == other.name and \
            self.starttime == other.starttime and \
            self.endtime == other.endtime

    def __ne__(self, other):
        return self.name != other.name or \
            self.starttime != other.starttime or \
            self.endtime != other.endtime
