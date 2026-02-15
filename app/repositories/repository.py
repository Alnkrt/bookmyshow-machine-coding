
from app.db.db import theaters, shows, seats, tickets, movies, screens, theatre_city_index, seat_show_index, bookings
from app.schemas.schemas import *


class TheaterRepository:
    def __init__(self) -> None:
        pass

    def add_theater(self, theater: Theatre):
        theaters[theater.id] = theater.model_dump()
        theatre_city_index[theater.city].append(theater.id)
        return True

    def remove_theater(self, theater_id: str):
        theater = theaters[theater_id]
        del theaters[theater_id]
        theatre_city_index[theater.city].remove(theater.id)
        return  True

    def get_theater(self, theater_id: str):
        return theaters[theater_id]

    def get_all_theaters(self):
        return theaters

class ScreenRepository:
    def __init__(self) -> None:
        pass

    def add_screen(self, screen: Screen):
        screens[screen.id] = screen.model_dump()
        return True

    def remove_screen(self, screen_id: str):
        del screens[screen_id]
        return True

    def get_screen(self, screen_id: str):
        return screens[screen_id]

    def get_all_screens(self):
        return screens

class ShowRepository:
    def __init__(self) -> None:
        pass

    def add_show(self, show: Shows):
        shows[show.id] = show.model_dump()
        return True

    def remove_show(self, show_id: str):
        del shows[show_id]
        return True

    def get_show(self, show_id: str):
        return shows[show_id]

    def get_all_shows(self):
        return shows

class MovieRepository:
    def __init__(self) -> None:
        pass

    def add_movie(self, movie: Movies):
        movies[movie.id] = movie.model_dump()
        return True

    def remove_movie(self, movie_id: str):
        del movies[movie_id]
        return True

    def get_movie(self, movie_id: str):
        return movies[movie_id]

    def get_all_movies(self):
        return movies

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


class TicketRepository:
    def __init__(self) -> None:
        pass

    def add_ticket(self, ticket: Ticket):
        tickets[ticket.id] = ticket.model_dump()
        return True

    def remove_ticket(self, ticket_id: str):
        del tickets[ticket_id]
        return True

    def get_ticket(self, ticket_id: str):
        return tickets[ticket_id]

    def get_all_tickets(self):
        return tickets