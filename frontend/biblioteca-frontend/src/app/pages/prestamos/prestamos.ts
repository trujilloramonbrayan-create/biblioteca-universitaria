import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-prestamos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './prestamos.html',
  styleUrl: './prestamos.css'
})
export class PrestamosComponent implements OnInit {

  prestamos: any[] = [];
  usuarios: any[] = [];
  recursos: any[] = [];

  loading: boolean = false;
  error: string = '';
  filtroEstado: string = 'TODOS';

  // Para usar Math.abs en el HTML
  Math = Math;

  // Control del modal sin Bootstrap JS
  mostrarModal: boolean = false;

  // Datos del nuevo préstamo (formulario)
  nuevoPrestamo: any = {
    usuario_id: null,
    recurso_id: null,
    fecha_prestamo: '',
    fecha_devolucion_estimada: ''
  };

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarPrestamos();
    this.cargarUsuarios();
    this.cargarRecursos();
  }

  // ========= MODAL (sin document, solo Angular) =========
  abrirModal(): void {
    this.mostrarModal = true;
  }

  cerrarModal(): void {
    this.mostrarModal = false;
  }

  // ========= CONTADORES =========
  get prestamosActivos(): number {
    return this.prestamos.filter(p => p.estado === 'ACTIVO').length;
  }

  get prestamosVencidos(): number {
    return this.prestamos.filter(p => p.estado === 'VENCIDO').length;
  }

  get prestamosDevueltos(): number {
    return this.prestamos.filter(p => p.estado === 'DEVUELTO').length;
  }

  // ========= CARGAR DATOS =========
  cargarPrestamos(): void {
    this.loading = true;
    this.error = '';

    this.apiService.getPrestamos().subscribe({
      next: (data) => {
        this.prestamos = Array.isArray(data) ? data : data.results || [];
        this.loading = false;
      },
      error: () => {
        this.error = 'Error al cargar los préstamos';
        this.loading = false;
      }
    });
  }

  cargarUsuarios(): void {
    this.apiService.getUsuarios().subscribe({
      next: (data) => {
        console.log('Respuesta /api/usuarios/', data);
        this.usuarios = Array.isArray(data) ? data : data.results || data;
      },
      error: (err) => {
        console.error('Error cargando usuarios', err);
      }
    });
  }
  

  cargarRecursos(): void {
    this.apiService.getRecursos().subscribe({
      next: (data) => {
        this.recursos = Array.isArray(data) ? data : data.results || data;
      },
      error: () => {
        console.error('Error cargando recursos');
      }
    });
  }

  // ========= FILTRADO =========
  get prestamosFiltrados() {
    if (this.filtroEstado === 'TODOS') return this.prestamos;
    return this.prestamos.filter(p => p.estado === this.filtroEstado);
  }

  // ========= CREAR PRÉSTAMO =========
  guardarPrestamo(): void {
    if (!this.nuevoPrestamo.usuario_id ||
        !this.nuevoPrestamo.recurso_id ||
        !this.nuevoPrestamo.fecha_prestamo ||
        !this.nuevoPrestamo.fecha_devolucion_estimada) {
      alert('Todos los campos son obligatorios');
      return;
    }

    this.apiService.createPrestamo(this.nuevoPrestamo).subscribe({
      next: () => {
        alert('Préstamo creado correctamente');
        this.cerrarModal();
        this.cargarPrestamos();

        // Reseteamos el formulario
        this.nuevoPrestamo = {
          usuario_id: null,
          recurso_id: null,
          fecha_prestamo: '',
          fecha_devolucion_estimada: ''
        };
      },
      error: (err) => {
        console.error(err);
        alert('Error al crear el préstamo');
      }
    });
  }

  // ========= DEVOLVER =========
  devolverPrestamo(id: number): void {
    if (!confirm('¿Confirmar devolución de este préstamo?')) return;

    const hoy = new Date();
    const fechaFormateada = hoy.toISOString().split('T')[0];

    this.apiService.updatePrestamo(id, {
      estado: 'DEVUELTO',
      fecha_devolucion_real: fechaFormateada
    }).subscribe({
      next: () => {
        alert('Préstamo devuelto correctamente');
        this.cargarPrestamos();
      },
      error: () => alert('Error devolviendo préstamo')
    });
  }

  // ========= RENOVAR (SUMA 7 días) =========
  renovarPrestamo(id: number): void {
    if (!confirm('¿Renovar este préstamo por 7 días más?')) return;

    const prestamo = this.prestamos.find(p => p.id === id);
    if (!prestamo) return;

    const nuevaFecha = new Date(prestamo.fecha_devolucion_estimada);
    nuevaFecha.setDate(nuevaFecha.getDate() + 7);
    const fechaFormateada = nuevaFecha.toISOString().split('T')[0];

    this.apiService.updatePrestamo(id, { fecha_devolucion_estimada: fechaFormateada }).subscribe({
      next: () => {
        alert('Préstamo renovado 7 días más');
        this.cargarPrestamos();
      },
      error: () => alert('Error renovando préstamo')
    });
  }

  // ========= ELIMINAR =========
  eliminarPrestamo(id: number): void {
    if (!confirm('¿Estás seguro de eliminar este préstamo?')) return;

    this.apiService.deletePrestamo(id).subscribe({
      next: () => {
        alert('Préstamo eliminado');
        this.cargarPrestamos();
      },
      error: () => alert('Error eliminando préstamo')
    });
  }

  // ========= ESTILOS DE ESTADO =========
  getEstadoClass(estado: string): string {
    switch (estado) {
      case 'ACTIVO': return 'bg-success';
      case 'VENCIDO': return 'bg-danger';
      case 'DEVUELTO': return 'bg-secondary';
      default: return 'bg-dark';
    }
  }

  // ========= CÁLCULO DÍAS RESTANTES =========
  getDiasRestantes(fechaDevolucion: Date): number {
    const hoy = new Date();
    const fecha = new Date(fechaDevolucion);
    const diff = fecha.getTime() - hoy.getTime();
    return Math.ceil(diff / (1000 * 3600 * 24));
  }
}
