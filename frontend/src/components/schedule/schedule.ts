import { Component, signal, input } from '@angular/core';
import { ScheduleResponse, Person } from '../../models/schedule-model';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';

type Shift = { day: string; start: string; end: string };

@Component({
  selector: 'app-schedule',
  imports: [ MatSelectModule, MatTableModule ],
  templateUrl: './schedule.html',
  styleUrl: './schedule.scss',
})
export class Schedule {
  data = input.required<ScheduleResponse>();

  selectedPerson = signal<Person | null>(null);
  shifts = signal<Shift[]>([]);
  week = signal(nextIsoWeek());

  private days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'] as const;

  selectPerson(person: Person) {
    this.selectedPerson.set(person);
    this.shifts.set(
      this.days.map(day => {
        const [start, end] = (person[day] ?? '').split('-');
        return { day, start: start ?? '', end: end ?? '' };
      })
    );
  }

  updateTime(i: number, field: 'start' | 'end', value: string) {
    const updated = [...this.shifts()];
    updated[i] = { ...updated[i], [field]: value };
    this.shifts.set(updated);
  }
}

// --- helpers (isolated ISO-week math) ---
function nextIsoWeek(): string {
  const d = new Date();
  d.setDate(d.getDate() + 7);
  const { year, week } = isoWeek(d);
  return `${year}-W${String(week).padStart(2, '0')}`;
}

function isoWeek(date: Date): { year: number; week: number } {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  d.setUTCDate(d.getUTCDate() + 3 - ((d.getUTCDay() + 6) % 7));
  const firstThursday = new Date(Date.UTC(d.getUTCFullYear(), 0, 4));
  const week = 1 + Math.round(
    ((d.getTime() - firstThursday.getTime()) / 86400000 - 3 + ((firstThursday.getUTCDay() + 6) % 7)) / 7
  );
  return { year: d.getUTCFullYear(), week };
}

function toTime(raw: string | undefined): string {
  if (!raw) return '';
  const m = raw.trim().replace('.', ':').match(/^(\d{1,2}):(\d{1,2})$/);
  if (!m) return '';
  return `${m[1].padStart(2, '0')}:${m[2].padStart(2, '0')}`;
}
