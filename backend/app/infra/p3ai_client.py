"""
P3AI Client - Connects to Real P3AI Network
Handles P3AI agent initialization, LLM setup, and network communication
"""
from typing import Optional
import os
from pathlib import Path


class P3AIClient:
    """Client for managing P3AI agent and LLM connections."""
    
    def __init__(self):
        self.agent = None
        self.llm = None
        self.is_connected = False
        self._initialize()
    
    def _initialize(self):
        """Initialize P3AI agent and LLM."""
        # Try to initialize P3AI agent
        try:
            from zyndai_agent.agent import ZyndAIAgent, AgentConfig
            
            # Look for identity credential file in multiple locations
            identity_paths = [
                Path("identity_credential.json"),
                Path("backend/identity_credential.json"),
                Path("../identity_credential.json"),
            ]
            
            identity_path = None
            for path in identity_paths:
                if path.exists():
                    identity_path = path
                    break
            
            secret_seed = os.getenv("AGENT_SEED") or os.getenv("AGENT_SECRET_SEED")
            
            if identity_path and secret_seed:
                # Configure agent to connect to real P3AI network
                agent_config = AgentConfig(
                    default_outbox_topic=None,  # Auto-connect to other agents
                    auto_reconnect=True,
                    message_history_limit=100,
                    registry_url="https://registry.zynd.ai",  # Production registry
                    mqtt_broker_url="mqtt://registry.zynd.ai:1883",  # Production MQTT
                    identity_credential_path=str(identity_path.absolute()),
                    secret_seed=secret_seed
                )
                
                # Initialize ZyndAI agent
                self.agent = ZyndAIAgent(agent_config=agent_config)
                self.is_connected = True
                
                print("=" * 60)
                print("✓ P3AI Agent Connected to Real Network")
                print(f"  Identity File: {identity_path}")
                print(f"  Registry: {agent_config.registry_url}")
                print(f"  MQTT Broker: {agent_config.mqtt_broker_url}")
                
                # Get agent identity
                try:
                    identity = self.agent.get_identity_document()
                    if identity:
                        print(f"  Agent DID: {identity.get('didIdentifier', 'N/A')[:50]}...")
                except:
                    pass
                
                print("=" * 60)
            else:
                print("=" * 60)
                print("⚠ P3AI Agent - Running in Simulation Mode")
                print("  To connect to real ZyndAI network:")
                print("  1. Visit https://dashboard.zynd.ai")
                print("  2. Create an agent and download identity_credential.json")
                print("  3. Copy your secret_seed from the dashboard")
                print("  4. Add to .env: AGENT_SEED=your_secret_seed")
                print("  5. Place identity_credential.json in project root")
                
                if not identity_path:
                    print("  ❌ Missing: identity_credential.json file")
                if not secret_seed:
                    print("  ❌ Missing: AGENT_SEED in .env")
                print("=" * 60)
        
        except ImportError:
            print("⚠ zyndai-agent package not found. Install: pip install zyndai-agent")
        except Exception as e:
            print(f"⚠ Could not initialize P3AI agent: {e}")
            print("  Running in simulation mode")
        
        # Initialize LLM (works with or without P3AI)
        try:
            from langchain_openai import ChatOpenAI
            
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                # Try GPT-3.5-turbo first (cheaper, higher rate limits)
                try:
                    self.llm = ChatOpenAI(
                        model="gpt-3.5-turbo",
                        temperature=0,
                        api_key=openai_key,
                        request_timeout=30,
                        max_retries=2
                    )
                    
                    # Test the API key with a simple call
                    print("🔑 Testing OpenAI API key...")
                    test_response = self.llm.invoke("Hi")
                    
                    # If we have a P3AI agent, set the LLM executor
                    if self.agent and self.is_connected:
                        try:
                            self.agent.set_agent_executor(self.llm)
                            print("✓ LLM (GPT-3.5-turbo) connected to P3AI agent")
                        except Exception as e:
                            print(f"⚠ Could not connect LLM to agent: {e}")
                    else:
                        print("✓ LLM (GPT-3.5-turbo) initialized (standalone mode)")
                    
                except Exception as api_error:
                    print(f"❌ OpenAI API Error: {api_error}")
                    if "429" in str(api_error):
                        print("  → Rate limit exceeded or insufficient credits")
                        print("  → Check your OpenAI account at: https://platform.openai.com/account/billing")
                    elif "401" in str(api_error):
                        print("  → Invalid API key")
                        print("  → Get a valid key at: https://platform.openai.com/api-keys")
                    print("  → LLM features will be disabled")
                    self.llm = None
            else:
                print("⚠ OPENAI_API_KEY not set - LLM features disabled")
                print("  Add to .env: OPENAI_API_KEY=your_openai_api_key")
        
        except ImportError:
            print("⚠ langchain-openai package not found. Install: pip install langchain-openai")
        except Exception as e:
            print(f"⚠ Could not initialize LLM: {e}")
    
    def get_agent(self) -> Optional[any]:
        """Get the P3AI agent instance."""
        return self.agent
    
    def get_llm(self) -> Optional[any]:
        """Get the LLM instance."""
        return self.llm
    
    def is_p3ai_available(self) -> bool:
        """Check if P3AI agent is connected to real network."""
        return self.agent is not None and self.is_connected
    
    def is_llm_available(self) -> bool:
        """Check if LLM is available."""
        return self.llm is not None
    
    def search_agents(self, capabilities: list[str], match_score_gte: float = 0.7, top_k: int = 5):
        """
        Search for agents on P3AI network by capabilities.
        
        Args:
            capabilities: List of capability keywords (e.g., ["nlp", "data_analysis"])
            match_score_gte: Minimum similarity score (0-1)
            top_k: Maximum number of results
        
        Returns:
            List of agent information dictionaries
        """
        if not self.is_p3ai_available():
            print("⚠ P3AI agent not connected. Cannot search network.")
            return []
        
        try:
            agents = self.agent.search_agents_by_capabilities(
                capabilities=capabilities,
                match_score_gte=match_score_gte,
                top_k=top_k
            )
            return agents
        except Exception as e:
            print(f"Error searching agents: {e}")
            return []
    
    def connect_to_agent(self, agent_info: dict) -> bool:
        """
        Connect to another agent on the P3AI network.
        
        Args:
            agent_info: Agent information from search results
        
        Returns:
            True if connection successful
        """
        if not self.is_p3ai_available():
            print("⚠ P3AI agent not connected.")
            return False
        
        try:
            self.agent.connect_agent(agent_info)
            print(f"✓ Connected to agent: {agent_info.get('name', 'Unknown')}")
            return True
        except Exception as e:
            print(f"Error connecting to agent: {e}")
            return False
    
    def send_message(self, message: str, message_type: str = "query") -> str:
        """
        Send encrypted message to connected agent.
        
        Args:
            message: Message content
            message_type: Type of message (query, response, greeting, etc.)
        
        Returns:
            Result message
        """
        if not self.is_p3ai_available():
            return "P3AI agent not connected"
        
        try:
            result = self.agent.send_message(
                message_content=message,
                message_type=message_type
            )
            return result
        except Exception as e:
            return f"Error sending message: {e}"
    
    def read_messages(self) -> str:
        """Read incoming encrypted messages from other agents."""
        if not self.is_p3ai_available():
            return "P3AI agent not connected"
        
        try:
            messages = self.agent.read_messages()
            return messages
        except Exception as e:
            return f"Error reading messages: {e}"
    
    def get_connection_status(self) -> dict:
        """Get current P3AI connection status with detailed information."""
        status = {
            "connected": self.is_p3ai_available(),
            "mode": "Real Network" if self.is_connected else "Simulation",
            "llm_available": self.is_llm_available(),
        }
        
        # Add network details if connected
        if self.agent and self.is_connected:
            try:
                status["registry_url"] = "https://registry.zynd.ai"
                status["mqtt_broker"] = "registry.zynd.ai:1883"
                status["agent_did"] = getattr(self.agent, 'did', 'Unknown')
                status["identity_verified"] = True
            except Exception as e:
                status["error"] = str(e)
        
        return status


# Singleton instance
_client_instance: Optional[P3AIClient] = None


def get_p3ai_client() -> P3AIClient:
    """Get or create the singleton P3AI client instance."""
    global _client_instance
    
    if _client_instance is None:
        _client_instance = P3AIClient()
    
    return _client_instance
