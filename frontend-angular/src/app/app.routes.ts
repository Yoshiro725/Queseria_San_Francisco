//   src/app/app.routes.ts

import { Routes } from '@angular/router';
import { Dashboard } from './dashboard/dashboard';
import { Produccion } from './pages/produccion/produccion'; //agregamos el componente inventarion 
import { Ventas } from './pages/ventas/ventas';
import { Reportes } from './pages/reportes/reportes';

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
        path: 'produccion', 
        component: Produccion
    },
    {  
        path: 'ventas', 
        component: Ventas 
    },
    {
        path: 'reportes', 
        component: Reportes
    },

];