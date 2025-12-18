from fastapi import APIRouter, HTTPException
from app.schemas import (
    IssueCredentialRequest,
    IssueCredentialResponse,
    AdvocacyRequest,
    AdvocacyResponse,
    CitizenProfile
)
from app.agents.credential_issuer_agent import CredentialIssuerAgent
from app.agents.advocacy_agent import AdvocacyAgent
from app.agents.citizen_agent import CitizenAgent
from app.infra.p3ai_client import get_p3ai_client

router = APIRouter()


@router.get("/status")
async def get_system_status():
    """
    Get system status including ZyndAI network connection.
    """
    try:
        client = get_p3ai_client()
        status = client.get_connection_status()
        
        # Check if we have real network connection
        is_connected = status.get("connected", False)
        
        return {
            "system": "Policy Navigator",
            "version": "1.0.0",
            "zyndai": status,
            "features": {
                "policy_interpretation": True,
                "eligibility_checking": True,
                "benefit_matching": True,
                "credential_issuance": is_connected,
                "agent_discovery": is_connected,
                "encrypted_communication": is_connected
            }
        }
    except Exception as e:
        return {
            "system": "Policy Navigator",
            "error": str(e),
            "zyndai": {"connected": False}
        }


@router.post("/issue-credential", response_model=IssueCredentialResponse)
async def issue_credential(request: IssueCredentialRequest):
    """
    Issue verifiable credentials for a citizen using real ZyndAI network.
    """
    try:
        client = get_p3ai_client()
        
        # Check if ZyndAI network is available
        if not client.is_p3ai_available():
            # Fallback to simulation mode
            agent = CredentialIssuerAgent()
            result = agent.handle({
                "citizen_profile": request.citizen_profile
            })
        else:
            # Use real ZyndAI agent for credential issuance
            agent = CredentialIssuerAgent()
            result = agent.handle({
                "citizen_profile": request.citizen_profile
            })
            
            # If we have a real agent, we could discover credential issuers on the network
            if client.agent:
                try:
                    # Search for credential issuers on ZyndAI network
                    issuers = client.search_agents(
                        capabilities=["credential_issuer", "government_verification"],
                        match_score_gte=0.7,
                        top_k=3
                    )
                    
                    if issuers:
                        result["network_issuers_found"] = len(issuers)
                        result["message"] = f"{result['count']} credential(s) issued. Found {len(issuers)} network issuers available."
                except Exception as e:
                    # If network search fails, continue with local credentials
                    result["message"] = f"{result['count']} credential(s) issued locally."
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return IssueCredentialResponse(
            credentials=result["credentials"],
            message=result.get("message", f"{result['count']} credential(s) issued successfully")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error issuing credentials: {str(e)}")


@router.post("/advocacy", response_model=AdvocacyResponse)
async def get_advocacy(request: AdvocacyRequest):
    """
    Get step-by-step guidance for applying to a benefit.
    """
    try:
        client = get_p3ai_client()
        llm = client.get_llm()
        
        if not llm:
            raise HTTPException(
                status_code=503,
                detail="LLM service not available. Please configure OPENAI_API_KEY."
            )
        
        agent = AdvocacyAgent(llm=llm)
        result = agent.handle({
            "policy_name": request.policy_name,
            "citizen_profile": request.citizen_profile
        })
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return AdvocacyResponse(
            policy_name=result["policy_name"],
            guidance=result["guidance"],
            steps=result["steps"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating guidance: {str(e)}")


@router.post("/profile")
async def create_profile(profile_data: CitizenProfile):
    """
    Create or update a citizen profile.
    """
    try:
        agent = CitizenAgent()
        result = agent.handle(profile_data.dict())
        
        return {
            "profile": result["profile"],
            "message": result["message"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating profile: {str(e)}")