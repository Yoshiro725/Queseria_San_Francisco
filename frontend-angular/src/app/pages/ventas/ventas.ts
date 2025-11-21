import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NuevaVentaModal } from '../../components/nueva-venta-modal/nueva-venta-modal';
import { FormsModule } from '@angular/forms';
import { VentasService, Venta, DetalleVenta } from '../../services/ventas.service';
import { Subscription } from 'rxjs';

interface VentaLocal {
  id: string;
  fecha: string;
  cliente: string;
  total: number;
  IVA: number;
  productos: DetalleVenta[];
}

@Component({
  selector: 'app-ventas',
  standalone: true,
  imports: [CommonModule, NuevaVentaModal, FormsModule],
  templateUrl: './ventas.html',
  styleUrl: './ventas.scss',
})
export class Ventas implements OnInit, OnDestroy {
  listaVentas: VentaLocal[] = [];
  ventasFiltradas: VentaLocal[] = [];
  ventaSeleccionada: VentaLocal | null = null;
  cargando = true;
  error: string = '';

  // Filtros
  filtroFechaDesde: string = '';
  filtroFechaHasta: string = '';
  filtroCliente: string = '';

  private ventasSubscription: Subscription | undefined;

  get totalVentas(): number {
    return this.ventasFiltradas.reduce((sum, venta) => sum + venta.total, 0);
  }

  constructor(private ventasService: VentasService) {}

  ngOnInit() {
    this.cargarVentasReactivamente();
  }

  ngOnDestroy() {
    if (this.ventasSubscription) {
      this.ventasSubscription.unsubscribe();
    }
  }

  cargarVentasReactivamente() {
    this.cargando = true;
    this.error = '';
    
    this.ventasSubscription = this.ventasService.obtenerVentas().subscribe({
      next: (ventas: Venta[]) => {
        this.listaVentas = this.transformarVentas(ventas);
        this.ventasFiltradas = [...this.listaVentas];
        this.cargando = false;
        console.log('✅ Ventas cargadas:', this.listaVentas.length);
      },
      error: (error) => {
        console.error('❌ Error cargando ventas:', error);
        this.error = 'Error al cargar las ventas';
        this.cargando = false;
        this.listaVentas = [];
        this.ventasFiltradas = [];
      }
    });
  }

  private transformarVentas(ventas: Venta[]): VentaLocal[] {
    return ventas.map((venta: Venta) => ({
      id: venta.id,
      fecha: this.formatearFecha(venta.fecha_venta),
      cliente: venta.cliente_nombre, // ✅ USAR NOMBRE DEL CLIENTE
      total: venta.total || 0,
      IVA: venta.IVA || 0,
      productos: venta.detalle || []
    }));
  }

  formatearFecha(fechaString: string): string {
    try {
      return new Date(fechaString).toISOString().split('T')[0];
    } catch {
      return new Date().toISOString().split('T')[0];
    }
  }

  formatearMoneda(monto: number): string {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN'
    }).format(monto);
  }

  seleccionarVenta(venta: VentaLocal): void {
    this.ventaSeleccionada = this.ventaSeleccionada === venta ? null : venta;
  }

  aplicarFiltros(): void {
    let ventas = [...this.listaVentas];

    if (this.filtroCliente) {
      ventas = ventas.filter(venta =>
        venta.cliente.toLowerCase().includes(this.filtroCliente.toLowerCase())
      );
    }

    if (this.filtroFechaDesde) {
      ventas = ventas.filter(venta => 
        new Date(venta.fecha) >= new Date(this.filtroFechaDesde)
      );
    }

    if (this.filtroFechaHasta) {
      ventas = ventas.filter(venta => 
        new Date(venta.fecha) <= new Date(this.filtroFechaHasta)
      );
    }

    this.ventasFiltradas = ventas;
  }

  limpiarFiltros(): void {
    this.filtroFechaDesde = '';
    this.filtroFechaHasta = '';
    this.filtroCliente = '';
    this.ventasFiltradas = [...this.listaVentas];
  }

  recargarManual(): void {
    this.ventasService.recargarVentas();
  }

  // Modal
  isVentaModalOpen = false;

  abrirModalNuevaVenta(): void {
    this.isVentaModalOpen = true;
  }

  cerrarModalNuevaVenta(): void {
    this.isVentaModalOpen = false;
  }

  onVentaGuardada(totalDeLaVenta: number): void {
    console.log('💰 Venta guardada con total:', totalDeLaVenta);
    this.cerrarModalNuevaVenta();
  }
}