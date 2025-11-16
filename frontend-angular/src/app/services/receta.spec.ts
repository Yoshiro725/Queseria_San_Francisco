import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Receta } from '../models/receta.interface';

@Injectable({
  providedIn: 'root'
})
export class RecetaService {
  private apiUrl = 'http://localhost:8000/recetas';
  
  // BehaviorSubject para mantener el estado de las recetas
  private recetasSubject = new BehaviorSubject<Receta[]>([]);
  public recetas$ = this.recetasSubject.asObservable();
  
  // Flag para saber si ya cargamos las recetas
  private recetasCargadas = false;

  constructor(private http: HttpClient) {}

  // Obtener todas las recetas (usando el BehaviorSubject)
  getRecetas(): Observable<Receta[]> {
    // Si no hemos cargado las recetas, las cargamos
    if (!this.recetasCargadas) {
      this.cargarRecetasIniciales();
    }
    return this.recetas$;
  }

  // Cargar recetas al iniciar el servicio
  private cargarRecetasIniciales(): void {
    this.http.get<Receta[]>(this.apiUrl).subscribe({
      next: (recetas) => {
        this.recetasSubject.next(recetas);
        this.recetasCargadas = true;
      },
      error: (error) => {
        console.error('Error cargando recetas iniciales:', error);
        this.recetasSubject.next([]); // Emitir array vacío en caso de error
      }
    });
  }

  // Obtener una receta por ID
  getRecetaById(id: string): Observable<Receta> {
    return this.http.get<Receta>(`${this.apiUrl}/${id}`);
  }

  // Crear nueva receta (ACTUALIZADO)
  createReceta(receta: Receta): Observable<Receta> {
    return this.http.post<Receta>(this.apiUrl, receta).pipe(
      tap((nuevaReceta) => {
        // Actualizar la lista de recetas después de crear
        this.actualizarListaRecetas();
      })
    );
  }

  // Actualizar receta (ACTUALIZADO)
  updateReceta(id: string, receta: Receta): Observable<Receta> {
    return this.http.put<Receta>(`${this.apiUrl}/${id}`, receta).pipe(
      tap(() => {
        this.actualizarListaRecetas();
      })
    );
  }

  // Eliminar receta (ACTUALIZADO)
  deleteReceta(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        this.actualizarListaRecetas();
      })
    );
  }

  // Cambiar estado (ACTUALIZADO)
  toggleRecetaEstado(id: string, estado: boolean): Observable<any> {
    return this.http.patch(`${this.apiUrl}/${id}/estado`, { estado }).pipe(
      tap(() => {
        this.actualizarListaRecetas();
      })
    );
  }

  // Método privado para actualizar la lista de recetas
  private actualizarListaRecetas(): void {
    this.http.get<Receta[]>(this.apiUrl).subscribe({
      next: (recetas) => {
        this.recetasSubject.next(recetas);
      },
      error: (error) => {
        console.error('Error actualizando lista de recetas:', error);
      }
    });
  }

  // ✅ MÉTODO AÑADIDO: Para forzar recarga manual
  recargarRecetas(): void {
    this.actualizarListaRecetas();
  }

  // Limpiar cache (opcional, para cuando quieras forzar recarga)
  limpiarCache(): void {
    this.recetasCargadas = false;
  }
}