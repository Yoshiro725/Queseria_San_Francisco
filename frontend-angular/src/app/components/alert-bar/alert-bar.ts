//   src/app/components/alert-bar/alert-bar.ts

import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alert-bar',
  standalone: true,
  imports: [CommonModule], // <-- Necesitamos CommonModule para *ngIf y *ngFor
  templateUrl: './alert-bar.html',
  styleUrl: './alert-bar.scss'
})
export class AlertBar {
  message = input<string>('ALERTA');

}