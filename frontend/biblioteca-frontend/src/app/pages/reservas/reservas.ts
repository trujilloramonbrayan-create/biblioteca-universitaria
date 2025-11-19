import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-reservas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reservas.html',
  styleUrl: './reservas.css'
})
export class ReservasComponent implements OnInit {
  reservas: any[] = [];
  loading: boolean = false;
  error: string = '';
  filtroEstado: string = 'TODOS';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarReservas();
  }

  // GETTERS PARA LOS CONTADORES
  get reservasPendientes(): number {
    return this.reservas.filter(r => r.estado === 'PENDIENTE').length;
  }

  get reservasConfirmadas(): number {
    return this.reservas.filter(r => r.estado === 'CONFIRMADA').length;
  }

  get reservasExpiradas(): number {
    return this.reservas.filter(r => r.estado === 'EXPIRADA').length;
  }

  cargarReservas(): void {
    this.loading = true;
    this.error = '';
    
    // Datos de ejemplo
    setTimeout(() => {
      this.reservas = [
        {
          id: 1,
          usuario: { nombre: 'Laura', apellido: 'Sánchez', email: 'laura@mail.com' },
          recurso: { titulo: 'Harry Potter y la piedra filosofal', autor: 'J.K. Rowling' },
          fecha_reserva: new Date('2025-11-10'),
          fecha_expiracion: new Date('2025-11-17'),
          estado: 'PENDIENTE',
          prioridad: 1
        },
        {
          id: 2,
          usuario: { nombre: 'Pedro', apellido: 'López', email: 'pedro@mail.com' },
          recurso: { titulo: 'El señor de los anillos', autor: 'J.R.R. Tolkien' },
          fecha_reserva: new Date('2025-11-09'),
          fecha_expiracion: new Date('2025-11-16'),
          estado: 'CONFIRMADA',
          prioridad: 1
        },
        {
          id: 3,
          usuario: { nombre: 'Sofia', apellido: 'Torres', email: 'sofia@mail.com' },
          recurso: { titulo: 'Orgullo y prejuicio', autor: 'Jane Austen' },
          fecha_reserva: new Date('2025-11-05'),
          fecha_expiracion: new Date('2025-11-12'),
          estado: 'EXPIRADA',
          prioridad: 2
        },
        {
          id: 4,
          usuario: { nombre: 'Diego', apellido: 'Morales', email: 'diego@mail.com' },
          recurso: { titulo: 'Crónica de una muerte anunciada', autor: 'Gabriel García Márquez' },
          fecha_reserva: new Date('2025-11-11'),
          fecha_expiracion: new Date('2025-11-18'),
          estado: 'PENDIENTE',
          prioridad: 2
        }
      ];
      this.loading = false;
    }, 1000);

    // API real:
    // this.apiService.getReservas().subscribe({...});
  }

  get reservasFiltradas() {
    if (this.filtroEstado === 'TODOS') {
      return this.reservas;
    }
    return this.reservas.filter(r => r.estado === this.filtroEstado);
  }

  confirmarReserva(id: number): void {
    if (confirm('¿Confirmar esta reserva y notificar al usuario?')) {
      console.log('Confirmando reserva:', id);
      // this.apiService.updateReserva(id, { estado: 'CONFIRMADA' }).subscribe(...)
    }
  }

  cancelarReserva(id: number): void {
    if (confirm('¿Cancelar esta reserva?')) {
      console.log('Cancelando reserva:', id);
      // this.apiService.updateReserva(id, { estado: 'CANCELADA' }).subscribe(...)
    }
  }

  eliminarReserva(id: number): void {
    if (confirm('¿Estás seguro de eliminar esta reserva?')) {
      console.log('Eliminando reserva:', id);
      // this.apiService.deleteReserva(id).subscribe(...)
    }
  }

  convertirAPrestamo(id: number): void {
    if (confirm('¿Convertir esta reserva en un préstamo?')) {
      console.log('Convirtiendo a préstamo:', id);
      // Aquí crearías un préstamo desde la reserva
    }
  }

  getEstadoClass(estado: string): string {
    switch(estado) {
      case 'PENDIENTE': return 'bg-warning text-dark';
      case 'CONFIRMADA': return 'bg-success';
      case 'CANCELADA': return 'bg-danger';
      case 'EXPIRADA': return 'bg-secondary';
      default: return 'bg-secondary';
    }
  }

  getDiasRestantes(fechaExpiracion: Date): number {
    const hoy = new Date();
    const fecha = new Date(fechaExpiracion);
    const diff = fecha.getTime() - hoy.getTime();
    return Math.ceil(diff / (1000 * 3600 * 24));
  }

  getPrioridadIcon(prioridad: number): string {
    return prioridad === 1 ? 'bi-star-fill text-warning' : 'bi-star text-muted';
  }
}