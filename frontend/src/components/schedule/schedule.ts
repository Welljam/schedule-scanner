import { Component, signal, input, inject} from '@angular/core';
import { ScheduleResponse, Person, CreateEventsRequest, Days} from '../../models/schedule-model';
import { MatSelectModule } from '@angular/material/select';
import { ScheduleApi } from '../../services/schedule-api';

@Component({
  selector: 'app-schedule',
  imports: [ MatSelectModule ],
  templateUrl: './schedule.html',
  styleUrl: './schedule.scss',
})
export class Schedule {
  data = input.required<ScheduleResponse>();
  private api = inject(ScheduleApi);
  selectedPerson = signal<Person | null>(null);
  shifts = signal<Days[]>([]);
  week = signal(nextIsoWeek());
  sent = signal<boolean>(false);

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

  sendSchedule(){
    const person = this.selectedPerson();
    if (!person) return;
    
    const createEvent: CreateEventsRequest = {
      name: person.name ?? 'Schedule',
      week: this.week(),
      days: this.shifts().filter(s => s.start && s.end),
    };

    this.api.create_event(createEvent).subscribe({
      next: () => this.sent.set(true),
      error: (err) => {
        if (err.status === 401) {
          window.location.href = 'http://localhost:8000/login';
        } else {
          console.error(err);
        }
      },
    })

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
