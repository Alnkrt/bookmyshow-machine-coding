from app.db.db import *

class SeatBookingRepository:
    def __init__(self) -> None:
        pass

    def add_seat(self, seat: SeatBooking):
        bookings[seat.id] = seat.model_dump()
        return True

    def remove_seat(self, id: str):
        del bookings[id]
        return True

    def get_seat(self, id: str):
        return bookings[id]

    def update_seat(self, seat_id: str, show_id: str, seat: dict):
        target_seat = [b for key, b in bookings.items() if b['seat_id'] == seat_id and b['show_id'] == show_id]
        if len(target_seat):
            for key, value in seat.items():
                if key in list(SeatBooking.model_fields.keys()):
                    bookings[target_seat[0]['id']][key] = value
        else:
            raise Exception("seat not found")
        return True

    def get_all_seats(self):
        return bookings

