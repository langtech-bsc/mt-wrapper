import httpx
from pydantic import BaseModel
from typing import List, Optional
from .config import settings
from .languages import language_name

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.0
    max_tokens: Optional[int] = 1024
    n: int = 1         # number of generations
    
    # In some OpenAI compatible endpoints (like vLLM which is likely used based on the model card)
    # best_of combined with use_beam_search or just n>1 triggers beam search.
    # We will pass extra parameters to try to trigger beam search natively.
    #extra_body: dict = {"num_beams": 5, "early_stopping": True}

async def _call_llm(text_prompt: str) -> str:
    """Helper function to call the Salamandra OpenAI-compatible endpoint."""
    headers = {
        "Content-Type": "application/json"
    }
    if settings.salamandra_api_key:
        headers["Authorization"] = f"Bearer {settings.salamandra_api_key}"
        
    messages = [{"role": "user", "content": text_prompt}]
        
    request_data = ChatCompletionRequest(
        model=settings.salamandra_model,
        messages=messages
    ).model_dump(exclude_none=True)
    
    url = f"{settings.salamandra_url.rstrip('/')}/chat/completions"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=request_data, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error calling LLM: {e}")
            raise

async def translate_text(text: str, source_lang: Optional[str], target_lang: str) -> str:
    source_str = language_name(source_lang) or "Unknown"
    target_lang = language_name(target_lang)
    prompt = f"Translate the following text from {source_str} into {target_lang}.\n{source_str}: {text}\n{target_lang}:"
    return await _call_llm(prompt)

async def post_edit_text(source_text: str, translation: str, source_lang: Optional[str], target_lang: str) -> str:
    source_str = language_name(source_lang) or "Unknown"
    target_lang = language_name(target_lang)
    prompt = f"Please fix any mistakes in the following {source_str}-{target_lang} machine translation or keep it unedited if it's correct.\nSource: {source_text}\nMT: {translation}\nCorrected:"
    return await _call_llm(prompt)

async def grammar_check_text(text: str, lang: str) -> str:
    lang = language_name(lang)
    prompt = f"Please fix any mistakes in the following {lang} sentence or keep it unedited if it's correct.\nSentence: {text}\nCorrected:"
    return await _call_llm(prompt)
