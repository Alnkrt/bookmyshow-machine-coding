from pydantic import BaseModel


class Theatre(BaseModel):
    id : str
    name : str
    pincode : str
    city : str
    state : str
