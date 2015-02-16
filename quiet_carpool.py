
import pdb
import pickle

from flask import Flask, request, redirect, render_template
app = Flask(__name__)

from Person import Person
from Event import Event
from Reservation import Reservation
from RideshareRequest import RideshareRequest
from Rideshare import Rideshare
from ReservationManager import ReservationManager

PICKLE_FNAME = 'reservation-manager.pickle'

try:
    with open(PICKLE_FNAME, 'rb') as f:
        manager = pickle.load(f)
except:
    print("creating a brand new manager")
    manager = ReservationManager()
    reservation = Reservation(Event('partytime', Person('ryan', 'rcarlson@something.com')))
    manager.reservation_map['1'] = reservation

    requester = Person('ambarish', 'ajoshi@something.com')
    ridesharer = Person('susan', 'sberman@something.com')

    rrequest = RideshareRequest(requester, 1)
    rideshare = Rideshare(ridesharer, 3)

    reservation.rideshares['1'] = rideshare
    reservation.rideshare_requests['1'] = rrequest

import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient('mongodb://localhost:27017/db')
db = client.get_default_database()


@app.route('/')
def index():
    return open('create_event.html', 'r').read()


@app.route('/event', methods=['POST'])
@app.route('/event/<event_id>/', methods=['GET'])
def event(event_id=None):
    try:
        print('event_id:', event_id)
        if event_id is None:
            organizer_name = request.form['org_name']
            organizer_email = request.form['org_email']
            organizer = Person(name=organizer_name,
                               email=organizer_email,
                               db=db)

            # create an event
            event_name = request.form['event_name']
            event = Event(name=event_name, organizer=organizer, db=db)

            # location = request.form['location']
            # event.location = location if len(location) > 0 else None

            reservation = Reservation(event=event, db=db)

            # event_id = manager.register_event(event)
            # serialize_manager()

            print('registered event: {}, reservation: {}'.format(event, reservation))

            return redirect('/event/{}'.format(str(event._id)))
        else:
            # reservation = manager.reservation_map[event_id]
            event = Event(_id=ObjectId(event_id), db=db)

            return render_template('event.html',
                                   event_name=event.name,
                                   org_name=event.organizer.name)
    except Exception as e:
        print('>>> error!')
        import traceback
        print(traceback.format_exc())
        print(manager.reservation_map)
        raise e


@app.route('/event/<event_id>/request_ride', methods=['POST'])
@app.route('/event/<event_id>/request_ride/<ride_request_id>/', methods=['GET'])
def need_a_ride(event_id=None, ride_request_id=None):
    try:
        reservation = manager.reservation_map[event_id]
        if ride_request_id is None:
            name = request.form['name']
            email = request.form['email']
            num_seats = int(request.form['num_seats'])

            # create a request
            rideshare_request = RideshareRequest(Person(name, email), num_seats)
            request_id = reservation.register_rideshare_request(rideshare_request)
            serialize_manager()
            return redirect('/event/{}/request_ride/{}'.format(
                event_id, request_id))

        else:
            rideshare_request = reservation.rideshare_requests[ride_request_id]

            match = None
            for rideshare_id in reservation.rideshares:
                rideshare = reservation.rideshares[rideshare_id]
                if rideshare_request.requester in rideshare.riders:
                    match = rideshare.ride_sharer
                    break

            html = ''
            if match is not None:
                html += "You've been matched with {}".format(match.name)

            else:

                open_rideshares = reservation.get_open_rideshares(
                    rideshare_request.number_seats)

                if len(open_rideshares) == 0:
                    html = 'Sorry, there are no available rideshares at this time. '
                    html += 'Check back soon to see when rides become available'
                else:
                    html = 'There {} {} ride{} available'.format(
                        'are' if len(open_rideshares) != 1 else 'is',
                        len(open_rideshares),
                        's' if len(open_rideshares) != 1 else '')
                    html += '<br><br>'
                    html += 'Select any rides you would be happy taking'
                    html += '<form action="requested" method="post">'
                    for rideshare, rideshare_id in open_rideshares:
                        ride_sharer = rideshare.ride_sharer
                        html += '<input type="checkbox" '
                        html += 'name="id" value="{}" '.format(rideshare_id)
                        html += '/>'
                        html += ' {} ({} seat{})'.format(
                            ride_sharer.name, rideshare.seats_available(),
                            's' if rideshare.seats_available() != 1 else '')
                        html += ' <br>'
                    html += '<input type="submit" value="Submit">'
                    html += '</form>'

            return html
    except Exception as e:
        print('>>> error!')
        import traceback
        print(traceback.format_exc())
        print(manager.reservation_map)
        raise e


