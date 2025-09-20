from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from dotenv import load_dotenv
from src.api.gemini import GeminiClient, HealthAnalysisResponse
from src.api.google_fit import GoogleFitClient, FitnessData

load_dotenv()

app = FastAPI(title="AI Nurse Companion")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
gemini_client = GeminiClient()
google_fit_client = GoogleFitClient()

class SymptomRequest(BaseModel):
    symptoms: List[str]
    context: Optional[Dict] = None

class ConversationMessage(BaseModel):
    user: str
    assistant: str

class FollowUpRequest(BaseModel):
    conversation_history: List[ConversationMessage]

@app.post("/api/analyze_symptoms", response_model=HealthAnalysisResponse)
async def analyze_symptoms(request: SymptomRequest):
    """
    Analyze symptoms using Gemini AI and return health insights
    """
    try:
        return await gemini_client.analyze_symptoms(request.symptoms, request.context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate_followup")
async def generate_followup(request: FollowUpRequest):
    """
    Generate follow-up questions based on conversation history
    """
    try:
        questions = await gemini_client.generate_follow_up(request.conversation_history)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health_data/{days}")
async def get_health_data(days: int = 7):
    """
    Get user's health data from Google Fit
    """
    try:
        activity_data = await google_fit_client.get_activity_data(days)
        sleep_data = await google_fit_client.get_sleep_data(days)
        
        # Merge activity and sleep data by date
        health_data = {}
        for data in activity_data:
            health_data[data.date] = data.dict()
            
        for data in sleep_data:
            if data.date in health_data:
                health_data[data.date].update(data.dict())
            else:
                health_data[data.date] = data.dict()
                
        return {"health_data": list(health_data.values())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)