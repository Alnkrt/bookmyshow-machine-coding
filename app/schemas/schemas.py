import enum
from datetime import datetime
from typing import List

from pydantic import BaseModel


class Theatre(BaseModel):
    id : str
    name : str
    pincode : str
    city : str
    state : str

class Screen(BaseModel) :
    id : str
    name : str
    theater_id : str

class Movies(BaseModel):
    id : str
    name : str
    duration : int
    director : str
    genre : str
    rating : int
    producer : str
    cast : str
    country : str
    language : str

class Shows(BaseModel):
    id : str
    name : str
    screen_id : str
    movie_id : str
    start_time : datetime
    end_time : datetime
    movie_id : str

class SeatType(str, enum.Enum):
    regular = 'REGULAR'
    elite = 'ELITE'
    premium = 'PREMIUM'

class SeatStatus(str, enum.Enum):
    available = 'AVAILABLE'
    booked = 'BOOKED'
    locked = 'LOCKED'

class Seats(BaseModel):
    id : int
    seat_type : SeatType
    screen_id : str

class SeatBooking(BaseModel):
    id : int
    seat_id : int
    show_id : str
    status : SeatStatus
    locked_at : datetime
    price : float


class Ticket(BaseModel):
    id : str
    seat_type : SeatType
    show_id : str
    price : float
    gst: float
    total_amount: float
    seats : List[int]
    is_paid: bool
    booked_at : datetime
