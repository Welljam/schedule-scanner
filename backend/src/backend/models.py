from pydantic import BaseModel

class Person(BaseModel):
    row: int
    name: str
    monday: str | None
    tuesday: str | None
    wednesday: str | None
    thursday: str | None
    friday: str | None
    saturday: str | None
    sunday: str | None

class ScheduleResponse(BaseModel):
    people: list[Person]

class DayShift(BaseModel):
    day: str
    start: str
    end: str

class CreateEventsRequest(BaseModel):
    name: str
    week: str
    days: list[DayShift]