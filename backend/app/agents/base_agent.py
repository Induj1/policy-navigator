from abc import ABC, abstractmethod
from typing import Optional, Any

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, llm: Optional[Any] = None):
        """
        Initialize the base agent.
        
        Args:
            llm: Optional language model for AI-powered operations
        """
        self.llm = llm
    
    @abstractmethod
    def handle(self, *args, **kwargs):
        """
        Handle the agent's primary operation.
        Must be implemented by subclasses.
        """
        pass