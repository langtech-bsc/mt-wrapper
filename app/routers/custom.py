from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..llm import post_edit_text, grammar_check_text

router = APIRouter(prefix="/api/v1", tags=["custom"])

class PostEditRequest(BaseModel):
    source_text: str
    translation: str
    source_lang: Optional[str] = None
    target_lang: str

class GrammarCheckRequest(BaseModel):
    text: str
    lang: str

@router.post("/post-edit")
async def post_edit(request: PostEditRequest):
    try:
        result = await post_edit_text(
            source_text=request.source_text,
            translation=request.translation,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        return {"corrected_translation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM backend error: {str(e)}")

@router.post("/grammar-check")
async def grammar_check(request: GrammarCheckRequest):
    try:
        result = await grammar_check_text(
            text=request.text,
            lang=request.lang
        )
        return {"corrected_text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM backend error: {str(e)}")
