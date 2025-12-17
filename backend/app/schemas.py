from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum


class OperatorEnum(str, Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="


class PolicyRule(BaseModel):
    """Represents a single eligibility rule extracted from policy text."""
    key: str = Field(..., description="The attribute name (e.g., 'income', 'state', 'is_student')")
    operator: OperatorEnum = Field(..., description="Comparison operator")
    value: Any = Field(..., description="The value to compare against")
    
    class Config:
        json_schema_extra = {
            "example": {
                "key": "income",
                "operator": "<=",
                "value": 800000
            }
        }


class Policy(BaseModel):
    """Represents a government policy/scheme."""
    id: Optional[str] = None
    name: str = Field(..., description="Policy/scheme name")
    raw_text: str = Field(..., description="Original policy text")
    rules: List[PolicyRule] = Field(default=[], description="Extracted eligibility rules")
    description: Optional[str] = None
    benefits: Optional[str] = None


class InterpretPolicyRequest(BaseModel):
    """Request to interpret a policy text."""
    raw_text: str = Field(..., description="Raw policy text to interpret")
    policy_name: Optional[str] = Field(None, description="Optional name for the policy")


class InterpretPolicyResponse(BaseModel):
    """Response from policy interpretation."""
    policy: Policy
    message: str = "Policy interpreted successfully"


class CitizenCredential(BaseModel):
    """Represents a verifiable credential for a citizen."""
    type: str = Field(..., description="Credential type (e.g., 'income', 'residence', 'student')")
    data: Dict[str, Any] = Field(..., description="Credential data")
    issuer_did: str = Field(..., description="DID of the credential issuer")
    issued_at: datetime = Field(default_factory=datetime.utcnow)


class CitizenProfile(BaseModel):
    """Represents a citizen's profile with credentials."""
    citizen_id: Optional[str] = None
    name: Optional[str] = None
    income: Optional[float] = Field(None, description="Annual family income in INR")
    state: Optional[str] = Field(None, description="State of residence")
    is_student: Optional[bool] = Field(None, description="Whether the person is a student")
    credentials: List[CitizenCredential] = Field(default=[], description="Verifiable credentials")


class IssueCredentialRequest(BaseModel):
    """Request to issue a credential."""
    citizen_profile: CitizenProfile


class IssueCredentialResponse(BaseModel):
    """Response from credential issuance."""
    credentials: List[CitizenCredential]
    message: str = "Credentials issued successfully"


class EligibilityReason(BaseModel):
    """Reason for eligibility or ineligibility."""
    rule: PolicyRule
    satisfied: bool
    message: str


class EligibilityResult(BaseModel):
    """Result of eligibility verification for a policy."""
    policy_id: Optional[str] = None
    policy_name: str
    eligible: bool
    reasons: List[EligibilityReason] = Field(default=[])
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class BenefitMatch(BaseModel):
    """A matched benefit/policy for a citizen."""
    policy: Policy
    eligibility: EligibilityResult
    application_guidance: Optional[str] = None


class BenefitMatchResponse(BaseModel):
    """Response from benefit matching."""
    citizen_profile: CitizenProfile
    matched_benefits: List[BenefitMatch] = Field(default=[])
    total_matches: int = 0
    message: str = "Benefit matching completed"


class EligibilityCheckRequest(BaseModel):
    """Request to check eligibility."""
    citizen_profile: CitizenProfile
    policies: List[Policy] = Field(default=[], description="Policies to check against")


class AdvocacyRequest(BaseModel):
    """Request for application guidance."""
    policy_name: str
    citizen_profile: CitizenProfile


class AdvocacyResponse(BaseModel):
    """Response with application guidance."""
    policy_name: str
    guidance: str
    steps: List[str] = Field(default=[])