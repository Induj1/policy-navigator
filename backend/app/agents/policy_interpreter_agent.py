from typing import Dict, Any
from .base_agent import BaseAgent
from app.schemas import Policy, PolicyRule, OperatorEnum
import re


class PolicyInterpreterAgent(BaseAgent):
    """Agent responsible for interpreting natural language policy text into structured rules."""
    
    def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpret policy text and extract structured rules.
        
        Args:
            context: Dict with 'raw_text' (str) and 'policy_name' (str)
        
        Returns:
            Dict with 'policy' (Policy), 'rules_count' (int), or 'error'
        """
        try:
            raw_text: str = context.get("raw_text", "")
            policy_name: str = context.get("policy_name", "Untitled Policy")
            
            if not raw_text:
                return {"error": "raw_text is required"}
            
            # Extract rules using LLM if available, otherwise use regex
            if self.llm:
                rules = self._extract_rules_with_llm(raw_text)
            else:
                rules = self._extract_rules_with_regex(raw_text)
            
            policy = Policy(
                name=policy_name,
                raw_text=raw_text,
                rules=rules,
                description=self._extract_description(raw_text),
                benefits=self._extract_benefits(raw_text)
            )
            
            return {
                "policy": policy,
                "rules_count": len(rules)
            }
        
        except Exception as e:
            return {"error": f"Error interpreting policy: {str(e)}"}
    
    def _extract_rules_with_llm(self, raw_text: str) -> list[PolicyRule]:
        """Extract rules using LLM."""
        try:
            from langchain.prompts import ChatPromptTemplate
            from langchain.output_parsers import PydanticOutputParser
            
            # Create a prompt for rule extraction
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a policy analysis expert. Extract eligibility rules from policy text.
For each rule, identify:
- key: the attribute name (e.g., 'income', 'state', 'is_student', 'age')
- operator: comparison operator (==, !=, <, <=, >, >=)
- value: the threshold or required value

Common patterns:
- "below X" or "less than X" → use <= operator
- "above X" or "more than X" → use >= operator  
- "must be X" → use == operator
- "resident of X" → key='state', operator='==', value='X'
- "enrolled student" → key='is_student', operator='==', value=True

Return rules in JSON format: [{"key": "...", "operator": "...", "value": ...}]"""),
                ("user", "Policy text: {text}\n\nExtract eligibility rules:")
            ])
            
            chain = prompt | self.llm
            response = chain.invoke({"text": raw_text})
            
            # Parse the response to extract rules
            import json
            content = response.content
            
            # Try to extract JSON from the response
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                rules_data = json.loads(json_match.group())
                rules = []
                for rule_dict in rules_data:
                    # Map operator string to enum
                    op_str = rule_dict.get('operator', '==')
                    operator = self._map_operator(op_str)
                    
                    rules.append(PolicyRule(
                        key=rule_dict.get('key', ''),
                        operator=operator,
                        value=rule_dict.get('value')
                    ))
                return rules
            
            # Fallback to regex if LLM doesn't return proper JSON
            return self._extract_rules_with_regex(raw_text)
        
        except Exception:
            # Fallback to regex extraction
            return self._extract_rules_with_regex(raw_text)
    
    def _extract_rules_with_regex(self, raw_text: str) -> list[PolicyRule]:
        """Extract rules using regex patterns."""
        rules = []
        text_lower = raw_text.lower()
        
        # Pattern 1: income not exceed / must not exceed
        income_match = re.search(r'income\s+(?:must\s+)?(?:not\s+)?(?:exceed|exceeding?)\s+[₹$]?\s*(\d[\d,]+)', text_lower)
        if income_match:
            value = int(income_match.group(1).replace(',', ''))
            rules.append(PolicyRule(
                key="income",
                operator=OperatorEnum.LESS_THAN_OR_EQUAL,
                value=value
            ))
        
        # Pattern 2: income below/less than X
        if not income_match:
            income_match2 = re.search(r'income\s+(?:below|less\s+than|under)\s+[₹$]?\s*(\d[\d,]+)', text_lower)
            if income_match2:
                value = int(income_match2.group(1).replace(',', ''))
                rules.append(PolicyRule(
                    key="income",
                    operator=OperatorEnum.LESS_THAN_OR_EQUAL,
                    value=value
                ))
        
        # Pattern 3: permanent/resident of State
        state_match = re.search(r'(?:permanent\s+)?resident\s+of\s+(\w+)', text_lower)
        if state_match:
            rules.append(PolicyRule(
                key="state",
                operator=OperatorEnum.EQUAL,
                value=state_match.group(1).title()
            ))
        
        # Pattern 4: enrolled student / must be student
        if re.search(r'(?:enrolled|full-time)\s+student|must\s+be\s+(?:a\s+)?student', text_lower):
            rules.append(PolicyRule(
                key="is_student",
                operator=OperatorEnum.EQUAL,
                value=True
            ))
        
        # Pattern 5: disability percentage should be at least X / disability of at least X
        disability_match = re.search(r'disability\s+(?:percentage\s+)?(?:should\s+be|must\s+be|of)?\s*(?:at\s+least)\s+(\d+)\s*(?:percent|%)', text_lower)
        if disability_match:
            rules.append(PolicyRule(
                key="disability_percentage",
                operator=OperatorEnum.GREATER_THAN_OR_EQUAL,
                value=int(disability_match.group(1))
            ))
        
        # Pattern 6: age between X and Y
        age_range_match = re.search(r'age\s+(?:must\s+be\s+)?between\s+(\d+)\s+and\s+(\d+)', text_lower)
        if age_range_match:
            min_age = int(age_range_match.group(1))
            max_age = int(age_range_match.group(2))
            rules.append(PolicyRule(
                key="age",
                operator=OperatorEnum.GREATER_THAN_OR_EQUAL,
                value=min_age
            ))
            rules.append(PolicyRule(
                key="age",
                operator=OperatorEnum.LESS_THAN_OR_EQUAL,
                value=max_age
            ))
        else:
            # Pattern 7: minimum age / age at least X
            min_age_match = re.search(r'(?:minimum\s+age|age\s+(?:at\s+least|minimum|above)).*?(\d+)\s*years?', text_lower)
            if min_age_match:
                rules.append(PolicyRule(
                    key="age",
                    operator=OperatorEnum.GREATER_THAN_OR_EQUAL,
                    value=int(min_age_match.group(1))
                ))
            
            # Pattern 8: maximum age / age below X
            max_age_match = re.search(r'(?:maximum\s+age|age\s+(?:below|under|less\s+than|maximum)).*?(\d+)\s*years?', text_lower)
            if max_age_match:
                rules.append(PolicyRule(
                    key="age",
                    operator=OperatorEnum.LESS_THAN_OR_EQUAL,
                    value=int(max_age_match.group(1))
                ))
        
        # Pattern: age above/over X (without already matching minimum age)
        if not min_age_match:
            age_above = re.search(r'age\s+(?:above|over|greater\s+than)\s+(\d+)', text_lower)
            if age_above:
                rules.append(PolicyRule(
                    key="age",
                    operator=OperatorEnum.GREATER_THAN,
                    value=int(age_above.group(1))
                ))
        
        return rules
    
    def _map_operator(self, op_str: str) -> OperatorEnum:
        """Map operator string to OperatorEnum."""
        op_map = {
            "==": OperatorEnum.EQUAL,
            "=": OperatorEnum.EQUAL,
            "!=": OperatorEnum.NOT_EQUAL,
            "<": OperatorEnum.LESS_THAN,
            "<=": OperatorEnum.LESS_THAN_OR_EQUAL,
            ">": OperatorEnum.GREATER_THAN,
            ">=": OperatorEnum.GREATER_THAN_OR_EQUAL,
        }
        return op_map.get(op_str, OperatorEnum.EQUAL)
    
    def _extract_description(self, raw_text: str) -> str:
        """Extract a brief description from policy text."""
        # Take first sentence or up to 200 characters
        sentences = raw_text.split('.')
        if sentences:
            return sentences[0].strip() + '.'
        return raw_text[:200]
    
    def _extract_benefits(self, raw_text: str) -> str:
        """Extract benefits information from policy text."""
        text_lower = raw_text.lower()
        
        # Look for benefit amount patterns
        benefit_match = re.search(r'(?:scholarship|subsidy|benefit|assistance).*?(\d+(?:,\d+)*)\s*(?:inr|rupees)', text_lower)
        if benefit_match:
            return f"Financial assistance up to {benefit_match.group(1)} INR"
        
        # Generic benefit extraction
        if 'scholarship' in text_lower:
            return "Education scholarship"
        elif 'subsidy' in text_lower:
            return "Financial subsidy"
        elif 'assistance' in text_lower:
            return "Financial assistance"
        
        return "Government benefit program"


# Global instance
policy_interpreter_agent = PolicyInterpreterAgent()