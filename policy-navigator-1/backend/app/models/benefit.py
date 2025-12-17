from pydantic import BaseModel
from typing import List, Optional

class Benefit(BaseModel):
    id: str
    name: str
    description: str
    eligibility_criteria: List[str]
    amount: float
    duration: Optional[int] = None  # Duration in months, if applicable
    application_link: Optional[str] = None  # Link to apply for the benefit

    class Config:
        orm_mode = True