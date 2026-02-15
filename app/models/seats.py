import enum

from pydantic import BaseModel


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
