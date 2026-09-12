import { Component, signal } from '@angular/core';
import { Upload } from '../components/upload/upload';

@Component({
  selector: 'app-root',
  imports: [ Upload ],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('frontend');
}
