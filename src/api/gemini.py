import os
import json
import asyncio
from typing import List, Dict, Optional
from dotenv import l google.generativeai as genai
from pydantic import BaseModel

load_dotenv()

class HealthAnalysisResponse(BaseModel):
    urgency_level: str
    initial_assessment: str
    recommended_actions: List[str]
    lifestyle_recommendations: List[str]
    warning_signs: List[str]

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def analyze_symptoms(self, symptoms: List[str], context: Optional[Dict] = None) -> HealthAnalysisResponse:
        """Analyze symptoms and generate health insights using Gemini API"""
        prompt = self._build_analysis_prompt(symptoms, context)
        response = await self._call_gemini_api(prompt)
        return self._parse_analysis_response(response)
        
    async def generate_follow_up(self, conversation_history: List[Dict]) -> str:
        """Generate relevant follow-up questions based on conversation history"""
        prompt = self._build_follow_up_prompt(conversation_history)
        response = await self._call_gemini_api(prompt)
        return response
        
    def _build_analysis_prompt(self, symptoms: List[str], context: Optional[Dict] = None) -> str:
        """Build a structured prompt for symptom analysis"""
        base_prompt = [
            "As a medical AI assistant, analyze these symptoms for triage:",
            f"Symptoms: {', '.join(symptoms)}"
        ]
        
        if context:
            base_prompt.append(f"Additional Context: {json.dumps(context)}")
            
        analysis_requirements = [
            "Please provide a JSON response with the following structure:",
            "{",
            '  "urgency_level": "(LOW/MEDIUM/HIGH/EMERGENCY)",',
            '  "initial_assessment": "Brief analysis of symptoms",',
            '  "recommended_actions": ["Action 1", "Action 2", ...],',
            '  "lifestyle_recommendations": ["Recommendation 1", "Recommendation 2", ...],',
            '  "warning_signs": ["Warning sign 1", "Warning sign 2", ...]',
            "}"
        ]
        
        return "\n".join(base_prompt + [""] + analysis_requirements)
    
    def _build_follow_up_prompt(self, conversation_history: List[Dict]) -> str:
        """Build prompt for generating follow-up questions"""
        conversation = "\n".join([
            f"User: {msg['user']}\nAssistant: {msg['assistant']}"
            for msg in conversation_history
        ])
        
        return (
            "Based on this medical conversation, generate 2-3 relevant follow-up "
            "questions to better understand the patient's condition:\n\n"
            f"{conversation}\n\n"
            "Format the questions as a JSON array."
        )
    
    async def _call_gemini_api(self, prompt: str) -> str:
        """Make an async call to the Gemini API"""
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={
                    'temperature': 0.3,
                    'top_p': 0.8,
                    'top_k': 40
                }
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
    
    def _parse_analysis_response(self, response: str) -> HealthAnalysisResponse:
        """Parse and validate the Gemini API response"""
        try:
            data = json.loads(response)
            return HealthAnalysisResponse(**data)
        except Exception as e:
            raise ValueError(f"Failed to parse Gemini API response: {str(e)}")
    """
    # Code to handle the response from the Gemini API goes here
    pass

import os
import json
import asyncio
import aiohttp
from typing import List, Dict, Optional
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class HealthAnalysisResponse(BaseModel):
    urgency_level: str
    initial_assessment: str
    recommended_actions: List[str]
    lifestyle_recommendations: List[str]
    warning_signs: List[str]

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
    async def analyze_symptoms(self, symptoms: List[str], context: Optional[Dict] = None) -> HealthAnalysisResponse:
        """Analyze symptoms and generate health insights using Gemini API"""
        prompt = self._build_analysis_prompt(symptoms, context)
        response = await self._call_gemini_api(prompt)
        return self._parse_analysis_response(response)
        
    async def generate_follow_up(self, conversation_history: List[Dict]) -> str:
        """Generate relevant follow-up questions based on conversation history"""
        prompt = self._build_follow_up_prompt(conversation_history)
        response = await self._call_gemini_api(prompt)
        return response
        
    def _build_analysis_prompt(self, symptoms: List[str], context: Optional[Dict] = None) -> str:
        """Build a structured prompt for symptom analysis"""
        base_prompt = [
            "As a medical AI assistant, analyze these symptoms for triage:",
            f"Symptoms: {', '.join(symptoms)}"
        ]
        
        if context:
            base_prompt.append(f"Additional Context: {json.dumps(context)}")
            
        analysis_requirements = [
            "Please provide a JSON response with the following structure:",
            "{",
            '  "urgency_level": "(LOW/MEDIUM/HIGH/EMERGENCY)",',
            '  "initial_assessment": "Brief analysis of symptoms",',
            '  "recommended_actions": ["Action 1", "Action 2", ...],',
            '  "lifestyle_recommendations": ["Recommendation 1", "Recommendation 2", ...],',
            '  "warning_signs": ["Warning sign 1", "Warning sign 2", ...]',
            "}"
        ]
        
        return "\n".join(base_prompt + [""] + analysis_requirements)
    
    def _build_follow_up_prompt(self, conversation_history: List[Dict]) -> str:
        """Build prompt for generating follow-up questions"""
        conversation = "\n".join([
            f"User: {msg['user']}\nAssistant: {msg['assistant']}"
            for msg in conversation_history
        ])
        
        return (
            "Based on this medical conversation, generate 2-3 relevant follow-up "
            "questions to better understand the patient's condition:\n\n"
            f"{conversation}\n\n"
            "Format the questions as a JSON array."
        )
    
    async def _call_gemini_api(self, prompt: str) -> str:
        """Make an async call to the Gemini API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.endpoint, headers=headers, json=data) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API call failed: {error_text}")
                    
                    result = await response.json()
                    return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
    
    def _parse_analysis_response(self, response: str) -> HealthAnalysisResponse:
        """Parse and validate the Gemini API response"""
        try:
            data = json.loads(response)
            return HealthAnalysisResponse(**data)
        except Exception as e:
            raise ValueError(f"Failed to parse Gemini API response: {str(e)}")