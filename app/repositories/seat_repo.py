from app.models import *
from app.db.db import *

class SeatRepository:
    def __init__(self) -> None:
        pass

    def add_seat(self, seat: Seats):
        seats[seat.id] = seat.model_dump()
        return True

    def remove_seat(self, seat_id: str):
        del seats[seat_id]
        return True

    def get_seat(self, seat_id: str):
        return seats[seat_id]

    def get_all_seats(self):
        return seats
