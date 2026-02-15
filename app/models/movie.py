from pydantic import BaseModel


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
