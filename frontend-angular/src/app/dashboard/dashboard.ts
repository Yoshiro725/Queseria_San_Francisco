//   src/app/dashboard/dashboard.ts

import { Component } from '@angular/core';
// --- 1. Añade estas 3 líneas ---
import { CommonModule } from '@angular/common';
import { StatCard } from '../components/stat-card/stat-card';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  // --- 2. Modifica esta línea de imports ---
  imports: [CommonModule, StatCard],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard {
  // Aquí pondremos los datos de las tarjetas
}