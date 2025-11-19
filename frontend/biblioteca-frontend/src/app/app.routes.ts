import { Routes } from '@angular/router';

export const routes: Routes = [
  { 
    path: '', 
    loadComponent: () => import('./pages/home/home').then(m => m.HomeComponent) 
  },
  { 
    path: 'recursos', 
    loadComponent: () => import('./pages/recursos/recursos').then(m => m.RecursosComponent) 
  },
  { 
    path: 'prestamos', 
    loadComponent: () => import('./pages/prestamos/prestamos').then(m => m.PrestamosComponent) 
  },
  { 
    path: 'reservas', 
    loadComponent: () => import('./pages/reservas/reservas').then(m => m.ReservasComponent) 
  },
  { path: '**', redirectTo: '' }
];