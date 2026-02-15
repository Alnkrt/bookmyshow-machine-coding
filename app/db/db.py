from collections import defaultdict
from typing import Dict

from app.models import Movies, Theatre, Shows, Seats, Ticket, Screen, SeatBooking
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

theaters : Dict[str, Theatre] = {}
movies : Dict[str, Movies] = {}
shows : Dict[str, Shows] = {}
screens : Dict[str, Screen] = {}
seats : Dict[int, Seats] = {}
bookings : Dict[int, SeatBooking] = {}
tickets : Dict[str, Ticket] = {}

theatre_city_index = defaultdict(list)
seat_show_index = defaultdict(list)

