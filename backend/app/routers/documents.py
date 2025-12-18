"""
Documents Router - Handles document upload and processing
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
import uuid

from app.agents.document_processor_agent import document_processor_agent
from app.agents.policy_interpreter_agent import policy_interpreter_agent

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    extract_method: str = Form("auto"),
    interpret_policy: bool = Form(False)
):
    """
    Upload and process a document
    
    Args:
        file: Document file (PDF, image, DOCX)
        extract_method: 'auto', 'ocr', or 'native'
        interpret_policy: Whether to automatically interpret as policy
    
    Returns:
        Extracted text and optional policy interpretation
    """
    try:
        # Read file content
        content = await file.read()
        
        # Process document
        result = await document_processor_agent.process_document(
            file_content=content,
            filename=file.filename,
            extract_method=extract_method
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to process document"))
        
        extracted_text = result["text"]
        
        # Get document statistics
        stats = await document_processor_agent.get_document_stats(extracted_text)
        
        # Detect language
        language = await document_processor_agent.detect_document_language(extracted_text)
        
        response_data = {
            "success": True,
            "filename": file.filename,
            "text": extracted_text,
            "extraction_method": result["method"],
            "file_format": result["format"],
            "statistics": stats,
            "detected_language": language
        }
        
        # Optionally interpret as policy
        if interpret_policy and extracted_text.strip():
            try:
                policy_result = await policy_interpreter_agent.interpret_policy(
                    raw_text=extracted_text,
                    policy_name=file.filename.replace('.pdf', '').replace('.docx', '')
                )
                response_data["policy"] = policy_result
            except Exception as e:
                response_data["policy_interpretation_error"] = str(e)
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-text")
async def extract_text_from_upload(
    file: UploadFile = File(...),
    method: str = Form("auto")
):
    """
    Extract text from uploaded document without policy interpretation
    
    Args:
        file: Document file
        method: Extraction method ('auto', 'ocr', 'native')
    
    Returns:
        Extracted text and metadata
    """
    try:
        content = await file.read()
        
        result = await document_processor_agent.process_document(
            file_content=content,
            filename=file.filename,
            extract_method=method
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        stats = await document_processor_agent.get_document_stats(result["text"])
        
        return {
            "success": True,
            "text": result["text"],
            "method": result["method"],
            "filename": file.filename,
            "statistics": stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported document formats"""
    return {
        "formats": document_processor_agent.supported_formats,
        "description": {
            "pdf": "PDF documents (native text or OCR)",
            "images": "JPG, PNG, TIFF, BMP (OCR)",
            "docx": "Word documents (native text)"
        },
        "features": {
            "ocr": "Optical Character Recognition for images and scanned PDFs",
            "native": "Direct text extraction from digital documents",
            "auto": "Automatic selection of best extraction method"
        }
    }
