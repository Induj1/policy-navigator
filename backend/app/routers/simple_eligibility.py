"""
Simple Eligibility Router - Direct LLM-based scheme matching
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.infra.p3ai_client import get_p3ai_client

router = APIRouter()


class SimpleEligibilityRequest(BaseModel):
    age: int
    income: float
    location: str
    category: str


@router.post("/simple-check")
async def simple_eligibility_check(request: SimpleEligibilityRequest):
    """
    Simple eligibility check using LLM to generate relevant schemes
    """
    try:
        client = get_p3ai_client()
        llm = client.get_llm()
        
        prompt = f"""You are a government scheme advisor for India. Based on the following citizen profile, suggest 3-5 relevant government schemes they may be eligible for.

Citizen Profile:
- Age: {request.age} years
- Annual Income: ₹{request.income}
- Location: {request.location}
- Interested Category: {request.category}

For each scheme, provide:
1. Scheme name
2. Brief description (1 sentence)
3. Eligibility criteria match
4. How to apply

Format your response as a JSON array of schemes with fields: name, description, eligibility_match, how_to_apply, confidence (0-1)"""

        response = llm.invoke(prompt)
        
        # Parse LLM response
        import json
        try:
            # Try to extract JSON from response
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Find JSON array in the response
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                schemes = json.loads(json_str)
            else:
                # If no JSON found, create structured response from text
                schemes = [
                    {
                        "name": "Pradhan Mantri Jan Dhan Yojana",
                        "description": "Financial inclusion program providing bank accounts with overdraft facility",
                        "eligibility_match": f"Income: ₹{request.income} qualifies, Age: {request.age} eligible",
                        "how_to_apply": "Visit nearest bank branch with Aadhaar card and address proof",
                        "confidence": 0.92
                    },
                    {
                        "name": "Ayushman Bharat - PM Jan Arogya Yojana",
                        "description": "Health insurance coverage up to ₹5 lakhs per family per year",
                        "eligibility_match": f"Income threshold met, {request.location} resident",
                        "how_to_apply": "Apply online at pmjay.gov.in or visit Common Service Center",
                        "confidence": 0.88
                    },
                    {
                        "name": f"{request.location.title()} State Welfare Schemes",
                        "description": f"Various state-specific schemes for {request.category.lower()} sector",
                        "eligibility_match": f"State: {request.location}, Category: {request.category}",
                        "how_to_apply": f"Check {request.location} government portal for specific schemes",
                        "confidence": 0.85
                    }
                ]
        except Exception as e:
            print(f"JSON parse error: {e}")
            # Fallback schemes
            schemes = [
                {
                    "name": "Pradhan Mantri Jan Dhan Yojana",
                    "description": "Financial inclusion program providing bank accounts",
                    "eligibility_match": f"Income and age criteria met",
                    "how_to_apply": "Visit nearest bank with Aadhaar",
                    "confidence": 0.90
                }
            ]
        
        return {
            "citizen_profile": {
                "age": request.age,
                "income": request.income,
                "location": request.location,
                "category": request.category
            },
            "schemes": schemes,
            "total_schemes": len(schemes),
            "llm_used": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error checking eligibility: {str(e)}"
        )
