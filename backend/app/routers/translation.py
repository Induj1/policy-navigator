"""
Translation Router - Handles multi-language support
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List

from app.agents.translation_agent import translation_agent, LANGUAGE_NAMES

router = APIRouter(prefix="/translate", tags=["translation"])


class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = "auto"


class PolicyTranslateRequest(BaseModel):
    policy: Dict
    target_language: str


class DetectLanguageRequest(BaseModel):
    text: str


@router.post("/text")
async def translate_text(request: TranslateRequest):
    """
    Translate text to target language
    
    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'hi', 'mr', 'ta')
        source_language: Source language code or 'auto' for detection
    
    Returns:
        Translated text with metadata
    """
    try:
        result = await translation_agent.translate_text(
            text=request.text,
            target_language=request.target_language,
            source_language=request.source_language
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Translation failed"))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect")
async def detect_language(request: DetectLanguageRequest):
    """
    Detect the language of given text
    
    Args:
        text: Text to analyze
    
    Returns:
        Detected language code and name
    """
    try:
        result = await translation_agent.detect_language(request.text)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/policy")
async def translate_policy(request: PolicyTranslateRequest):
    """
    Translate a complete policy object
    
    Args:
        policy: Policy dictionary with text fields
        target_language: Target language code
    
    Returns:
        Translated policy
    """
    try:
        result = await translation_agent.translate_policy(
            policy_data=request.policy,
            target_language=request.target_language
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Policy translation failed"))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/languages")
async def get_supported_languages():
    """
    Get list of all supported languages
    
    Returns:
        List of language codes and names
    """
    try:
        languages = await translation_agent.get_supported_languages()
        
        return {
            "languages": languages,
            "count": len(languages),
            "default": "en"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ui-strings")
async def translate_ui_strings(target_language: str, strings: Dict[str, str]):
    """
    Translate UI strings for frontend localization
    
    Args:
        target_language: Target language code
        strings: Dictionary of English UI strings
    
    Returns:
        Dictionary of translated strings
    """
    try:
        translated = await translation_agent.translate_ui_text(
            ui_strings=strings,
            target_language=target_language
        )
        
        return {
            "success": True,
            "language": target_language,
            "strings": translated
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/language-info/{language_code}")
async def get_language_info(language_code: str):
    """
    Get detailed information about a specific language
    
    Args:
        language_code: Language code (e.g., 'hi', 'mr')
    
    Returns:
        Language information
    """
    if language_code not in LANGUAGE_NAMES:
        raise HTTPException(status_code=404, detail=f"Language '{language_code}' not supported")
    
    return {
        "code": language_code,
        "name": LANGUAGE_NAMES[language_code],
        "supported": True,
        "features": {
            "text_translation": True,
            "policy_translation": True,
            "ui_localization": True
        }
    }
