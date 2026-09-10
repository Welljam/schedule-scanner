from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from .process_schedule import analyze_schedule
from .models import ScheduleResponse

app = FastAPI()

@app.post("/schedule", response_model=ScheduleResponse)
def create_schedule():
    raw_text = analyze_schedule()

    try:
        schedule = ScheduleResponse.model_validate_json(raw_text) 
    except ValidationError:
        raise HTTPException(status_code=500, detail="Failed to parse model output into JSON")
    return schedule

