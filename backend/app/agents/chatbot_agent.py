"""
Chatbot Agent - Handles conversational interactions
"""

from typing import List, Dict, Optional
from datetime import datetime
import json

from app.agents.base_agent import BaseAgent
from app.infra.p3ai_client import get_p3ai_client


class ChatMessage:
    """Represents a single chat message"""
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.role = role  # 'user' or 'assistant'
        self.content = content
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }


class ConversationSession:
    """Manages a conversation session with history"""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[ChatMessage] = []
        self.created_at = datetime.now()
        self.context = {}
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation"""
        self.messages.append(ChatMessage(role, content))
    
    def get_history(self, last_n: int = 10) -> List[Dict]:
        """Get last N messages"""
        return [msg.to_dict() for msg in self.messages[-last_n:]]
    
    def clear_history(self):
        """Clear conversation history"""
        self.messages = []


class ChatbotAgent(BaseAgent):
    """Agent that handles conversational interactions"""
    
    def __init__(self):
        super().__init__(llm=None)
        self.name = "Chatbot Agent"
        self.description = "Handles natural language conversations about policies and eligibility"
        self.sessions: Dict[str, ConversationSession] = {}
        self.system_prompt = """You are a helpful AI assistant for the Policy Navigator system. 
You help citizens understand government policies, check eligibility, and find benefits.

Your capabilities:
1. Answer questions about policies and eligibility criteria
2. Guide users through the eligibility checking process
3. Explain policy terms in simple language
4. Suggest relevant policies based on user profile
5. Provide step-by-step instructions

Always be:
- Clear and concise
- Empathetic and supportive
- Accurate with policy information
- Helpful in guiding users to the right features

