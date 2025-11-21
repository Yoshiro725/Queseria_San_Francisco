import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface DetalleVenta {
  producto_id: string;
  cantidad: number;
  precioVenta: number;
  nombre_producto?: string;
  subtotal?: number;
}

export interface Venta {
  id: string; // ✅ Solo 'id', sin '_id'
  fecha_venta: string;
  cliente_id: string;
  total: number;
  IVA: number;
  detalle: DetalleVenta[];
}

export interface VentaCreate {
  fecha_venta: string;
  cliente_id: string;
  total: number;
  IVA: number;
  detalle: DetalleVenta[];
}

@Injectable({
  providedIn: 'root'
})
export class VentasService {
  private apiUrl = 'http://localhost:8000/ventas';
  
  private ventasSubject = new BehaviorSubject<Venta[]>([]);
  public ventas$ = this.ventasSubject.asObservable();

  constructor(private http: HttpClient) {
    this.cargarVentasIniciales();
  }

  private cargarVentasIniciales(): void {
    this.http.get<Venta[]>(this.apiUrl).subscribe({
      next: (ventas) => {
        console.log('📦 Ventas cargadas:', ventas);
        const ventasConSubtotales = ventas.map(venta => ({
          ...venta,
          detalle: venta.detalle.map(detalle => ({
            ...detalle,
            subtotal: detalle.cantidad * detalle.precioVenta
          }))
        }));
        this.ventasSubject.next(ventasConSubtotales);
      },
      error: (error) => {
        console.error('❌ Error cargando ventas:', error);
        this.ventasSubject.next([]);
      }
    });
  }

  obtenerVentas(): Observable<Venta[]> {
    return this.ventas$;
  }

  obtenerVentaPorId(id: string): Observable<Venta> {
    return this.http.get<Venta>(`${this.apiUrl}/${id}`);
  }

  crearVenta(venta: VentaCreate): Observable<Venta> {
    return this.http.post<Venta>(this.apiUrl, venta).pipe(
      tap((nuevaVenta) => {
        console.log('✅ Venta creada:', nuevaVenta);
        this.cargarVentasIniciales();
      })
    );
  }

  recargarVentas(): void {
    this.cargarVentasIniciales();
  }
}