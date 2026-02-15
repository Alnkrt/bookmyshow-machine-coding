from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.models import SeatType


class Ticket(BaseModel):
    id : str
    seat_type : SeatType
    seat_number : int
    show_id : str
    price : float
    gst: float
    total_amount: float
    seats : List[int]
    is_paid: bool
    booked_at : datetime
