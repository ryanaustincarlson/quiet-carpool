
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
    manager = ReservationManager()
    manager.reservation_map['1'] = Reservation(Event('partytime',
                                               Person('Roberto', 'a@a.com')))


@app.route('/')
def index():
    return open('create_event.html', 'r').read()


@app.route('/event', methods=['POST'])
@app.route('/event/<event_id>/', methods=['GET'])
def event(event_id=None):
    print('event_id:', event_id)
    if event_id is None:
        organizer_name = request.form['org_name']
        organizer_email = request.form['org_email']
        organizer = Person(name=organizer_name,
                           email=organizer_email)

        # create an event
        event_name = request.form['event_name']
        event = Event(event_name, organizer)

        location = request.form['location']
        event.location = location if len(location) > 0 else None

        event_id = manager.register_event(event)
        serialize_manager()

        return redirect('/event/{}'.format(event_id))
    else:
        reservation = manager.reservation_map[event_id]
        return render_template('event.html',
                               event_name=reservation.event.name,
                               org_name=reservation.event.organizer.name)


@app.route('/event/<event_id>/request_ride', methods=['POST'])
@app.route('/event/<event_id>/request_ride/<ride_request_id>/', methods=['GET'])
def need_a_ride(event_id=None, ride_request_id=None):
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
        open_rideshares = reservation.get_open_rideshares(
            rideshare_request.number_seats)

        html = ''
        if len(open_rideshares) == 0:
            html = 'Sorry, there are no available rideshares at this time. '
            html += 'Check back soon to see when rides become available'
        else:
            html = 'There are {} rides available'.format(len(open_rideshares))
            html += '<br><br>'
            html += 'Select any rides you wouldd be happy taking'
            html += '<form action="requested" method="post">'
            for rideshare in open_rideshares:
                ride_sharer = rideshare.ride_sharer
                html += '<input type="checkbox" '
                html += 'value="blah" '
                html += '/>'
                html += '{} ({} seat{})'.format(
                    ride_sharer.name, rideshare.seats_available(),
                    's' if rideshare.seats_available() != 1 else '')
                html += ' <br>'
            html += '<input type="submit" value="Submit">'
            html += '</form>'

        for rideshare in open_rideshares:
            print(rideshare)

        return html


@app.route('/event/<event_id>/rideshare', methods=['POST'])
@app.route('/event/<event_id>/rideshare/<rideshare_id>/', methods=['GET'])
def have_a_ride(event_id=None, rideshare_id=None):
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
        rideshare = reservation.rideshares[rideshare_id]
        return "Thanks! We'll let you know if anyone needs a ride!"


def serialize_manager():
    with open(PICKLE_FNAME, 'wb') as f:
        pickle.dump(manager, f)

if __name__ == '__main__':
    app.run(debug=True)
