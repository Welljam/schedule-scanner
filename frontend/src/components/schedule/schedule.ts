import { Component, inject, signal, input } from '@angular/core';
import { ScheduleResponse } from '../../models/schedule-model';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-schedule',
  imports: [ MatSelectModule ],
  templateUrl: './schedule.html',
  styleUrl: './schedule.scss',
})
export class Schedule {
  data = input.required<ScheduleResponse>();



}
