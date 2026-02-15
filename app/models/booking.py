from datetime import datetime

from pydantic import BaseModel

from app.models import SeatStatus


class SeatBooking(BaseModel):
    id : int
    seat_id : int
    show_id : str
    status : SeatStatus
    locked_at : datetime
    price : float

