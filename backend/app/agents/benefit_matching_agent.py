from typing import Dict, Any
from .base_agent import BaseAgent
from .eligibility_agent import EligibilityAgent
from app.schemas import CitizenProfile, Policy, BenefitMatch, BenefitMatchResponse

class BenefitMatchingAgent(BaseAgent):
    """Agent responsible for matching citizens with eligible benefits/policies."""
    
    def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Match a citizen profile against multiple policies.
        
        Args:
            context: Dict with 'citizen_profile' (CitizenProfile) and 'policies' (List[Policy])
        
        Returns:
            Dict with 'response' (BenefitMatchResponse) or 'error'
        """
        try:
            citizen_profile: CitizenProfile = context.get("citizen_profile")
            policies: list[Policy] = context.get("policies", [])
            
            if not citizen_profile:
                return {"error": "citizen_profile is required"}
            
            # If no policies provided, get sample policies
            if not policies:
                policies = self._get_sample_policies()
            
            # Check eligibility for each policy
            eligibility_agent = EligibilityAgent(llm=self.llm)
            matched_benefits = []
            
            for policy in policies:
                # Check eligibility
                eligibility_result = eligibility_agent.handle({
                    "citizen_profile": citizen_profile,
                    "policy": policy
                })
                
                if "error" in eligibility_result:
                    continue
                
                eligibility = eligibility_result["result"]
                
                # If eligible, add to matches
                if eligibility.eligible:
                    # Get application guidance if LLM is available
                    guidance = None
                    if self.llm:
                        guidance = self._generate_guidance(policy, citizen_profile)
                    
                    benefit_match = BenefitMatch(
                        policy=policy,
                        eligibility=eligibility,
                        application_guidance=guidance
                    )
                    matched_benefits.append(benefit_match)
            
            response = BenefitMatchResponse(
                citizen_profile=citizen_profile,
                matched_benefits=matched_benefits,
                total_matches=len(matched_benefits),
                message=f"Found {len(matched_benefits)} matching benefit(s)"
            )
            
            return {"response": response}
        
        except Exception as e:
            return {"error": f"Error matching benefits: {str(e)}"}
    
    def _get_sample_policies(self) -> list[Policy]:
        """Get sample policies for matching."""
        from app.infra.policy_fetcher import get_policy_fetcher
        
        # Use PolicyFetcher to get policies (tries network, falls back to hardcoded)
        fetcher = get_policy_fetcher()
        return fetcher.fetch_all_policies()
    
    def _generate_guidance(self, policy: Policy, citizen_profile: CitizenProfile) -> str:
        """Generate application guidance using LLM."""
        if not self.llm:
            return f"To apply for {policy.name}, please visit your local government office."
        
        try:
            from langchain.prompts import ChatPromptTemplate
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful government benefits advisor. Provide clear, step-by-step guidance for citizens applying for government benefits."),
                ("user", f"Policy: {policy.name}\nDescription: {policy.description}\nBenefits: {policy.benefits}\n\nProvide a brief 2-3 sentence guidance on how to apply for this benefit.")
            ])
            
            chain = prompt | self.llm
            response = chain.invoke({})
            return response.content
        
        except Exception:
            return f"To apply for {policy.name}, please contact your local government office for application procedures."