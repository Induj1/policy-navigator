from pydantic import BaseModel, constr, validator

class PolicyInput(BaseModel):
    policy_text: str

    @validator('policy_text')
    def validate_policy_text(cls, value):
        if not value:
            raise ValueError('Policy text cannot be empty.')
        return value

class CredentialInput(BaseModel):
    citizen_id: constr(min_length=1)
    income: float
    state: constr(min_length=2, max_length=2)

    @validator('income')
    def validate_income(cls, value):
        if value < 0:
            raise ValueError('Income must be a non-negative number.')
        return value

class BenefitInput(BaseModel):
    benefit_name: str

    @validator('benefit_name')
    def validate_benefit_name(cls, value):
        if not value:
            raise ValueError('Benefit name cannot be empty.')
        return value