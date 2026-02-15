from app.db.db import *

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