If asked about specific eligibility, guide users to use the "Check Eligibility" feature.
If asked to interpret a policy, guide them to the "Understand Policies" feature.
"""
    
    def get_session(self, session_id: str) -> ConversationSession:
        """Get or create a conversation session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationSession(session_id)
        return self.sessions[session_id]
    
    async def chat(
        self,
        message: str,
        session_id: str,
        user_context: Optional[Dict] = None
    ) -> Dict:
        """
        Process a chat message and generate a response
        
        Args:
            message: User's message
            session_id: Unique session identifier
            user_context: Optional context about the user (profile, preferences)
        
        Returns:
            Dictionary with response and metadata
        """
        try:
            session = self.get_session(session_id)
            session.add_message("user", message)
            
            # Build context from conversation history
            history = session.get_history(last_n=5)
            
            # Add user context if available
            context_info = ""
            if user_context:
                context_info = f"\n\nUser Context: {json.dumps(user_context, indent=2)}"
            
            # Build prompt with history
            conversation_context = "\n".join([
                f"{msg['role'].title()}: {msg['content']}"
                for msg in history[:-1]  # Exclude the current message
            ])
            
            prompt = f"""{self.system_prompt}

Previous conversation:
{conversation_context}

{context_info}

User: {message}

Provide a helpful, concise response:"""
            
            # Get response from LLM
            p3ai_client = get_p3ai_client()
            
            if p3ai_client and p3ai_client.llm:
                response = await p3ai_client.llm.ainvoke(prompt)
                response_text = response.content if hasattr(response, 'content') else str(response)
            else:
                # Fallback response without LLM
                response_text = await self._generate_fallback_response(message, user_context)
            
            # Add assistant response to session
            session.add_message("assistant", response_text)
            
            return {
                "success": True,
                "response": response_text,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "message_count": len(session.messages)
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": "I apologize, but I encountered an error. Please try again or use the menu to navigate to specific features.",
                "error": str(e),
                "session_id": session_id
            }
    
    async def _generate_fallback_response(
        self,
        message: str,
        user_context: Optional[Dict]
    ) -> str:
        """Generate a response without LLM (fallback)"""
        message_lower = message.lower()
        
        # Simple keyword-based responses
        if any(word in message_lower for word in ["hello", "hi", "hey", "start"]):
            return """Hello! 👋 Welcome to Policy Navigator. I'm here to help you discover government benefits and check your eligibility.

I can help you:
• Check eligibility for policies
• Understand policy requirements
• Find benefits you qualify for
• Answer questions about government schemes

What would you like to know?"""
        
        elif any(word in message_lower for word in ["eligibility", "eligible", "qualify"]):
            return """To check your eligibility for government benefits:

1. Click on "Check Eligibility" in the menu
2. Fill in your details (income, age, state, etc.)
3. Submit the form
4. Get instant results showing which policies you qualify for

Would you like me to guide you through any specific step?"""
        
        elif any(word in message_lower for word in ["policy", "policies", "scheme", "schemes"]):
            return """To understand government policies:

1. Go to "Understand Policies" page
2. Paste or upload a policy document
3. Our AI will extract eligibility criteria and benefits
4. View the structured information

You can also browse all available benefits on the "Browse Benefits" page.

What policy are you interested in?"""
        
        elif any(word in message_lower for word in ["upload", "document", "file", "pdf"]):
            return """You can upload policy documents in multiple formats:

Supported formats:
• PDF files (.pdf)
• Images (.jpg, .png)
• Word documents (.docx)

Just go to the "Understand Policies" page and use the upload button. Our AI will extract the text and interpret the policy for you.

Need help with a specific document?"""
        
        elif any(word in message_lower for word in ["language", "translate", "hindi", "marathi"]):
            return """Policy Navigator supports multiple Indian languages! 🌏

Available languages:
• English, हिंदी (Hindi)
• मराठी (Marathi), தமிழ் (Tamil)
• తెలుగు (Telugu), ಕನ್ನಡ (Kannada)
• ગુજરાતી (Gujarati), বাংলা (Bengali)
• And more!

Use the language selector in the menu to switch languages.

Which language would you prefer?"""
        
        elif any(word in message_lower for word in ["help", "how", "guide"]):
            return """I'm here to help! Here's what I can assist with:

📋 **Features:**
• Check Eligibility - See which benefits you qualify for
• Understand Policies - Interpret policy documents
• Browse Benefits - Explore all available schemes

💬 **Ask me about:**
• Specific policies and their requirements
• How to check eligibility
• Uploading documents
• Language support
• Navigation help

What would you like to know more about?"""
        
        else:
            return """I'd be happy to help! Could you please provide more details about:

• Are you looking for information about a specific policy?
• Do you want to check your eligibility?
• Need help uploading a document?
• Want to know about available benefits?

Use the menu to navigate to specific features, or ask me a question!"""
    
    async def get_quick_actions(self, user_context: Optional[Dict] = None) -> List[Dict]:
        """Get quick action suggestions based on context"""
        actions = [
            {
                "id": "check_eligibility",
                "label": "Check My Eligibility",
                "icon": "✓",
                "description": "Find out which benefits you qualify for"
            },
            {
                "id": "understand_policy",
                "label": "Understand a Policy",
                "icon": "📄",
                "description": "Upload or paste a policy document"
            },
            {
                "id": "browse_benefits",
                "label": "Browse All Benefits",
                "icon": "🔍",
                "description": "Explore available government schemes"
            },
            {
                "id": "upload_document",
                "label": "Upload Document",
                "icon": "📤",
                "description": "Upload PDF or image for analysis"
            }
        ]
        
        return actions
    
    async def clear_session(self, session_id: str) -> bool:
        """Clear a conversation session"""
        if session_id in self.sessions:
            self.sessions[session_id].clear_history()
            return True
        return False
    
    async def get_session_history(self, session_id: str) -> List[Dict]:
        """Get full conversation history for a session"""
        if session_id in self.sessions:
            return self.sessions[session_id].get_history()
        return []
    
    async def process(self, task: str) -> str:
        """Base process method for agent interface"""
        return "Chatbot Agent ready. Use chat() method for conversations."
    
    def handle(self, *args, **kwargs):
        """Handle method implementation for BaseAgent interface"""
        return {"agent": "ChatbotAgent", "status": "ready"}


# Global instance
chatbot_agent = ChatbotAgent()
