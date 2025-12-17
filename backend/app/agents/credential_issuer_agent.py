from typing import Dict, Any, List
from .base_agent import BaseAgent
from app.schemas import CitizenProfile, CitizenCredential
from datetime import datetime
import uuid


class CredentialIssuerAgent(BaseAgent):
    """Agent responsible for issuing verifiable credentials to citizens."""
    
    def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Issue credentials based on citizen profile.
        
        Args:
            context: Dict with 'citizen_profile' (CitizenProfile)
        
        Returns:
            Dict with 'credentials' (List[CitizenCredential]) or 'error'
        """
        try:
            citizen_profile: CitizenProfile = context.get("citizen_profile")
            
            if not citizen_profile:
                return {"error": "citizen_profile is required"}
            
            credentials = []
            
            # Issue income credential if income is provided
            if citizen_profile.income is not None:
                income_cred = CitizenCredential(
                    type="income_verification",
                    data={
                        "income": citizen_profile.income,
                        "verified": True
                    },
                    issuer_did=self._get_issuer_did()
                )
                credentials.append(income_cred)
            
            # Issue residence credential if state is provided
            if citizen_profile.state:
                residence_cred = CitizenCredential(
                    type="residence_proof",
                    data={
                        "state": citizen_profile.state,
                        "verified": True
                    },
                    issuer_did=self._get_issuer_did()
                )
                credentials.append(residence_cred)
            
            # Issue student credential if student status is provided
            if citizen_profile.is_student is not None:
                student_cred = CitizenCredential(
                    type="student_status",
                    data={
                        "is_student": citizen_profile.is_student,
                        "verified": True
                    },
                    issuer_did=self._get_issuer_did()
                )
                credentials.append(student_cred)
            
            return {"credentials": credentials}
        
        except Exception as e:
            return {"error": f"Error issuing credentials: {str(e)}"}
    
    def _get_issuer_did(self) -> str:
        """Generate or retrieve the issuer DID."""
        # In a real implementation, this would use the P3AI agent's DID
        # For simulation, we generate a unique identifier
        return f"did:p3ai:issuer:{uuid.uuid4()}"