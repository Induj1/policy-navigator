from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.policy_interpreter import PolicyInterpreterAgent

router = APIRouter()

class PolicyInput(BaseModel):
    policy_text: str

class PolicyOutput(BaseModel):
    structured_rules: dict

@router.post("/interpret", response_model=PolicyOutput)
async def interpret_policy(policy_input: PolicyInput):
    agent = PolicyInterpreterAgent()
    try:
        structured_rules = agent.handle(policy_input.policy_text)
        return PolicyOutput(structured_rules=structured_rules)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))