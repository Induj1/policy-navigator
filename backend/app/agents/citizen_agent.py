from .base_agent import BaseAgent
from pydantic import BaseModel
from typing import Dict, Any

class CitizenProfile(BaseModel):
    income: float
    state: str
    is_student: bool

class CitizenAgent(BaseAgent):
    def handle(self, citizen_data: Dict[str, Any]) -> CitizenProfile:
        profile = CitizenProfile(**citizen_data)
        return profile