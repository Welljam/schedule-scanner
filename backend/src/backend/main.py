from fastapi import FastAPI, HTTPException, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from .process_schedule import analyze_schedule
from .models import ScheduleResponse
from .google_oauth import router as google_router
from .create_events import router as create_router

app = FastAPI()
app.include_router(google_router)
app.include_router(create_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)

@app.post("/schedule", response_model=ScheduleResponse)
async def create_schedule(file: UploadFile = File(...)):
    contents = await file.read()
    raw_text = analyze_schedule(contents)

    try:
        schedule = ScheduleResponse.model_validate_json(raw_text) 
    except ValidationError:
        raise HTTPException(status_code=500, detail="Failed to parse model output into JSON")
    
    return schedule

