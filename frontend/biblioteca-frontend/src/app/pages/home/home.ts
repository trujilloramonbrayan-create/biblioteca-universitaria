import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomeComponent implements OnInit {
  stats = {
    totalRecursos: 0,
    prestamosActivos: 0,
    reservasPendientes: 0,
    usuariosActivos: 0
  };

  actividadReciente: any[] = [];
  loading = true;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarEstadisticas();
  }

  cargarEstadisticas(): void {
    // Aquí conectarás con tu API real
    // Por ahora usamos datos de prueba
    this.loading = true;
    
    // Simular carga de datos
    setTimeout(() => {
      this.stats = {
        totalRecursos: 1234,
        prestamosActivos: 89,
        reservasPendientes: 45,
        usuariosActivos: 567
      };
      
      this.actividadReciente = [
        {
          usuario: 'Juan Pérez',
          accion: 'Préstamo',
          recurso: 'Cien años de soledad',
          fecha: 'Hoy, 10:30 AM',
          estado: 'completado'
        },
        {
          usuario: 'María García',
          accion: 'Reserva',
          recurso: 'El principito',
          fecha: 'Hoy, 09:15 AM',
          estado: 'pendiente'
        }
      ];
      
      this.loading = false;
    }, 1000);
  }
}