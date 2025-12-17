from fastapi import APIRouter, HTTPException
from app.agents.benefit_matcher import BenefitMatchingAgent
from app.models.credential import CitizenCredential
from app.models.benefit import Benefit

router = APIRouter()

@router.post("/match-benefits", response_model=list[Benefit])
async def match_benefits(credential: CitizenCredential):
    agent = BenefitMatchingAgent()
    try:
        benefits = agent.match(credential)
        return benefits
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))