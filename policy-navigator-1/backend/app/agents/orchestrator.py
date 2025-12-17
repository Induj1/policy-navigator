from .policy_interpreter import PolicyInterpreterAgent
from .eligibility_verifier import EligibilityAgent
from .benefit_matcher import BenefitMatchingAgent

class OrchestratorAgent:
    def __init__(self):
        self.policy_interpreter = PolicyInterpreterAgent()
        self.eligibility_verifier = EligibilityAgent()
        self.benefit_matcher = BenefitMatchingAgent()

    def process_request(self, raw_policy_text, citizen_credentials):
        structured_rules = self.policy_interpreter.handle(raw_policy_text)
        eligibility_results = self.eligibility_verifier.handle(citizen_credentials, structured_rules)
        benefits = self.benefit_matcher.handle(eligibility_results)

        return {
            "structured_rules": structured_rules,
            "eligibility_results": eligibility_results,
            "benefits": benefits
        }