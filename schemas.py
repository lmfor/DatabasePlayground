from pydantic import BaseModel

class CityBase(BaseModel):
    name: str
    country: str

class CityCreate(CityBase):
    pass

class CityRead(CityBase):
    id: int

    class Config:
        orm_mode = True  # This allows Pydantic to read data from SQLAlchemy models