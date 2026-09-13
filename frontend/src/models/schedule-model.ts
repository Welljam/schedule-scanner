export interface Person {
    row: number;
    name: string | null;
    monday: string | null;
    tuesday: string | null;
    wednesday: string | null;
    thursday: string | null;
    friday: string | null;
    saturday: string | null;
    sunday: string | null;
}

export interface ScheduleResponse {
    people: Person[];
}

export interface Days {
    day: string; 
    start: string; 
    end: string;
}

export interface CreateEventsRequest {
  name: string;
  week: string;
  days: Days[];
}