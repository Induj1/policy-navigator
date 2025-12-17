from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.eligibility_verifier import EligibilityAgent

router = APIRouter()

class EligibilityRequest(BaseModel):
    citizen_id: str
    income: float
    state: str

class EligibilityResponse(BaseModel):
    eligible: bool
    message: str

@router.post("/check-eligibility", response_model=EligibilityResponse)
async def check_eligibility(request: EligibilityRequest):
    agent = EligibilityAgent()
    result = agent.verify_eligibility(request.citizen_id, request.income, request.state)
    
    if result['eligible']:
        return EligibilityResponse(eligible=True, message="You are eligible for benefits.")
    else:
        raise HTTPException(status_code=400, detail=result['message'])