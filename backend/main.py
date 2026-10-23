from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="FocusGuard AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
        "message": "FocusGuard AI Backend is running"
    }


@app.post("/analyze")
def analyze_activity(request: ActivityRequest):
    activity = request.activity.lower()

    if activity == "study":
        decision = "Productive"
        reason = "This activity is directly related to the study session."
        confidence = 0.95

    elif activity == "instagram":
        decision = "Distracting"
        reason = "Social media activity is usually unrelated to the current study goal."
        confidence = 0.95

    else:
        decision = "Uncertain"
        reason = "The activity may or may not support the current study goal."
        confidence = 0.70

    return {
        "decision": decision,
        "reason": reason,
        "confidence": confidence
    }