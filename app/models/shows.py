from datetime import datetime

from pydantic import BaseModel


class Shows(BaseModel):
    id : str
    name : str
    screen_id : str
    movie_id : str
    start_time : datetime
    end_time : datetime
    movie_id : str
