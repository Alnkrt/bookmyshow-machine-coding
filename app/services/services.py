from datetime import datetime, timedelta

from app.db.db import theatre_city_index
from app.repositories import TheaterRepository, ShowRepository, MovieRepository, TicketRepository, \
    ScreenRepository, SeatRepository, SeatBookingRepository
from app.models import SeatStatus, Seats, SeatBooking

theatre_obj = TheaterRepository()
shows_obj = ShowRepository()
movies_obj = MovieRepository()
screens_obj = ScreenRepository()
seat_booking_obj = SeatBookingRepository()
tickets_obj = TicketRepository()
seat_obj = SeatRepository()


def get_theatre_by_city(city):
    all_theatres = theatre_obj.get_all_theaters()
    theatre_ids = theatre_city_index[city]

    return [all_theatres[idx] for idx in theatre_ids]

def get_shows_by_city(city):
    theatre_ids = theatre_city_index[city]
    all_screens = screens_obj.get_all_screens()
    filtered_screens = [screen for key, screen in all_screens.items() if screen.theater_id in theatre_ids]
    filtered_screens_id = [s['id'] for s in filtered_screens]
    all_shows = shows_obj.get_all_shows()
    filtered_shows = [show for key, show in all_shows.items() if show['screen_id'] in filtered_screens_id]

    return filtered_shows

def get_shows_by_movie(city: str, movie: str):
    all_movies = movies_obj.get_all_movies()
    target_movie = [m for key, m in all_movies.items() if m['name'].startswith(movie)]
    if len(target_movie):
        theatre_ids = theatre_city_index[city]
        all_screens = screens_obj.get_all_screens()
        filtered_screens = [screen for key, screen in all_screens.items() if screen['theater_id'] in theatre_ids]
        filtered_screens_id = [s['id'] for s in filtered_screens]
        all_shows = shows_obj.get_all_shows()
        filtered_shows = [show for key, show in all_shows.items() if show['screen_id'] in filtered_screens_id and show['movie_id'] == target_movie[0]['id']]
        return filtered_shows

    return []

def get_seats_by_show( show_id: str):
    all_seats = seat_booking_obj.get_all_seats()
    all_seats =[seat for key, seat in all_seats.items()]
    available_seats = [seat for seat in all_seats if seat['show_id'] == show_id and is_seat_available(seat)]

    return available_seats

def lock_seat(show_id:str, seat_ids: list):
    show = shows_obj.get_show(show_id)
    movie = movies_obj.get_movie(show['movie_id'])
    seats = seat_booking_obj.get_all_seats()
    for id in seat_ids:
            seat = [s  for key, s in seats.items() if s['seat_id'] == id][0]
            if is_seat_available(seat):
                seat_booking_obj.update_seat(seat_id=id, show_id = show_id, seat={'status' : SeatStatus.locked, 'locked_at' : datetime.now()})
            else:
                raise Exception('Seats are already booked')

    amount = sum(seat['price'] for key,seat in seats.items() if seat['seat_id'] in seat_ids)
    print('seats chosen successfully , Pay within 5 minutes for successful booking.')
    print('Movie: ', movie['name'], '\nTiming:', show['start_time'],  '\nSeats: ', seat_ids, "\nAmount: ", amount)

def book_ticket(show_id:str, seat_ids: list):
    seats = seat_booking_obj.get_all_seats()

    selected_seats = [s for key, s in seats.items() if s['show_id'] == show_id and s['seat_id'] in seat_ids]

    for seat in selected_seats:
        if seat['status'] == SeatStatus.locked and seat['locked_at'] > datetime.now() - timedelta(minutes=20):
            seat_booking_obj.update_seat(seat_id= seat['seat_id'] , show_id=show_id , seat={'status' : SeatStatus.booked})
        else:
            raise Exception('Seats are already booked')

    print('Ticket successfully booked successfully.')
    return True

def is_seat_available(seat: SeatBooking) -> bool:
    """
    Returns True if seat is AVAILABLE or if the Lock has EXPIRED.
    """
    # Case 1: Already Booked (Permanent)

    lock_timeout = 5
    if seat['status'] == SeatStatus.booked:
        return False

    # Case 2: Available
    if seat['status'] == SeatStatus.available:
        return True

    # Case 3: Locked (Check for Expiry)
    if seat['status'] == SeatStatus.locked:
        if not seat.locked_at:
            return True  # Should not happen, but safe fallback

        # check difference
        elapsed = datetime.now() - seat.locked_at
        if elapsed > timedelta(minutes=lock_timeout):
            return True  # Lock Expired -> It's free real estate!

        return False  # Still valid lock

    return False

