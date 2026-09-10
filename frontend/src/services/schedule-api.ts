import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ScheduleResponse } from '../models/schedule-model';

@Injectable({
  providedIn: 'root',
})
export class ScheduleApi {
  http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000';

  createSchedule(): Observable<ScheduleResponse>{
    return this.http.post<ScheduleResponse>(`${this.baseUrl}/schedule`, {});
  };
}
