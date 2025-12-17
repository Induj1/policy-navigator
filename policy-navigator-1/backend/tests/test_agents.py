from fastapi import HTTPException
import pytest
from app.agents.policy_interpreter import PolicyInterpreterAgent
from app.agents.eligibility_verifier import EligibilityAgent
from app.agents.benefit_matcher import BenefitMatchingAgent

@pytest.fixture
def policy_interpreter_agent():
    return PolicyInterpreterAgent()

@pytest.fixture
def eligibility_agent():
    return EligibilityAgent()

@pytest.fixture
def benefit_matching_agent():
    return BenefitMatchingAgent()

def test_policy_interpreter_agent(policy_interpreter_agent):
    raw_policy = "Citizens with an income below $30,000 are eligible for assistance."
    structured_rules = policy_interpreter_agent.handle(raw_policy)
    assert structured_rules is not None
    assert "income" in structured_rules
    assert structured_rules["income"]["max"] == 30000

def test_eligibility_agent(eligibility_agent):
    citizen_credentials = {"income": 25000, "state": "CA"}
    policy_rules = {"income": {"max": 30000}}
    eligibility_result = eligibility_agent.handle(citizen_credentials, policy_rules)
    assert eligibility_result is True

def test_benefit_matching_agent(benefit_matching_agent):
    citizen_profile = {"income": 25000, "state": "CA"}
    eligible_policies = [{"name": "Assistance Program", "income_limit": 30000}]
    matched_benefits = benefit_matching_agent.handle(citizen_profile, eligible_policies)
    assert len(matched_benefits) > 0
    assert matched_benefits[0]["name"] == "Assistance Program"