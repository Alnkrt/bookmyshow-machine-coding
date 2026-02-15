from pydantic import BaseModel


class Screen(BaseModel) :
    id : str
    name : str
    theater_id : str
