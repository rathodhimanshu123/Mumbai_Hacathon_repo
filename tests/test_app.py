import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_analyze_symptoms():
    """Test symptom analysis endpoint"""
    response = client.post("/api/analyze_symptoms", json={
        "symptoms": ["severe headache", "fever", "fatigue"],
        "context": {"age": 35, "duration": "2 days"}
    })
    assert response.status_code == 200
    data = response.json()
    assert "urgency_level" in data
    assert "recommended_actions" in data
    assert isinstance(data["recommended_actions"], list)

def test_generate_followup():
    """Test follow-up question generation"""
    response = client.post("/api/generate_followup", json={
        "conversation_history": [
            {
                "user": "I have a severe headache",
                "assistant": "How long have you been experiencing the headache?"
            },
            {
                "user": "About 2 days",
                "assistant": "Is the pain constant or does it come and go?"
            }
        ]
    })
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data

def test_get_health_data():
    """Test health data retrieval"""
    response = client.get("/api/health_data/7")
    assert response.status_code == 200
    data = response.json()
    assert "health_data" in data
    assert isinstance(data["health_data"], list)
    if data["health_data"]:
        health_record = data["health_data"][0]
        assert "date" in health_record
        
@pytest.mark.asyncio
async def test_gemini_client(mocker):
    """Test Gemini client methods"""
    from src.api.gemini import GeminiClient
    
    mock_response = {
        "urgency_level": "MEDIUM",
        "initial_assessment": "Test assessment",
        "recommended_actions": ["Action 1", "Action 2"],
        "lifestyle_recommendations": ["Rec 1", "Rec 2"],
        "warning_signs": ["Warning 1", "Warning 2"]
    }
    
    mocker.patch(
        "src.api.gemini.GeminiClient._call_gemini_api",
        return_value=mock_response
    )
    
    client = GeminiClient()
    result = await client.analyze_symptoms(["headache"])
    
    assert result.urgency_level == "MEDIUM"
    assert len(result.recommended_actions) == 2
    assert len(result.lifestyle_recommendations) == 2