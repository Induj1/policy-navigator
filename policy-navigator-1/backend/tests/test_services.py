import pytest
from app.services.credential_service import CredentialService
from app.services.policy_service import PolicyService
from app.services.llm_service import LLMService

@pytest.fixture
def credential_service():
    return CredentialService()

@pytest.fixture
def policy_service():
    return PolicyService()

@pytest.fixture
def llm_service():
    return LLMService()

def test_credential_service_valid_credentials(credential_service):
    valid_credentials = {
        "name": "John Doe",
        "age": 30,
        "income": 50000,
        "state": "CA"
    }
    assert credential_service.validate_credentials(valid_credentials) is True

def test_credential_service_invalid_credentials(credential_service):
    invalid_credentials = {
        "name": "",
        "age": -1,
        "income": 50000,
        "state": "CA"
    }
    assert credential_service.validate_credentials(invalid_credentials) is False

def test_policy_service_get_policy(policy_service):
    policy_id = 1
    policy = policy_service.get_policy(policy_id)
    assert policy is not None
    assert policy.id == policy_id

def test_llm_service_generate_response(llm_service):
    prompt = "What are the eligibility requirements for food assistance?"
    response = llm_service.generate_response(prompt)
    assert response is not None
    assert isinstance(response, str)  # Ensure the response is a string

def test_policy_service_match_benefits(policy_service):
    citizen_data = {
        "age": 30,
        "income": 40000,
        "state": "CA"
    }
    benefits = policy_service.match_benefits(citizen_data)
    assert isinstance(benefits, list)  # Ensure the result is a list
    assert len(benefits) > 0  # Ensure there are matching benefits