from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import (
    InterpretPolicyRequest,
    InterpretPolicyResponse,
    Policy
)
from app.agents.policy_interpreter_agent import PolicyInterpreterAgent
from app.infra.p3ai_client import get_p3ai_client
from app.infra.policy_fetcher import get_policy_fetcher

router = APIRouter()


@router.post("/interpret", response_model=InterpretPolicyResponse)
async def interpret_policy(request: InterpretPolicyRequest):
    """
    Interpret raw policy text and extract structured eligibility rules.
    """
    try:
        client = get_p3ai_client()
        llm = client.get_llm()
        
        if not llm:
            raise HTTPException(
                status_code=503,
                detail="LLM service not available. Please configure OPENAI_API_KEY."
            )
        
        agent = PolicyInterpreterAgent(llm=llm)
        
        result = agent.handle({
            "raw_text": request.raw_text,
            "policy_name": request.policy_name or "Untitled Policy"
        })
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return InterpretPolicyResponse(
            policy=result["policy"],
            message=f"Policy interpreted successfully. {result['rules_count']} rules extracted."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interpreting policy: {str(e)}")


@router.get("/sample", response_model=List[Policy])
async def get_sample_policies():
    """
    Get policies - tries to fetch from ZyndAI network first,
    falls back to hardcoded if network unavailable.
    """
    try:
        fetcher = get_policy_fetcher()
        policies = fetcher.fetch_all_policies()
        return policies
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching policies: {str(e)}")


@router.get("/by-state/{state}", response_model=List[Policy])
async def get_policies_by_state(state: str):
    """
    Get policies specific to a state from ZyndAI network.
    Falls back to filtered hardcoded policies if network unavailable.
    """
    try:
        fetcher = get_policy_fetcher()
        policies = fetcher.fetch_policies_by_state(state)
        return policies
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching state policies: {str(e)}")


@router.post("/refresh")
async def refresh_policies():
    """
    Force refresh policies from ZyndAI network.
    Clears cache and fetches fresh data.
    """
    try:
        fetcher = get_policy_fetcher()
        fetcher.clear_cache()
        policies = fetcher.fetch_all_policies()
        
        client = get_p3ai_client()
        
        return {
            "message": "Policies refreshed successfully",
            "count": len(policies),
            "source": "ZyndAI Network" if client.is_p3ai_available() else "Hardcoded",
            "network_connected": client.is_p3ai_available()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing policies: {str(e)}")