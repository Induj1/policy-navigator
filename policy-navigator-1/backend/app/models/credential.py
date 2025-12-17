from pydantic import BaseModel
from typing import List, Optional

class CitizenCredential(BaseModel):
    citizen_id: str
    name: str
    date_of_birth: str
    address: str
    income: Optional[float] = None
    state: str
    verified: bool = False

class VerifiableCredential(BaseModel):
    credential: CitizenCredential
    issued_at: str
    expires_at: str
    issuer: str
    proof: Optional[dict] = None

class CredentialResponse(BaseModel):
    success: bool
    message: str
    credential: Optional[VerifiableCredential] = None