@app.route('/event/<event_id>/request_ride/<ride_request_id>/requested',
           methods=['POST'])
def rides_requested(event_id=None, ride_request_id=None):
    reservation = manager.reservation_map[event_id]
    rideshare_request = reservation.rideshare_requests[ride_request_id]

    acceptable_rideshare_ids = request.form.getlist('id')
    for rideshare_id in acceptable_rideshare_ids:
        rideshare = reservation.rideshares[rideshare_id]

        rideshare_request.add_acceptable_rideshare(rideshare)

    serialize_manager()

    return "Great! We've logged your preferences"


@app.route('/event/<event_id>/rideshare', methods=['POST'])
@app.route('/event/<event_id>/rideshare/<rideshare_id>/', methods=['GET'])
def have_a_ride(event_id=None, rideshare_id=None):
    try:
        reservation = manager.reservation_map[event_id]
        if rideshare_id is None:
            name = request.form['name']
            email = request.form['email']
            # location = request.form['location']
            num_seats = int(request.form['num_seats'])

            p = Person(name, email)
            rideshare = Rideshare(p, num_seats)
            # reservation.rideshares.add(rideshare)
            rideshare_id = reservation.register_rideshare(rideshare)
            serialize_manager()

            return redirect('/event/{}/rideshare/{}'.format(
                event_id, rideshare_id))
        else:
            print(reservation.rideshares)
            rideshare = reservation.rideshares[rideshare_id]

            rideshare_request_matches = \
                reservation.get_rideshare_request_matches(rideshare)

            html = "Thanks for offering a ride"
            html += " -- you have {} of {} spots available".format(
                rideshare.seats_available(),
                rideshare.number_seats)
            html += "<br><br>"
            html += "<h1>Reserved</h1>"
            if len(rideshare.riders) == 0:
                html += "None Yet!"
            else:
                html += '<ul>'
                for rider in rideshare.riders:
                    html += "<li>{}</li>".format(rider.name)
                html += '</ul>'
            html += "<br><br>"
            html += "<h1>Open</h1>"

            if len(rideshare_request_matches) == 0:
                html += "No one needs a ride yet - we'll email you if you can help"
            else:
                html += 'Select up to {} requests to reserve spots'.format(rideshare.seats_available())
                html += '<form action="reserved" method="post">'
                for rideshare_request, request_id in rideshare_request_matches:
                    requester = rideshare_request.requester
                    html += '<input type="checkbox" '
                    html += 'name="id" value="{}" '.format(request_id)
                    html += '/>'
                    html += ' {}'.format(requester.name)
                    html += ' <br>'
                html += '<input type="submit" value="Submit">'
                html += '</form>'

            return html
    except Exception as e:
        print('>>> error!')
        import traceback
        print(traceback.format_exc())
        print(manager.reservation_map)
        raise e


@app.route('/event/<event_id>/rideshare/<rideshare_id>/reserved', methods=['POST'])
def rides_reserved(event_id=None, rideshare_id=None):
    reservation = manager.reservation_map[event_id]
    rideshare = reservation.rideshares[rideshare_id]

    reserved_request_ids = request.form.getlist('id')
    for request_id in reserved_request_ids:
        rideshare_request = reservation.rideshare_requests[request_id]
        requester = rideshare_request.requester

        rideshare.reserve_seat(requester)

    serialize_manager()

    return redirect('/event/{}/rideshare/{}'.format(
                    event_id, rideshare_id))


def serialize_manager():
    pass
    # with open(PICKLE_FNAME, 'wb') as f:
    #     pickle.dump(manager, f)

if __name__ == '__main__':
    app.run()
