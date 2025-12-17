from pydantic import BaseModel

class CitizenProfile(BaseModel):
    id: int
    name: str
    email: str
    date_of_birth: str
    address: str
    phone_number: str
    verified: bool = False

    class Config:
        orm_mode = True