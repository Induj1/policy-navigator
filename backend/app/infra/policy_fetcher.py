"""
Policy Fetcher - Dynamically fetches policies from ZyndAI network
Falls back to hardcoded policies if network unavailable
"""
from typing import List, Optional
from app.schemas import Policy, PolicyRule, OperatorEnum
from app.infra.p3ai_client import get_p3ai_client
import json
import time


class PolicyFetcher:
    """Fetches policies from real government agents on ZyndAI network."""
    
    def __init__(self):
        self.client = get_p3ai_client()
        self.cached_policies = []
        self.connected_policy_agents = []
    
    def discover_policy_agents(self) -> List[dict]:
        """
        Search ZyndAI network for government policy agents.
        
        Returns:
            List of policy-serving agents
        """
        if not self.client.is_p3ai_available():
            print("⚠ ZyndAI not connected - using hardcoded policies")
            return []
        
        try:
            # Search for government policy agents
            policy_agents = self.client.search_agents(
                capabilities=[
                    "government_policy",
                    "policy_database",
                    "benefit_schemes",
                    "eligibility_rules"
                ],
                match_score_gte=0.7,
                top_k=10
            )
            
            print(f"✓ Found {len(policy_agents)} policy agents on ZyndAI network:")
            for agent in policy_agents:
                print(f"  - {agent.get('name')} (match: {agent.get('matchScore', 0):.2f})")
            
            self.connected_policy_agents = policy_agents
            return policy_agents
        
        except Exception as e:
            print(f"Error discovering policy agents: {e}")
            return []
    
    def fetch_policies_from_agent(self, agent_info: dict) -> List[Policy]:
        """
        Connect to a policy agent and fetch their policies.
        
        Args:
            agent_info: Agent information from search results
        
        Returns:
            List of Policy objects
        """
        if not self.client.is_p3ai_available():
            return []
        
        try:
            # Connect to the policy agent
            connected = self.client.connect_to_agent(agent_info)
            if not connected:
                return []
            
            # Request policy list
            response = self.client.send_message(
                message=json.dumps({
                    "action": "list_policies",
                    "filters": {
                        "active": True,
                        "year": 2024
                    }
                }),
                message_type="query"
            )
            
            print(f"✓ Sent request to {agent_info.get('name')}")
            
            # Wait for and read the response
            time.sleep(2)  # Give time for response
            
            messages = self.client.read_messages()
            
            if messages and "No new messages" not in messages:
                # Parse the policy data
                try:
                    policy_data = json.loads(messages)
                    
                    policies = []
                    for p_dict in policy_data.get("policies", []):
                        # Convert to Policy schema
                        policy = Policy(
                            name=p_dict.get("name"),
                            raw_text=p_dict.get("raw_text", ""),
                            description=p_dict.get("description"),
                            rules=[
                                PolicyRule(
                                    key=rule.get("key"),
                                    operator=OperatorEnum(rule.get("operator")),
                                    value=rule.get("value")
                                )
                                for rule in p_dict.get("rules", [])
                            ],
                            benefits=p_dict.get("benefits")
                        )
                        policies.append(policy)
                    
                    self.cached_policies.extend(policies)
                    print(f"✓ Received {len(policies)} policies from {agent_info.get('name')}")
                    return policies
                
                except json.JSONDecodeError:
                    print(f"⚠ Could not parse response from {agent_info.get('name')}")
                    return []
        
        except Exception as e:
            print(f"Error fetching policies from agent: {e}")
            return []
        
        return []
    
    def fetch_all_policies(self) -> List[Policy]:
        """
        Discover and fetch policies from all available policy agents.
        
        Returns:
            Combined list of policies from all agents
        """
        if not self.client.is_p3ai_available():
            print("⚠ ZyndAI not connected - returning hardcoded policies")
            return self._get_hardcoded_policies()
        
        # Discover policy agents
        agents = self.discover_policy_agents()
        
        if not agents:
            print("⚠ No policy agents found - using hardcoded policies")
            return self._get_hardcoded_policies()
        
        # Fetch from each agent
        all_policies = []
        for agent in agents:
            policies = self.fetch_policies_from_agent(agent)
            all_policies.extend(policies)
        
        if all_policies:
            print(f"✓ Fetched {len(all_policies)} policies from {len(agents)} agents")
            return all_policies
        else:
            print("⚠ No policies received from network - using hardcoded policies")
            return self._get_hardcoded_policies()
    
    def fetch_policies_by_state(self, state: str) -> List[Policy]:
        """
        Fetch policies specific to a state.
        
        Args:
            state: State name (e.g., "Karnataka", "Maharashtra")
        
        Returns:
            List of state-specific policies
        """
        if not self.client.is_p3ai_available():
            return [p for p in self._get_hardcoded_policies() 
                   if any(r.key == "state" and r.value == state for r in p.rules)]
        
        try:
            # Search for state-specific policy agents
            state_agents = self.client.search_agents(
                capabilities=[
                    f"{state}_government",
                    "state_policy",
                    "regional_benefits"
                ],
                match_score_gte=0.6,
                top_k=5
            )
            
            policies = []
            for agent in state_agents:
                agent_policies = self.fetch_policies_from_agent(agent)
                policies.extend(agent_policies)
            
            if policies:
                print(f"✓ Found {len(policies)} policies for {state}")
                return policies
            else:
                print(f"⚠ No {state} policies found on network - using hardcoded")
                return [p for p in self._get_hardcoded_policies() 
                       if any(r.key == "state" and r.value == state for r in p.rules)]
        
        except Exception as e:
            print(f"Error fetching state policies: {e}")
            return [p for p in self._get_hardcoded_policies() 
                   if any(r.key == "state" and r.value == state for r in p.rules)]
    
    def _get_hardcoded_policies(self) -> List[Policy]:
        """Fallback hardcoded policies (same as current implementation)."""
        return [
            Policy(
                name="Karnataka Education Scholarship",
                raw_text="Students from Karnataka with family income below 800000 INR are eligible for education scholarship",
                description="Financial assistance for students from low-income families in Karnataka",
                rules=[
                    PolicyRule(key="state", operator=OperatorEnum.EQUAL, value="Karnataka"),
                    PolicyRule(key="income", operator=OperatorEnum.LESS_THAN_OR_EQUAL, value=800000),
                    PolicyRule(key="is_student", operator=OperatorEnum.EQUAL, value=True)
                ],
                benefits="Education scholarship up to 50000 INR per year"
            ),
            Policy(
                name="Low Income Housing Subsidy",
                raw_text="Families with annual income below 500000 INR are eligible for housing subsidy",
                description="Government assistance for low-income families to purchase or build homes",
                rules=[
                    PolicyRule(key="income", operator=OperatorEnum.LESS_THAN_OR_EQUAL, value=500000)
                ],
                benefits="Housing subsidy up to 200000 INR"
            ),
            Policy(
                name="General Student Welfare Scheme",
                raw_text="All enrolled students are eligible for student welfare benefits",
                description="General welfare scheme for all students",
                rules=[
                    PolicyRule(key="is_student", operator=OperatorEnum.EQUAL, value=True)
                ],
                benefits="Access to student welfare programs and resources"
            ),
            Policy(
                name="Maharashtra Disability Support",
                raw_text="Citizens of Maharashtra with disability of at least 40 percent and minimum age 21 years are eligible",
                description="Support scheme for persons with disabilities in Maharashtra",
                rules=[
                    PolicyRule(key="state", operator=OperatorEnum.EQUAL, value="Maharashtra"),
                    PolicyRule(key="disability_percentage", operator=OperatorEnum.GREATER_THAN_OR_EQUAL, value=40),
                    PolicyRule(key="age", operator=OperatorEnum.GREATER_THAN_OR_EQUAL, value=21)
                ],
                benefits="Monthly disability pension and healthcare support"
            )
        ]
    
    def clear_cache(self):
        """Clear cached policies to force fresh fetch."""
        self.cached_policies = []
        self.connected_policy_agents = []


# Singleton instance
_fetcher_instance: Optional[PolicyFetcher] = None


def get_policy_fetcher() -> PolicyFetcher:
    """Get or create the singleton PolicyFetcher instance."""
    global _fetcher_instance
    
    if _fetcher_instance is None:
        _fetcher_instance = PolicyFetcher()
    
    return _fetcher_instance
