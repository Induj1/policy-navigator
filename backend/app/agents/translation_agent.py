"""
Translation Agent - Handles multi-language support
"""

from typing import Optional, Dict, List
from enum import Enum

try:
    from deep_translator import GoogleTranslator
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0  # For consistent results
    TRANSLATION_LIBS_AVAILABLE = True
except ImportError:
    TRANSLATION_LIBS_AVAILABLE = False
    print("⚠️  Translation libraries not installed. Run: pip install deep-translator langdetect")

from app.agents.base_agent import BaseAgent


class SupportedLanguage(str, Enum):
    """Supported languages for the application"""
    ENGLISH = "en"
    HINDI = "hi"
    MARATHI = "mr"
    TAMIL = "ta"
    TELUGU = "te"
    KANNADA = "kn"
    GUJARATI = "gu"
    BENGALI = "bn"
    MALAYALAM = "ml"
    PUNJABI = "pa"


LANGUAGE_NAMES = {
    "en": "English",
    "hi": "हिंदी (Hindi)",
    "mr": "मराठी (Marathi)",
    "ta": "தமிழ் (Tamil)",
    "te": "తెలుగు (Telugu)",
    "kn": "ಕನ್ನಡ (Kannada)",
    "gu": "ગુજરાતી (Gujarati)",
    "bn": "বাংলা (Bengali)",
    "ml": "മലയാളം (Malayalam)",
    "pa": "ਪੰਜਾਬੀ (Punjabi)"
}


class TranslationAgent(BaseAgent):
    """Agent that handles text translation and language detection"""
    
    def __init__(self):
        super().__init__(llm=None)
        self.name = "Translation Agent"
        self.description = "Translates text between multiple Indian languages"
        self.supported_languages = list(SupportedLanguage)
    
    async def detect_language(self, text: str) -> Dict[str, str]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary with language code and name
        """
        if not TRANSLATION_LIBS_AVAILABLE:
            return {
                "code": "unknown",
                "name": "Unknown",
                "error": "Translation libraries not installed"
            }
        
        try:
            lang_code = detect(text)
            lang_name = LANGUAGE_NAMES.get(lang_code, f"Unknown ({lang_code})")
            
            return {
                "code": lang_code,
                "name": lang_name,
                "confidence": "high"
            }
        except Exception as e:
            return {
                "code": "unknown",
                "name": "Unknown",
                "error": str(e)
            }
    
    async def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: str = "auto"
    ) -> Dict[str, str]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'hi', 'mr')
            source_language: Source language code or 'auto' for detection
        
        Returns:
            Dictionary with translated text and metadata
        """
        if not TRANSLATION_LIBS_AVAILABLE:
            return {
                "success": False,
                "translated_text": text,
                "source_language": "unknown",
                "target_language": target_language,
                "error": "Translation libraries not installed"
            }
        
        try:
            # Detect source language if auto
            if source_language == "auto":
                detected = await self.detect_language(text)
                source_language = detected.get("code", "en")
            
            # Skip translation if source and target are the same
            if source_language == target_language:
                return {
                    "success": True,
                    "translated_text": text,
                    "source_language": source_language,
                    "target_language": target_language,
                    "note": "Source and target languages are the same"
                }
            
            # Translate
            translator = GoogleTranslator(source=source_language, target=target_language)
            translated = translator.translate(text)
            
            return {
                "success": True,
                "translated_text": translated,
                "source_language": source_language,
                "target_language": target_language,
                "source_name": LANGUAGE_NAMES.get(source_language, source_language),
                "target_name": LANGUAGE_NAMES.get(target_language, target_language)
            }
            
        except Exception as e:
            return {
                "success": False,
                "translated_text": text,
                "source_language": source_language,
                "target_language": target_language,
                "error": str(e)
            }
    
    async def translate_policy(
        self,
        policy_data: Dict,
        target_language: str
    ) -> Dict:
        """
        Translate a policy object to target language
        
        Args:
            policy_data: Policy dictionary with text fields
            target_language: Target language code
        
        Returns:
            Translated policy dictionary
        """
        try:
            translated_policy = policy_data.copy()
            
            # Translate policy name
            if "name" in policy_data:
                result = await self.translate_text(
                    policy_data["name"],
                    target_language
                )
                translated_policy["name"] = result["translated_text"]
            
            # Translate description
            if "description" in policy_data:
                result = await self.translate_text(
                    policy_data["description"],
                    target_language
                )
                translated_policy["description"] = result["translated_text"]
            
            # Translate raw text
            if "raw_text" in policy_data:
                result = await self.translate_text(
                    policy_data["raw_text"],
                    target_language
                )
                translated_policy["raw_text"] = result["translated_text"]
            
            # Translate benefits
            if "benefits" in policy_data and isinstance(policy_data["benefits"], str):
                result = await self.translate_text(
                    policy_data["benefits"],
                    target_language
                )
                translated_policy["benefits"] = result["translated_text"]
            
            translated_policy["language"] = target_language
            translated_policy["original_language"] = "en"
            
            return {
                "success": True,
                "policy": translated_policy
            }
            
        except Exception as e:
            return {
                "success": False,
                "policy": policy_data,
                "error": str(e)
            }
    
    async def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages"""
        return [
            {"code": code, "name": name}
            for code, name in LANGUAGE_NAMES.items()
        ]
    
    async def translate_ui_text(
        self,
        ui_strings: Dict[str, str],
        target_language: str
    ) -> Dict[str, str]:
        """
        Translate UI strings for frontend localization
        
        Args:
            ui_strings: Dictionary of English UI strings
            target_language: Target language code
        
        Returns:
            Dictionary of translated strings
        """
        if target_language == "en":
            return ui_strings
        
        translated = {}
        for key, text in ui_strings.items():
            result = await self.translate_text(text, target_language, "en")
            translated[key] = result.get("translated_text", text)
        
        return translated
    
    async def process(self, task: str) -> str:
        """Base process method for agent interface"""
        return "Translation Agent ready. Use translate_text() or translate_policy() methods."
    
    def handle(self, *args, **kwargs):
        """Handle method implementation for BaseAgent interface"""
        return {"agent": "TranslationAgent", "status": "ready"}


# Global instance
translation_agent = TranslationAgent()
