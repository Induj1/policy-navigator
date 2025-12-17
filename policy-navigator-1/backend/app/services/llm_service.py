from typing import Any, Dict
import openai

class LLMService:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def query_model(self, prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 150) -> Dict[str, Any]:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message['content']

    def interpret_policy(self, policy_text: str) -> Dict[str, Any]:
        prompt = f"Interpret the following policy text and extract the key rules: {policy_text}"
        interpretation = self.query_model(prompt)
        return {"interpretation": interpretation}

    def verify_eligibility(self, credentials: Dict[str, Any], policy_rules: str) -> Dict[str, Any]:
        prompt = f"Given the following credentials: {credentials} and policy rules: {policy_rules}, determine eligibility."
        eligibility_result = self.query_model(prompt)
        return {"eligibility": eligibility_result}

    def match_benefits(self, citizen_data: Dict[str, Any], policies: str) -> Dict[str, Any]:
        prompt = f"Match the following citizen data: {citizen_data} with these policies: {policies}."
        matched_benefits = self.query_model(prompt)
        return {"matched_benefits": matched_benefits}