from typing import Dict, Any
from .base_agent import BaseAgent
from app.schemas import (
    CitizenProfile, 
    Policy, 
    PolicyRule, 
    OperatorEnum,
    EligibilityResult, 
    EligibilityReason
)

class EligibilityAgent(BaseAgent):
    """Agent responsible for checking citizen eligibility against policy rules."""
    
    def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a citizen is eligible for a policy.
        
        Args:
            context: Dict with 'citizen_profile' (CitizenProfile) and 'policy' (Policy)
        
        Returns:
            Dict with 'result' (EligibilityResult) or 'error'
        """
        try:
            citizen_profile: CitizenProfile = context.get("citizen_profile")
            policy: Policy = context.get("policy")
            
            if not citizen_profile:
                return {"error": "citizen_profile is required"}
            
            if not policy:
                return {"error": "policy is required"}
            
            # Check each rule
            reasons = []
            all_satisfied = True
            
            for rule in policy.rules:
                satisfied = self._check_rule(citizen_profile, rule)
                
                reason = EligibilityReason(
                    rule=rule,
                    satisfied=satisfied,
                    message=self._get_reason_message(rule, satisfied, citizen_profile)
                )
                reasons.append(reason)
                
                if not satisfied:
                    all_satisfied = False
            
            result = EligibilityResult(
                policy_id=policy.name,
                policy_name=policy.name,
                eligible=all_satisfied,
                reasons=reasons,
                confidence=1.0 if all_satisfied else 0.0
            )
            
            return {"result": result}
        
        except Exception as e:
            return {"error": f"Error checking eligibility: {str(e)}"}
    
    def _check_rule(self, citizen_profile: CitizenProfile, rule: PolicyRule) -> bool:
        """Check if a single rule is satisfied."""
        # Get the citizen's value for this attribute
        citizen_value = getattr(citizen_profile, rule.key, None)
        
        # Handle credentials if checking credential-based rules
        if citizen_value is None and citizen_profile.credentials:
            for cred in citizen_profile.credentials:
                if rule.key in cred.data:
                    citizen_value = cred.data[rule.key]
                    break
        
        if citizen_value is None:
            return False
        
        # Evaluate based on operator
        if rule.operator == OperatorEnum.EQUAL:
            return citizen_value == rule.value
        elif rule.operator == OperatorEnum.NOT_EQUAL:
            return citizen_value != rule.value
        elif rule.operator == OperatorEnum.GREATER_THAN:
            return float(citizen_value) > float(rule.value)
        elif rule.operator == OperatorEnum.LESS_THAN:
            return float(citizen_value) < float(rule.value)
        elif rule.operator == OperatorEnum.GREATER_THAN_OR_EQUAL:
            return float(citizen_value) >= float(rule.value)
        elif rule.operator == OperatorEnum.LESS_THAN_OR_EQUAL:
            return float(citizen_value) <= float(rule.value)
        
        return False
    
    def _get_reason_message(self, rule: PolicyRule, satisfied: bool, citizen_profile: CitizenProfile) -> str:
        """Generate a human-readable message for the eligibility reason."""
        citizen_value = getattr(citizen_profile, rule.key, None)
        
        if citizen_value is None and citizen_profile.credentials:
            for cred in citizen_profile.credentials:
                if rule.key in cred.data:
                    citizen_value = cred.data[rule.key]
                    break
        
        if satisfied:
            return f"✓ Requirement met: {rule.key} {rule.operator.value} {rule.value} (your value: {citizen_value})"
        else:
            if citizen_value is None:
                return f"✗ Missing required information: {rule.key}"
            return f"✗ Requirement not met: {rule.key} {rule.operator.value} {rule.value} (your value: {citizen_value})"