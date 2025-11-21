import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Insumo {
  id: string;
  nombre_insumo: string;
  unidad: string;
  stock_actual: number;
  stock_minimo: number;
  costo_unitario: number;
}

@Injectable({
  providedIn: 'root'
})
export class InsumoService {
  private apiUrl = 'http://localhost:8000/insumos';

  constructor(private http: HttpClient) {}

  // Obtener todos los insumos
  getInsumos(): Observable<Insumo[]> {
    return this.http.get<Insumo[]>(this.apiUrl);
  }

  // Obtener un insumo por ID
  getInsumoById(id: string): Observable<Insumo> {
    return this.http.get<Insumo>(`${this.apiUrl}/${id}`);
  }

  // ✅ ACTUALIZADO: Usar PUT en lugar de PATCH
  actualizarStockInsumo(insumoId: string, nuevoStock: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${insumoId}`, { 
      stock_actual: nuevoStock 
    });
  }

  // ✅ MÉTODO ALTERNATIVO usando PATCH en endpoint específico
  actualizarStockInsumoAlternativo(insumoId: string, nuevoStock: number): Observable<any> {
    return this.http.patch(`${this.apiUrl}/${insumoId}/stock`, { 
      stock_actual: nuevoStock 
    });
  }
}