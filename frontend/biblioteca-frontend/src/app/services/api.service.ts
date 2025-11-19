import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    });
  }

  // ============ RECURSOS (USA ROUTER) ============
  getRecursos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/recursos/`, { headers: this.getHeaders() });
  }

  getRecurso(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/recursos/${id}/`, { headers: this.getHeaders() });
  }

  createRecurso(recurso: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/recursos/`, recurso, { headers: this.getHeaders() });
  }

  updateRecurso(id: number, recurso: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/recursos/${id}/`, recurso, { headers: this.getHeaders() });
  }

  deleteRecurso(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/recursos/${id}/`, { headers: this.getHeaders() });
  }

  // ============ PRÉSTAMOS (TUS RUTAS REALES) ============
  getPrestamos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/prestamos/`, { headers: this.getHeaders() });
  }

  createPrestamo(prestamo: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/prestamos/crear/`, prestamo, { headers: this.getHeaders() });
  }

  updatePrestamo(id: number, prestamo: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/prestamos/${id}/actualizar/`, prestamo, { headers: this.getHeaders() });
  }

  deletePrestamo(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/prestamos/${id}/eliminar/`, { headers: this.getHeaders() });
  }

  // ============ RESERVAS (VERIFICA TUS URLS DE DJANGO) ============
  getReservas(): Observable<any> {
    return this.http.get(`${this.apiUrl}/reservas/`, { headers: this.getHeaders() });
  }

  getReserva(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/reservas/${id}/`, { headers: this.getHeaders() });
  }

  createReserva(reserva: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/reservas/`, reserva, { headers: this.getHeaders() });
  }

  updateReserva(id: number, reserva: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/reservas/${id}/`, reserva, { headers: this.getHeaders() });
  }

  deleteReserva(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/reservas/${id}/`, { headers: this.getHeaders() });
  }

  // ============ USUARIOS (USA ROUTER) ============
  getUsuarios(): Observable<any> {
    return this.http.get(`${this.apiUrl}/usuarios/`, { headers: this.getHeaders() });
  }

  getUsuario(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/usuarios/${id}/`, { headers: this.getHeaders() });
  }

  createUsuario(usuario: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/usuarios/`, usuario, { headers: this.getHeaders() });
  }

  updateUsuario(id: number, usuario: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/usuarios/${id}/`, usuario, { headers: this.getHeaders() });
  }

  deleteUsuario(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/usuarios/${id}/`, { headers: this.getHeaders() });
  }
}
