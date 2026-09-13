from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from googleapiclient.discovery import build
from .models import CreateEventsRequest
from .google_oauth import load_credentials

router = APIRouter()

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
TIMEZONE = "Europe/Stockholm"


def shift_date(week: str, day: str):
    weekday = DAYS.index(day) + 1
    return datetime.strptime(f"{week}-{weekday}", "%G-W%V-%u").date()


@router.post("/create")
def create_event(request: CreateEventsRequest, req: Request):
    creds = load_credentials(req.cookies.get("google_tokens"))
    if creds is None:
        raise HTTPException(status_code=401, detail="User not authenticated. Go to /login first.")

    service = build("calendar", "v3", credentials=creds)

    links = []
    for shift in request.days:
        date = shift_date(request.week, shift.day)
        event_body = {
            "summary": f"{request.name} work",
            "start": {"dateTime": f"{date}T{shift.start}:00", "timeZone": TIMEZONE},
            "end": {"dateTime": f"{date}T{shift.end}:00", "timeZone": TIMEZONE},
        }
        created = service.events().insert(calendarId="primary", body=event_body).execute()
        links.append(created.get("htmlLink"))

    return {"status": "created", "count": len(links), "links": links}
