from pydantic import BaseModel
from typing import List, Optional

class Policy(BaseModel):
    id: str
    title: str
    description: str
    eligibility_criteria: List[str]
    benefits: List[str]
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True