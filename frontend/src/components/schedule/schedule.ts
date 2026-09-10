import { Component, inject, signal } from '@angular/core';
import { ScheduleApi } from '../../services/schedule-api';
import { ScheduleResponse } from '../../models/schedule-model';

@Component({
  selector: 'app-schedule',
  imports: [],
  templateUrl: './schedule.html',
  styleUrl: './schedule.scss',
})
export class Schedule {
  private api = inject(ScheduleApi);
  schedule = signal<ScheduleResponse | null>(null);

  load(){
    this.api.createSchedule().subscribe({
      next: (data) => this.schedule.set(data),
      error: (err) => console.error(err),
    })
  }

}
