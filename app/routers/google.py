from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Union, Optional
from ..llm import translate_text
import asyncio

router = APIRouter()

class GoogleTranslateRequest(BaseModel):
    q: Union[str, List[str]]
    target: str
    source: Optional[str] = None
    format: Optional[str] = "text"

@router.post("/language/translate/v2")
async def google_translate(request: GoogleTranslateRequest):
    queries = request.q if isinstance(request.q, list) else [request.q]
    
    tasks = [
        translate_text(text=q, source_lang=request.source, target_lang=request.target)
        for q in queries
    ]
    
    try:
        results = await asyncio.gather(*tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM backend error: {str(e)}")
    
    translations = []
    for res in results:
        t_obj = {"translatedText": res}
        if request.source:
             t_obj["detectedSourceLanguage"] = request.source
        translations.append(t_obj)

    return {
        "data": {
            "translations": translations
        }
    }
