//   src/app/app.routes.ts

import { Routes } from '@angular/router';
import { Dashboard } from './dashboard/dashboard';

export const routes: Routes = [
    
    // --- 2. Añade estas dos rutas ---
    
    // Si la ruta está vacía (ej. localhost:4200), redirige a /dashboard
    { 
        path: '', 
        redirectTo: 'dashboard', 
        pathMatch: 'full' 
    },
    
    // Cuando la ruta sea /dashboard, carga el Dashboard
    { 
        path: 'dashboard', 
        component: Dashboard 
    },

];