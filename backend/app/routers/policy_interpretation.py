from fastapi import APIRouter, HTTPException, Request
from app.infra.p3ai_client import get_p3ai_client

router = APIRouter()

@router.post("/simplify")
async def simplify_policy(request: Request):
    """
    Simplifies complex government policy documents into understandable language.
    """
    print(f"=== INTERPRET ENDPOINT HIT ===")
    try:
        body = await request.json()
        policy_text = body.get("policy_text", "")
        
        if not policy_text:
            return {"error": "policy_text is required"}
        
        print(f"Policy text length: {len(policy_text)}")
        print(f"Policy text preview: {policy_text[:100]}...")
        
        client = get_p3ai_client()
        llm = client.get_llm()
        
        if not llm:
            return {"error": "LLM not available"}
        
        prompt = f"""Simplify this government policy into simple language:

{policy_text}

Provide a clear explanation."""

        response = llm.invoke(prompt)
        simplified_text = response.content if hasattr(response, 'content') else str(response)
        
        return {
            "success": True,
            "interpretation": simplified_text
        }
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"error": str(e)}

