from typing import List, Dict
from pydantic import BaseModel

class CitizenCredential(BaseModel):
    citizen_id: str
    income: float
    state: str

class PolicyRule(BaseModel):
    rule_id: str
    description: str
    eligibility_criteria: Dict[str, str]

class EligibilityResult(BaseModel):
    eligible: bool
    reasons: List[str]

class EligibilityAgent:
    def __init__(self, policy_rules: List[PolicyRule]):
        self.policy_rules = policy_rules

    def check_eligibility(self, credential: CitizenCredential) -> EligibilityResult:
        eligible = False
        reasons = []

        for rule in self.policy_rules:
            if self._matches_criteria(credential, rule.eligibility_criteria):
                eligible = True
                reasons.append(f"Eligible for rule: {rule.description}")

        return EligibilityResult(eligible=eligible, reasons=reasons)

    def _matches_criteria(self, credential: CitizenCredential, criteria: Dict[str, str]) -> bool:
        for key, value in criteria.items():
            if getattr(credential, key) != value:
                return False
        return True