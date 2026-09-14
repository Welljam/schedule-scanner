import { Component, inject, signal } from '@angular/core';
import { ScheduleApi } from '../../services/schedule-api';
import { ScheduleResponse } from '../../models/schedule-model';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { Schedule } from '../schedule/schedule';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-upload',
  imports: [ MatProgressSpinnerModule, MatSelectModule, Schedule, MatIconModule],
  templateUrl: './upload.html',
  styleUrl: './upload.scss',
  standalone: true
})
export class Upload {
  private api = inject(ScheduleApi);
  private selectedFile: File | null = null;
  schedule = signal<ScheduleResponse | null>(null);
  fileSelected = false;
  loading = false;
  fileName = '';
  sent = signal(false);

  constructor() {
    const pending = localStorage.getItem('pendingSchedule');
    if (pending) {
      localStorage.removeItem('pendingSchedule');
      this.api.create_event(JSON.parse(pending)).subscribe({
        next: () => this.sent.set(true),
        error: (err) => console.error(err),
      });
    }
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    this.selectedFile = input.files?.[0] ?? null;
    this.fileName = this.selectedFile?.name ?? '';
    this.fileSelected = !!this.selectedFile;
  }

  submit() {
    if (!this.selectedFile) return;
    this.loading = true;
    this.api.uploadSchedule(this.selectedFile).subscribe({
      next: (data) => {this.schedule.set(data); this.loading = false;},
      error: (err) => { console.error(err); this.loading = false; },
    });
  }
}