from fastapi import APIRouter, HTTPException
from app.schemas import (
    EligibilityCheckRequest,
    BenefitMatchResponse
)
from app.agents.benefit_matching_agent import BenefitMatchingAgent
from app.agents.credential_issuer_agent import CredentialIssuerAgent
from app.infra.p3ai_client import get_p3ai_client

router = APIRouter()


@router.post("/match", response_model=BenefitMatchResponse)
async def match_benefits(request: EligibilityCheckRequest):
    """
    Match citizen with eligible policies and benefits.
    """
    try:
        client = get_p3ai_client()
        llm = client.get_llm()
        
        # Issue credentials for the citizen first
        credential_agent = CredentialIssuerAgent()
        cred_result = credential_agent.handle({
            "citizen_profile": request.citizen_profile
        })
        
        if "error" in cred_result:
            raise HTTPException(status_code=400, detail=cred_result["error"])
        
        # Update citizen profile with credentials
        request.citizen_profile.credentials = cred_result["credentials"]
        
        # Match benefits
        matching_agent = BenefitMatchingAgent(llm=llm)
        result = matching_agent.handle({
            "citizen_profile": request.citizen_profile,
            "policies": request.policies
        })
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result["response"]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching benefits: {str(e)}")


@router.post("/check")
async def check_single_eligibility(request: EligibilityCheckRequest):
    """
    Check eligibility for specific policies.
    """
    try:
        from app.agents.eligibility_agent import EligibilityAgent
        from app.agents.credential_issuer_agent import CredentialIssuerAgent
        
        # Issue credentials
        credential_agent = CredentialIssuerAgent()
        cred_result = credential_agent.handle({
            "citizen_profile": request.citizen_profile
        })
        
        request.citizen_profile.credentials = cred_result["credentials"]
        
        # Check eligibility for each policy
        eligibility_agent = EligibilityAgent()
        results = []
        
        for policy in request.policies:
            result = eligibility_agent.handle({
                "citizen_profile": request.citizen_profile,
                "policy": policy
            })
            if result.get("result"):
                results.append(result["result"])
        
        return {
            "results": results,
            "total_checked": len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking eligibility: {str(e)}")