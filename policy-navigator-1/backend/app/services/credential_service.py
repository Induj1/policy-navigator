from typing import List, Dict
from pydantic import BaseModel, ValidationError

class CitizenCredential(BaseModel):
    citizen_id: str
    name: str
    age: int
    income: float
    state: str

class CredentialService:
    def __init__(self):
        self.credentials: List[CitizenCredential] = []

    def add_credential(self, credential_data: Dict) -> CitizenCredential:
        try:
            credential = CitizenCredential(**credential_data)
            self.credentials.append(credential)
            return credential
        except ValidationError as e:
            raise ValueError(f"Invalid credential data: {e}")

    def get_credentials(self) -> List[CitizenCredential]:
        return self.credentials

    def find_credential(self, citizen_id: str) -> CitizenCredential:
        for credential in self.credentials:
            if credential.citizen_id == citizen_id:
                return credential
        raise ValueError("Credential not found")