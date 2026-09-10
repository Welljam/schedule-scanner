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

