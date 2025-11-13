import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Receta } from '../models/receta.interface';

@Injectable({
  providedIn: 'root'
})
export class RecetaService {
  private apiUrl = 'http://localhost:8000/recetas'; // URL de tu FastAPI

  constructor(private http: HttpClient) {}

  // Obtener todas las recetas
  getRecetas(): Observable<Receta[]> {
    return this.http.get<Receta[]>(this.apiUrl);
  }

  // Obtener una receta por ID
  getRecetaById(id: string): Observable<Receta> {
    return this.http.get<Receta>(`${this.apiUrl}/${id}`);
  }

  // Crear nueva receta
  createReceta(receta: Receta): Observable<Receta> {
    return this.http.post<Receta>(this.apiUrl, receta);
  }

  // Actualizar receta
  updateReceta(id: string, receta: Receta): Observable<Receta> {
    return this.http.put<Receta>(`${this.apiUrl}/${id}`, receta);
  }

  // Eliminar receta
  deleteReceta(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  // Cambiar estado (Activo/Inactivo)
  toggleRecetaEstado(id: string, estado: boolean): Observable<any> {
    return this.http.patch(`${this.apiUrl}/${id}/estado`, { estado });
  }
}