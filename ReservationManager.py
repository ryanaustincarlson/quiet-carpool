
import uuid

from Reservation import Reservation


class ReservationManager:
    def __init__(self):
        # uuid -> reservation
        self.reservation_map = {}

    def register_event(self, event):
        event_id = ReservationManager.generate_uuid()
        self.reservation_map[event_id] = Reservation(event)
        return event_id

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())
