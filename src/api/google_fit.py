import os
from typing import Dict, List, Optional
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pydantic import BaseModel

SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    'https://www.googleapis.com/auth/fitness.sleep.read'
]

class FitnessData(BaseModel):
    date: str
    steps: Optional[int]
    active_minutes: Optional[int]
    heart_rate_avg: Optional[int]
    sleep_hours: Optional[float]
    deep_sleep_percentage: Optional[float]

class GoogleFitClient:
    def __init__(self):
        self.creds = None
        self.service = None
        self.load_credentials()

    def load_credentials(self):
        """Load or refresh Google Fit API credentials"""
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('fitness', 'v1', credentials=self.creds)

    async def get_activity_data(self, days: int = 7) -> List[FitnessData]:
        """Get user's activity data for the last n days"""
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(days=days)

        # Convert times to nanoseconds for the API
        end_nanos = int(end_time.timestamp() * 1000000000)
        start_nanos = int(start_time.timestamp() * 1000000000)

        body = {
            "aggregateBy": [{
                "dataTypeName": "com.google.step_count.delta",
            }, {
                "dataTypeName": "com.google.active_minutes",
            }, {
                "dataTypeName": "com.google.heart_rate.bpm",
            }],
            "bucketByTime": {"durationMillis": 86400000},  # 1 day
            "startTimeMillis": start_nanos // 1000000,
            "endTimeMillis": end_nanos // 1000000
        }

        try:
            response = await self.service.users().dataset().aggregate(userId="me", body=body).execute()
            return self._parse_activity_response(response)
        except Exception as e:
            print(f"Error fetching activity data: {str(e)}")
            return []

    async def get_sleep_data(self, days: int = 7) -> List[FitnessData]:
        """Get user's sleep data for the last n days"""
        # Note: Sleep data requires different endpoint and parsing
        # This is a placeholder implementation
        return [
            FitnessData(
                date="2025-09-20",
                sleep_hours=7.5,
                deep_sleep_percentage=20
            )
        ]

    def _parse_activity_response(self, response: Dict) -> List[FitnessData]:
        """Parse the Google Fit API activity response"""
        fitness_data = []
        for bucket in response.get("bucket", []):
            date = datetime.datetime.fromtimestamp(
                int(bucket["startTimeMillis"]) / 1000
            ).strftime("%Y-%m-%d")
            
            data = FitnessData(
                date=date,
                steps=0,
                active_minutes=0,
                heart_rate_avg=0
            )

            for dataset in bucket.get("dataset", []):
                for point in dataset.get("point", []):
                    data_type = point["dataTypeName"]
                    if data_type == "com.google.step_count.delta":
                        data.steps = sum(val["intVal"] for val in point["value"])
                    elif data_type == "com.google.active_minutes":
                        data.active_minutes = sum(val["intVal"] for val in point["value"])
                    elif data_type == "com.google.heart_rate.bpm":
                        values = [val["fpVal"] for val in point["value"]]
                        data.heart_rate_avg = int(sum(values) / len(values)) if values else 0

            fitness_data.append(data)

        return fitness_data
    pass