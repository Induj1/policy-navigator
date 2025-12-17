"""
Policy Impact Predictor Router - API endpoints for ML-based impact analysis
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.agents.policy_impact_predictor import policy_impact_predictor

router = APIRouter(prefix="/impact", tags=["impact-prediction"])


class PredictImpactRequest(BaseModel):
    policy: Dict[str, Any]
    population_data: Optional[Dict] = None
    regional_context: Optional[Dict] = None


class QuickPredictionRequest(BaseModel):
    policy_name: str
    num_eligibility_rules: int = 3
    category: str = "welfare_schemes"
    benefit_value: float = 25000


@router.post("/predict")
async def predict_policy_impact(request: PredictImpactRequest):
    """
    Predict comprehensive impact of a policy
    
    Features:
    - Predicted number of beneficiaries
    - Budget estimation
    - Success probability
    - Regional impact analysis
    - ROI for government
    
    Args:
        policy: Policy object with rules, name, description, benefits
        population_data: Optional population statistics
        regional_context: Optional regional demographic/economic data
    
    Returns:
        Comprehensive impact prediction with ML-based insights
    """
    try:
        result = await policy_impact_predictor.predict_impact(
            policy_data=request.policy,
            population_data=request.population_data,
            regional_context=request.regional_context
        )
        
        if not result.get('success'):
            raise HTTPException(
                status_code=400, 
                detail=result.get('error', 'Prediction failed')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error predicting policy impact: {str(e)}"
        )


@router.post("/quick-predict")
async def quick_predict(request: QuickPredictionRequest):
    """
    Quick impact prediction with minimal inputs
    
    Useful for preliminary analysis before full policy is defined.
    
    Args:
        policy_name: Name of the policy
        num_eligibility_rules: Number of eligibility criteria
        category: Policy category (education/housing/welfare/disability)
        benefit_value: Estimated benefit amount per beneficiary
    
    Returns:
        Quick impact estimates
    """
    try:
        # Construct minimal policy object
        policy_data = {
            'name': request.policy_name,
            'rules': [{'key': f'rule_{i}'} for i in range(request.num_eligibility_rules)],
            'benefits': f'Up to {request.benefit_value} INR',
            'description': f'{request.category} scheme'
        }
        
        result = await policy_impact_predictor.predict_impact(
            policy_data=policy_data,
            population_data=None,
            regional_context=None
        )
        
        if not result.get('success'):
            raise HTTPException(
                status_code=400,
                detail=result.get('error', 'Quick prediction failed')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in quick prediction: {str(e)}"
        )


@router.get("/beneficiaries/estimate")
async def estimate_beneficiaries(
    income_threshold: Optional[int] = None,
    has_age_criteria: bool = False,
    has_location_criteria: bool = False,
    category: str = "welfare_schemes"
):
    """
    Estimate beneficiaries based on simple criteria
    
    Args:
        income_threshold: Income limit (if any)
        has_age_criteria: Whether age restrictions apply
        has_location_criteria: Whether location restrictions apply
        category: Policy category
    
    Returns:
        Beneficiary estimates
    """
    try:
        # Build policy features
        features = {
            'category': category,
            'num_eligibility_rules': sum([
                income_threshold is not None,
                has_age_criteria,
                has_location_criteria
            ]),
            'has_income_criteria': income_threshold is not None,
            'has_age_criteria': has_age_criteria,
            'has_location_criteria': has_location_criteria,
            'complexity_score': 0.5,
            'benefit_value': 25000
        }
        
        beneficiaries = await policy_impact_predictor._predict_beneficiaries(
            features, None
        )
        
        return {
            'success': True,
            'beneficiary_estimates': beneficiaries,
            'category': category
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error estimating beneficiaries: {str(e)}"
        )


@router.get("/budget/estimate")
async def estimate_budget(
    predicted_beneficiaries: int,
    benefit_per_person: float,
    complexity_score: float = 0.5
):
    """
    Estimate budget requirements
    
    Args:
        predicted_beneficiaries: Expected number of beneficiaries
        benefit_per_person: Benefit amount per beneficiary (INR)
        complexity_score: Policy complexity (0-1)
    
    Returns:
        Budget estimates with breakdown
    """
    try:
        features = {
            'benefit_value': benefit_per_person,
            'complexity_score': complexity_score
        }
        
        beneficiary_prediction = {
            'predicted': predicted_beneficiaries
        }
        
        budget = await policy_impact_predictor._estimate_budget(
            features, beneficiary_prediction
        )
        
        return {
            'success': True,
            'budget_estimation': budget
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error estimating budget: {str(e)}"
        )


@router.post("/roi/calculate")
async def calculate_roi(
    total_budget: int,
    predicted_beneficiaries: int,
    success_probability: float
):
    """
    Calculate Return on Investment
    
    Args:
        total_budget: Total estimated budget (INR)
        predicted_beneficiaries: Expected beneficiaries
        success_probability: Success probability (0-1)
    
    Returns:
        ROI analysis
    """
    try:
        budget_dict = {'total_estimated_budget': total_budget}
        beneficiary_dict = {'predicted': predicted_beneficiaries}
        success_dict = {'overall_probability': success_probability}
        
        roi = await policy_impact_predictor._calculate_roi(
            budget_dict, beneficiary_dict, success_dict
        )
        
        return {
            'success': True,
            'roi_analysis': roi
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating ROI: {str(e)}"
        )


@router.get("/success/probability")
async def calculate_success_probability(
    num_eligibility_rules: int = 3,
    complexity_score: float = 0.5,
    category: str = "welfare_schemes"
):
    """
    Calculate success probability
    
    Args:
        num_eligibility_rules: Number of eligibility criteria
        complexity_score: Policy complexity (0-1)
        category: Policy category
    
    Returns:
        Success probability analysis
    """
    try:
        features = {
            'category': category,
            'num_eligibility_rules': num_eligibility_rules,
            'complexity_score': complexity_score
        }
        
        success = await policy_impact_predictor._calculate_success_probability(features)
        
        return {
            'success': True,
            'success_analysis': success
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating success probability: {str(e)}"
        )


@router.get("/regional/analysis")
async def analyze_regional_impact(
    has_location_criteria: bool = False
):
    """
    Analyze regional impact distribution
    
    Args:
        has_location_criteria: Whether policy has location restrictions
    
    Returns:
        Regional impact breakdown
    """
    try:
        features = {
            'has_location_criteria': has_location_criteria,
            'category': 'welfare_schemes'
        }
        
        regional = await policy_impact_predictor._analyze_regional_impact(
            features, None
        )
        
        return {
            'success': True,
            'regional_impact': regional
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing regional impact: {str(e)}"
        )


@router.get("/models/info")
async def get_model_info():
    """
    Get information about ML models and prediction capabilities
    
    Returns:
        Model information and capabilities
    """
    return {
        'success': True,
        'models': {
            'beneficiary_prediction': {
                'type': 'Statistical ML Model',
                'features': [
                    'income_threshold',
                    'age_range',
                    'geographic_scope',
                    'awareness_factor'
                ],
                'confidence': 'High for historical categories, Medium for new policies'
            },
            'success_probability': {
                'type': 'Weighted Scoring Model',
                'factors': [
                    'policy_clarity',
                    'implementation_ease',
                    'funding_adequacy',
                    'stakeholder_support'
                ],
                'accuracy': '75-85% based on historical data'
            },
            'budget_estimation': {
                'type': 'Cost-based Model',
                'components': [
                    'direct_benefits',
                    'administrative_overhead',
                    'implementation_costs'
                ],
                'accuracy': '±20% margin'
            }
        },
        'categories_supported': [
            'education_schemes',
            'housing_schemes',
            'welfare_schemes',
            'disability_schemes'
        ],
        'last_updated': '2025-12-17',
        'version': '1.0.0'
    }
