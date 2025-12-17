import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Try to import P3AI, but continue without it if unavailable
try:
    from p3ai_agent.agent import P3AIAgent, AgentConfig
    P3AI_AVAILABLE = True
except ImportError:
    P3AI_AVAILABLE = False
    print("⚠ P3AI agent not available, running in simulation mode")


class P3AIClient:
    """Client for interacting with P3AI/Zynd protocol."""
    
    def __init__(self):
        self.identity_path = os.getenv("P3AI_IDENTITY_PATH", "./identity.json")
        self.network = os.getenv("P3AI_NETWORK", "testnet")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.agent: Optional[Any] = None
        self.llm: Optional[ChatOpenAI] = None
        
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the P3AI agent and LLM."""
        try:
            # Initialize LLM
            if self.openai_api_key:
                self.llm = ChatOpenAI(
                    model="gpt-4",
                    temperature=0.7,
                    openai_api_key=self.openai_api_key
                )
            
            # Initialize P3AI Agent if available
            if P3AI_AVAILABLE and os.path.exists(self.identity_path):
                config = AgentConfig(
                    identity_path=self.identity_path,
                    network=self.network
                )
                self.agent = P3AIAgent(config=config)
                print(f"✓ P3AI Agent initialized with identity from {self.identity_path}")
            else:
                if not P3AI_AVAILABLE:
                    print(f"⚠ P3AI not available. Agent features will be simulated.")
                else:
                    print(f"⚠ Identity file not found at {self.identity_path}. Agent features will be limited.")
        
        except Exception as e:
            print(f"⚠ Error initializing P3AI client: {e}")
    
    def get_identity(self) -> Optional[Dict[str, Any]]:
        """Get the current agent's identity information."""
        if not self.agent:
            return {
                "did": "did:p3:simulated:agent",
                "status": "simulated",
                "message": "Running in simulation mode"
            }
        
        try:
            identity = self.agent.get_identity()
            return {
                "did": identity.get("did"),
                "public_key": identity.get("public_key"),
                "network": self.network
            }
        except Exception as e:
            print(f"Error getting identity: {e}")
            return None
    
    def search_agents(self, query: str, agent_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for other agents on the P3AI network."""
        if not self.agent:
            return [
                {
                    "did": "did:p3:gov:karnataka:revenue",
                    "name": "Karnataka Revenue Department",
                    "type": "credential_issuer",
                    "capabilities": ["income_verification"]
                }
            ]
        
        try:
            results = self.agent.search(query=query, agent_type=agent_type)
            return results
        except Exception as e:
            print(f"Error searching agents: {e}")
            return []
    
    def send_message(
        self,
        recipient_did: str,
        message: Dict[str, Any],
        message_type: str = "request"
    ) -> Optional[Dict[str, Any]]:
        """Send a message to another agent."""
        if not self.agent:
            print(f"Simulated message to {recipient_did}: {message}")
            return {
                "status": "simulated",
                "message": "Message sent in simulation mode",
                "recipient": recipient_did
            }
        
        try:
            response = self.agent.send_message(
                recipient=recipient_did,
                content=message,
                message_type=message_type
            )
            return response
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def get_llm(self) -> Optional[ChatOpenAI]:
        """Get the initialized LLM instance."""
        return self.llm
    
    def is_available(self) -> bool:
        """Check if P3AI agent is available and operational."""
        return self.agent is not None


# Global singleton instance
_p3ai_client: Optional[P3AIClient] = None


def get_p3ai_client() -> P3AIClient:
    """Get or create the P3AI client singleton."""
    global _p3ai_client
    if _p3ai_client is None:
        _p3ai_client = P3AIClient()
    return _p3ai_client