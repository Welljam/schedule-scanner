import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ScheduleResponse, CreateEventsRequest } from '../models/schedule-model';

@Injectable({
  providedIn: 'root',
})
export class ScheduleApi {
  http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000';

  uploadSchedule(file: File): Observable<ScheduleResponse> {
    const form = new FormData();
    form.append('file', file);
    return this.http.post<ScheduleResponse>(`${this.baseUrl}/schedule`, form);
  }

  create_event(event: CreateEventsRequest): Observable<CreateEventsRequest>{
    return this.http.post<CreateEventsRequest>(`${this.baseUrl}/create`, event, { withCredentials: true });
  }
}
