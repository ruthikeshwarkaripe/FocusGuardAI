import os
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load .env from the project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from the .env file")


# Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=10000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)


app = FastAPI(title="FocusGuard AI Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ActivityRequest(BaseModel):
    subject: str
    topic: str
    goal: str
    activity: str


@app.get("/")
def root():
    return {
        "message": "FocusGuard AI Backend is running with Gemini"
    }


@app.post("/analyze")
def analyze_activity(request: ActivityRequest):

    prompt = f"""
You are FocusGuard AI, an intelligent study assistant.

Analyze whether the user's current activity supports their study goal.

Study context:
Subject: {request.subject}
Topic: {request.topic}
Goal: {request.goal}

Current activity:
{request.activity}

Classify the activity into exactly one of:
Productive
Distracting
Uncertain

Return ONLY valid JSON in this exact format:

{{
  "decision": "Productive",
  "reason": "Short explanation",
  "confidence": 0.95
}}

Rules:
- Productive = directly supports the study goal.
- Distracting = clearly unrelated or harmful to the study goal.
- Uncertain = could reasonably be useful or distracting depending on context.
- confidence must be a number between 0 and 1.
- Keep the reason short and clear.
"""

    try:
        print("Sending request to Gemini...")

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )

        print("Gemini response received.")
        print(response.text)

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        result = json.loads(text)

        result["source"] = "Gemini"

        return result

    except Exception as error:
        print("GEMINI ERROR:", repr(error))

        activity = request.activity.lower()

        if activity == "study":
            return {
                "decision": "Productive",
                "reason": "This activity directly supports your study session.",
                "confidence": 0.95,
                "source": "Local fallback"
            }

        if activity == "instagram":
            return {
                "decision": "Distracting",
                "reason": "Instagram is a social media platform that is unrelated to your current study goal.",
                "confidence": 0.95,
                "source": "Local fallback"
            }

        if activity == "whatsapp":
            return {
                "decision": "Uncertain",
                "reason": "WhatsApp may be useful for study communication, but it can also become distracting.",
                "confidence": 0.70,
                "source": "Local fallback"
            }

        if activity == "youtube":
            return {
                "decision": "Uncertain",
                "reason": "YouTube can support learning, but it can also contain unrelated content.",
                "confidence": 0.70,
                "source": "Local fallback"
            }

        return {
            "decision": "Uncertain",
            "reason": "FocusGuard could not confidently determine whether this activity supports your study goal.",
            "confidence": 0.50
        }