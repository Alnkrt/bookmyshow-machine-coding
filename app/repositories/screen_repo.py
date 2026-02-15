from app.db.db import *

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
