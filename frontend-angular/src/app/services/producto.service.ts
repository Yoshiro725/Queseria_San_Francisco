import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ProductoLacteo {
  id: string;
  desc_queso: string;
  precio: number;
  totalInventario: number;
}

@Injectable({
  providedIn: 'root'
})
export class ProductoService {
  private apiUrl = 'http://localhost:8000/productos';

  constructor(private http: HttpClient) {}

  // Crear nuevo producto lácteo
  createProducto(producto: Omit<ProductoLacteo, 'id'>): Observable<ProductoLacteo> {
    return this.http.post<ProductoLacteo>(this.apiUrl, producto);
  }

  // Obtener todos los productos
  getProductos(): Observable<ProductoLacteo[]> {
    return this.http.get<ProductoLacteo[]>(this.apiUrl);
  }

  // ✅ ACTUALIZADO: Usar PUT para actualizar producto
  actualizarInventarioProducto(productoId: string, nuevoInventario: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${productoId}`, { 
      totalInventario: nuevoInventario 
    });
  }

  // ✅ MÉTODO ALTERNATIVO usando PATCH en endpoint específico
  actualizarInventarioProductoAlternativo(productoId: string, cantidadProducida: number): Observable<any> {
    return this.http.patch(`${this.apiUrl}/${productoId}/inventario`, { 
      cantidad: cantidadProducida 
    });
  }

  // ✅ OBTENER UN PRODUCTO POR ID
  getProductoById(id: string): Observable<ProductoLacteo> {
    return this.http.get<ProductoLacteo>(`${this.apiUrl}/${id}`);
  }
}