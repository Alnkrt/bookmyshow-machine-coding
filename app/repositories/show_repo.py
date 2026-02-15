from app.models import *
from app.db.db import *

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
