"""
Chat Router - Handles chatbot interactions
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
import uuid

from app.agents.chatbot_agent import chatbot_agent

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_context: Optional[Dict] = None


class ClearSessionRequest(BaseModel):
    session_id: str


@router.post("/message")
async def send_message(request: ChatRequest):
    """
    Send a message to the chatbot and get a response
    
    Args:
        message: User's message
        session_id: Optional session ID (creates new session if not provided)
        user_context: Optional user context (profile, preferences)
    
    Returns:
        Chatbot response with session info
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process message
        result = await chatbot_agent.chat(
            message=request.message,
            session_id=session_id,
            user_context=request.user_context
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Chat failed"))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}/history")
async def get_session_history(session_id: str, last_n: int = 20):
    """
    Get conversation history for a session
    
    Args:
        session_id: Session identifier
        last_n: Number of recent messages to retrieve
    
    Returns:
        List of messages
    """
    try:
        history = await chatbot_agent.get_session_history(session_id)
        
        # Return last N messages
        return {
            "success": True,
            "session_id": session_id,
            "messages": history[-last_n:] if last_n else history,
            "total_messages": len(history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/clear")
async def clear_session(request: ClearSessionRequest):
    """
    Clear conversation history for a session
    
    Args:
        session_id: Session identifier
    
    Returns:
        Success status
    """
    try:
        success = await chatbot_agent.clear_session(request.session_id)
        
        return {
            "success": success,
            "session_id": request.session_id,
            "message": "Session cleared" if success else "Session not found"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quick-actions")
async def get_quick_actions(user_context: Optional[str] = None):
    """
    Get quick action suggestions
    
    Args:
        user_context: Optional JSON string with user context
    
    Returns:
        List of quick actions
    """
    try:
        import json
        context = json.loads(user_context) if user_context else None
        
        actions = await chatbot_agent.get_quick_actions(context)
        
        return {
            "success": True,
            "actions": actions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}/info")
async def get_session_info(session_id: str):
    """
    Get information about a chat session
    
    Args:
        session_id: Session identifier
    
    Returns:
        Session metadata
    """
    try:
        session = chatbot_agent.get_session(session_id)
        
        return {
            "success": True,
            "session_id": session_id,
            "message_count": len(session.messages),
            "created_at": session.created_at.isoformat(),
            "has_context": bool(session.context)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest")
async def get_suggestions(query: str, user_context: Optional[Dict] = None):
    """
    Get contextual suggestions based on user query
    
    Args:
        query: User's partial query or current context
        user_context: Optional user context
    
    Returns:
        List of suggested questions or actions
    """
    try:
        # Common suggestions
        suggestions = [
            "How do I check my eligibility for benefits?",
            "What documents do I need to upload?",
            "Can you explain this policy in simple terms?",
            "Which government schemes am I eligible for?",
            "How do I apply for a benefit?",
            "What languages are supported?",
            "Can I upload a PDF document?",
            "Show me all available benefits"
        ]
        
        # Filter suggestions based on query
        query_lower = query.lower()
        filtered = [s for s in suggestions if any(word in query_lower for word in s.lower().split())]
        
        if not filtered:
            filtered = suggestions[:4]
        
        return {
            "success": True,
            "suggestions": filtered[:5]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
