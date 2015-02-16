
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/db')
db = client.get_default_database()

people = [x for x in db.people.find()]
events = [x for x in db.events.find()]
reservations = [x for x in db.reservations.find()]
