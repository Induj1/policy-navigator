"""
Document Processor Agent - Handles OCR and document text extraction
"""

import os
import io
from typing import Optional, Dict, Any
from pathlib import Path
import tempfile

try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_path, convert_from_bytes
    import PyPDF2
    import docx
    DOCUMENT_LIBS_AVAILABLE = True
except ImportError:
    DOCUMENT_LIBS_AVAILABLE = False
    print("⚠️  Document processing libraries not installed. Run: pip install pytesseract pdf2image PyPDF2 python-docx Pillow")

from app.agents.base_agent import BaseAgent


class DocumentProcessorAgent(BaseAgent):
    """Agent that processes documents and extracts text using OCR"""
    
    def __init__(self):
        super().__init__(llm=None)
        self.name = "Document Processor Agent"
        self.description = "Extracts text from PDFs, images, and documents using OCR"
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.docx', '.doc']
        
        # Configure Tesseract path for Windows (adjust if needed)
        if os.name == 'nt':  # Windows
            # Common installation paths
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Tesseract-OCR\tesseract.exe'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
    
    async def process_document(
        self,
        file_content: bytes,
        filename: str,
        extract_method: str = "auto"
    ) -> Dict[str, Any]:
        """
        Process a document and extract text
        
        Args:
            file_content: Binary content of the file
            filename: Name of the file
            extract_method: 'auto', 'ocr', or 'native'
        
        Returns:
            Dictionary with extracted text and metadata
        """
        if not DOCUMENT_LIBS_AVAILABLE:
            return {
                "success": False,
                "error": "Document processing libraries not installed",
                "text": "",
                "method": "none"
            }
        
        file_ext = Path(filename).suffix.lower()
        
        if file_ext not in self.supported_formats:
            return {
                "success": False,
                "error": f"Unsupported file format: {file_ext}",
                "text": "",
                "method": "none"
            }
        
        try:
            # Try native text extraction first for PDFs and DOCX
            if extract_method in ["auto", "native"]:
                if file_ext == '.pdf':
                    text = await self._extract_pdf_native(file_content)
                    if text.strip():
                        return {
                            "success": True,
                            "text": text,
                            "method": "native_pdf",
                            "filename": filename,
                            "format": file_ext
                        }
                
                elif file_ext == '.docx':
                    text = await self._extract_docx(file_content)
                    if text.strip():
                        return {
                            "success": True,
                            "text": text,
                            "method": "native_docx",
                            "filename": filename,
                            "format": file_ext
                        }
            
            # Fall back to OCR for images or if native extraction failed
            if extract_method in ["auto", "ocr"]:
                text = await self._extract_with_ocr(file_content, file_ext)
                return {
                    "success": True,
                    "text": text,
                    "method": "ocr",
                    "filename": filename,
                    "format": file_ext
                }
            
            return {
                "success": False,
                "error": "Could not extract text from document",
                "text": "",
                "method": "failed"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": "",
                "method": "error"
            }
    
    async def _extract_pdf_native(self, file_content: bytes) -> str:
        """Extract text from PDF using native PDF reader"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Native PDF extraction failed: {e}")
            return ""
    
    async def _extract_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            print(f"DOCX extraction failed: {e}")
            return ""
    
    async def _extract_with_ocr(self, file_content: bytes, file_ext: str) -> str:
        """Extract text using OCR"""
        try:
            if file_ext == '.pdf':
                # Convert PDF to images then OCR
                images = convert_from_bytes(file_content)
                text = ""
                for i, image in enumerate(images):
                    page_text = pytesseract.image_to_string(image, lang='eng')
                    text += f"\n--- Page {i+1} ---\n{page_text}"
                return text.strip()
            else:
                # Direct OCR for images
                image = Image.open(io.BytesIO(file_content))
                text = pytesseract.image_to_string(image, lang='eng')
                return text.strip()
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            raise
    
    async def detect_document_language(self, text: str) -> str:
        """Detect the language of extracted text"""
        try:
            from langdetect import detect
            return detect(text)
        except:
            return "unknown"
    
    async def get_document_stats(self, text: str) -> Dict[str, Any]:
        """Get statistics about the extracted text"""
        words = text.split()
        lines = text.split('\n')
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "line_count": len(lines),
            "estimated_pages": len(lines) // 40 + 1  # Rough estimate
        }
    
    async def process(self, task: str) -> str:
        """Base process method for agent interface"""
        return "Document Processor Agent ready. Use process_document() method for file processing."
    
    def handle(self, *args, **kwargs):
        """Handle method implementation for BaseAgent interface"""
        return {"agent": "DocumentProcessorAgent", "status": "ready"}


# Global instance
document_processor_agent = DocumentProcessorAgent()
