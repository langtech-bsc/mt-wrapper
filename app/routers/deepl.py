from fastapi import APIRouter, HTTPException, Request
from ..llm import translate_text
import asyncio
import json

router = APIRouter()

@router.post("/v2/translate")
@router.post("/v2/translate/")
async def deepl_translate(request: Request):
    content_type = request.headers.get("Content-Type", "")
    
    texts = []
    target_lang = None
    source_lang = None
    
    if "application/json" in content_type:
        try:
            data = await request.json()
            texts_data = data.get("text", [])
            texts = texts_data if isinstance(texts_data, list) else [texts_data]
            target_lang = data.get("target_lang")
            source_lang = data.get("source_lang")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON body")
    else:
        form = await request.form()
        texts = form.getlist("text")
        target_lang = form.get("target_lang")
        source_lang = form.get("source_lang")
        
    if not texts:
        raise HTTPException(status_code=400, detail="Missing 'text' parameter")
    if not target_lang:
        raise HTTPException(status_code=400, detail="Missing 'target_lang' parameter")
        
    tasks = [
        translate_text(text=t, source_lang=source_lang, target_lang=target_lang)
        for t in texts
    ]
    
    try:
        results = await asyncio.gather(*tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM backend error: {str(e)}")
        
    translations = [
        {
            "detected_source_language": source_lang or "UNKNOWN",
            "text": res
        }
        for res in results
    ]
        
    return {"translations": translations}
