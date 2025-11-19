import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-recursos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './recursos.html',
  styleUrl: './recursos.css'
})

export class RecursosComponent implements OnInit {

  recursos: any[] = [];
  loading: boolean = false;
  error: string = '';

  // Buscador
  searchTerm: string = '';

  // Modal
  mostrarModal: boolean = false;
  esEdicion: boolean = false;
  recursoEditando: any = null;

  // Formulario ALINEADO con el modelo Recurso de Django
  recursoForm: any = {
    titulo: '',
    autor: '',
    tipo: 'libro',            // choices: libro, revista, articulo, tesis, ebook, revista_digital, video, audio
    formato: 'fisico',        // choices: fisico, digital
    isbn: '',
    codigo_interno: '',
    editorial: '',
    anio_publicacion: new Date().getFullYear(),
    edicion: '',
    idioma: 'Español',
    categoria: '',
    palabras_clave: '',
    materia: '',
    ubicacion: '',
    numero_copias: 1,
    copias_disponibles: 1,
    url_acceso: '',
    estado: 'disponible',     // choices: disponible, prestado, reservado, mantenimiento, extraviado, baja
    descripcion: '',
    resumen: '',
    paginas: null
  };

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarRecursos();
  }

  // ================= CARGAR =================
  cargarRecursos(): void {
    this.loading = true;
    this.error = '';

    this.apiService.getRecursos().subscribe({
      next: (data) => {
        // por si usas paginación en DRF
        this.recursos = Array.isArray(data) ? data : data.results || data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar recursos:', err);
        this.error = 'Error al cargar los recursos';
        this.loading = false;
      }
    });
  }

  // ================= FILTRADO =================
  get recursosFiltrados(): any[] {
    const term = this.searchTerm.toLowerCase().trim();
    if (!term) return this.recursos;

    return this.recursos.filter((r) =>
      (r.titulo && r.titulo.toLowerCase().includes(term)) ||
      (r.autor && r.autor.toLowerCase().includes(term)) ||
      (r.isbn && r.isbn.toLowerCase().includes(term))
    );
  }

  limpiarFiltros(): void {
    this.searchTerm = '';
  }

  // ================= MODAL =================
  abrirModalNuevo(): void {
    this.esEdicion = false;
    this.recursoEditando = null;
    this.recursoForm = {
      titulo: '',
      autor: '',
      tipo: 'libro',
      formato: 'fisico',
      isbn: '',
      codigo_interno: '',
      editorial: '',
      anio_publicacion: new Date().getFullYear(),
      edicion: '',
      idioma: 'Español',
      categoria: '',
      palabras_clave: '',
      materia: '',
      ubicacion: '',
      numero_copias: 1,
      copias_disponibles: 1,
      url_acceso: '',
      estado: 'disponible',
      descripcion: '',
      resumen: '',
      paginas: null
    };
    this.mostrarModal = true;
  }

  abrirModalEditar(recurso: any): void {
    this.esEdicion = true;
    this.recursoEditando = recurso;
    this.recursoForm = {
      titulo: recurso.titulo || '',
      autor: recurso.autor || '',
      tipo: recurso.tipo || 'libro',
      formato: recurso.formato || 'fisico',
      isbn: recurso.isbn || '',
      codigo_interno: recurso.codigo_interno || '',
      editorial: recurso.editorial || '',
      anio_publicacion: recurso.anio_publicacion || new Date().getFullYear(),
      edicion: recurso.edicion || '',
      idioma: recurso.idioma || 'Español',
      categoria: recurso.categoria || '',
      palabras_clave: recurso.palabras_clave || '',
      materia: recurso.materia || '',
      ubicacion: recurso.ubicacion || '',
      numero_copias: recurso.numero_copias ?? 1,
      copias_disponibles: recurso.copias_disponibles ?? recurso.numero_copias ?? 1,
      url_acceso: recurso.url_acceso || '',
      estado: recurso.estado || 'disponible',
      descripcion: recurso.descripcion || '',
      resumen: recurso.resumen || '',
      paginas: recurso.paginas ?? null
    };
    this.mostrarModal = true;
  }

  cerrarModal(): void {
    this.mostrarModal = false;
  }

  // ================= GUARDAR =================
  guardarRecurso(): void {
    // Validación básica en el FRONT
    if (
      !this.recursoForm.titulo ||
      !this.recursoForm.autor ||
      !this.recursoForm.tipo ||
      !this.recursoForm.codigo_interno ||
      !this.recursoForm.anio_publicacion ||
      !this.recursoForm.categoria
    ) {
      alert('Título, autor, tipo, código interno, año de publicación y categoría son obligatorios');
      return;
    }

    // Normalizar numéricos
    this.recursoForm.anio_publicacion = Number(this.recursoForm.anio_publicacion);
    this.recursoForm.numero_copias = Number(this.recursoForm.numero_copias || 1);
    this.recursoForm.copias_disponibles = Number(
      this.recursoForm.copias_disponibles ?? this.recursoForm.numero_copias
    );

    const payload = { ...this.recursoForm };

    if (this.esEdicion && this.recursoEditando) {
      // EDITAR
      this.apiService.updateRecurso(this.recursoEditando.id, payload).subscribe({
        next: () => {
          alert('Recurso actualizado correctamente');
          this.cerrarModal();
          this.cargarRecursos();
        },
        error: (err) => {
          console.error('Error al actualizar recurso (body):', err.error);
          alert('Error al actualizar el recurso');
        }
      });
    } else {
      // CREAR
      this.apiService.createRecurso(payload).subscribe({
        next: () => {
          alert('Recurso creado correctamente');
          this.cerrarModal();
          this.cargarRecursos();
        },
        error: (err) => {
          console.error('Error al crear recurso (body):', err.error);
          alert('Error al crear el recurso');
        }
      });
    }
  }

  // ================= ELIMINAR =================
  eliminarRecurso(id: number, titulo?: string): void {
    if (!confirm(`¿Estás seguro de eliminar el recurso "${titulo || ''}"?`)) return;

    this.apiService.deleteRecurso(id).subscribe({
      next: () => this.cargarRecursos(),
      error: (err) => {
        console.error('Error al eliminar:', err);
        alert('Error al eliminar el recurso');
      }
    });
  }

  // ================= ESTILOS DE ESTADO =================
  getEstadoBadge(recurso: any): string {
    switch (recurso.estado) {
      case 'disponible':
        return 'bg-success';
      case 'prestado':
        return 'bg-danger';
      case 'reservado':
        return 'bg-warning text-dark';
      case 'mantenimiento':
        return 'bg-secondary';
      case 'extraviado':
        return 'bg-dark';
      case 'baja':
        return 'bg-secondary';
      default:
        return 'bg-secondary';
    }
  }

  getEstadoTexto(recurso: any): string {
    switch (recurso.estado) {
      case 'disponible':
        return 'Disponible';
      case 'prestado':
        return 'Prestado';
      case 'reservado':
        return 'Reservado';
      case 'mantenimiento':
        return 'Mantenimiento';
      case 'extraviado':
        return 'Extraviado';
      case 'baja':
        return 'Dado de baja';
      default:
        return 'Desconocido';
    }
  }
}
