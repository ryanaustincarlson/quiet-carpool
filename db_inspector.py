
import sys
import pymongo
from pprint import pprint

client = pymongo.MongoClient('mongodb://localhost:27017/db')
db = client.get_default_database()

collections = ['people',
               'events',
               'reservations',
               'rideshares',
               'requests']


def find_stuff(stuff):
    found = [x for x in db[stuff].find()]
    print(">> {}".format(stuff))
    pprint(found)
    print()
    return found

for collection in collections:
    find_stuff(collection)

    if len(sys.argv) == 2:
        if sys.argv[1] == 'remove':
            db[collection].remove()

# db.rideshares.remove()

# people = [x for x in db.people.find()]
# events = [x for x in db.events.find()]
# reservations = [x for x in db.reservations.find()]
# rideshares = [x for x in db.rideshares.find()]
# requests = [x for x in db.requests.find()]

print([x for x in db.people.find({'email': 'ryan.austin.carlson@gmail.com'})])
