//   src/app/app.routes.ts

import { Routes } from '@angular/router';
import { Dashboard } from './dashboard/dashboard';
import { Produccion } from './pages/produccion/produccion'; //agregamos el componente inventarion 

export const routes: Routes = [
    { 
        path: '', 
        redirectTo: 'dashboard', 
        pathMatch: 'full' 
    },
    { 
        path: 'dashboard', 
        component: Dashboard 
    },
    {
        path: 'produccion', component: Produccion
    },

];