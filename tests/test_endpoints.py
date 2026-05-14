import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "model" in response.json()

@patch("app.llm._call_llm", new_callable=AsyncMock)
def test_google_translate(mock_call_llm):
    mock_call_llm.return_value = "Hola mundo"
    
    response = client.post("/language/translate/v2", json={
        "q": "Hello world",
        "target": "es",
        "source": "en"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "translations" in data["data"]
    assert data["data"]["translations"][0]["translatedText"] == "Hola mundo"
    assert data["data"]["translations"][0]["detectedSourceLanguage"] == "en"

@patch("app.llm._call_llm", new_callable=AsyncMock)
def test_deepl_translate_json(mock_call_llm):
    mock_call_llm.return_value = "Hola mundo"
    
    response = client.post("/v2/translate", json={
        "text": ["Hello world"],
        "target_lang": "ES",
        "source_lang": "EN"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "translations" in data
    assert data["translations"][0]["text"] == "Hola mundo"
    
@patch("app.llm._call_llm", new_callable=AsyncMock)
def test_deepl_translate_form(mock_call_llm):
    mock_call_llm.return_value = "Hola mundo form"
    
    response = client.post("/v2/translate", data={
        "text": ["Hello form"],
        "target_lang": "ES",
        "source_lang": "EN"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["translations"][0]["text"] == "Hola mundo form"

@patch("app.llm._call_llm", new_callable=AsyncMock)
def test_custom_post_edit(mock_call_llm):
    mock_call_llm.return_value = "Hola a todos"
    
    response = client.post("/api/v1/post-edit", json={
        "source_text": "Hello everyone",
        "translation": "Hola todo el mundo",
        "target_lang": "es"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["corrected_translation"] == "Hola a todos"

@patch("app.llm._call_llm", new_callable=AsyncMock)
def test_custom_grammar_check(mock_call_llm):
    mock_call_llm.return_value = "I am going to the store."
    
    response = client.post("/api/v1/grammar-check", json={
        "text": "I is going to store.",
        "lang": "en"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["corrected_text"] == "I am going to the store."
