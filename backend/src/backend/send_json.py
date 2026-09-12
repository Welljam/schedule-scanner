from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from .process_schedule import analyze_schedule
from .models import ScheduleResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/schedule", response_model=ScheduleResponse)
async def create_schedule(file: UploadFile = File(...)):
    contents = await file.read()
    raw_text = analyze_schedule(contents)

    try:
        schedule = ScheduleResponse.model_validate_json(raw_text) 
    except ValidationError:
        raise HTTPException(status_code=500, detail="Failed to parse model output into JSON")
    
    return schedule

