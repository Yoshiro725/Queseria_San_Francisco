import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NuevaVentaModal } from '../../components/nueva-venta-modal/nueva-venta-modal';
import { FormsModule } from '@angular/forms';

// 1. Definimos la estructura de una venta
export interface Venta {
  id: number;
  fecha: string;
  cliente: string;
  total: number;
  productos: { nombre: string; cantidad: number; precio: number }[];
}

@Component({
  selector: 'app-ventas',
  standalone: true,
  imports: [CommonModule, NuevaVentaModal, FormsModule], // Se añade FormsModule
  templateUrl: './ventas.html',
  styleUrl: './ventas.scss',
})
export class Ventas {
  // --- 1. Variable para guardar el tab activo ---
  activeTab: string = 'dia'; // 'dia', 'semana', 'mes', 'año'

  // --- 2. Datos de ventas simulados ---
  listaVentas: Venta[] = [
    { id: 1, fecha: '2024-05-20', cliente: 'Ana García', total: 200, productos: [{ nombre: 'Queso Fresco 1kg', cantidad: 1, precio: 90 }, { nombre: 'Quesillo 1kg', cantidad: 1, precio: 110 }] },
    { id: 2, fecha: '2024-05-20', cliente: 'Cliente General', total: 45, productos: [{ nombre: 'Requesón 500g', cantidad: 1, precio: 45 }] },
    { id: 3, fecha: '2024-05-21', cliente: 'Luis Martinez', total: 180, productos: [{ nombre: 'Queso Fresco 1kg', cantidad: 2, precio: 90 }] },
    { id: 4, fecha: '2024-05-22', cliente: 'Ana García', total: 80, productos: [{ nombre: 'Crema 1L', cantidad: 1, precio: 80 }] },
  ];
  ventasFiltradas: Venta[] = this.listaVentas; // Al inicio, mostramos todas
  ventaSeleccionada: Venta | null = null;

  // --- Propiedades para los filtros ---
  filtroFechaDesde: string = '';
  filtroFechaHasta: string = '';
  filtroCliente: string = '';

  // --- Propiedad para el total calculado ---
  get totalVentas(): number {
    return this.ventasFiltradas.reduce((sum, venta) => sum + venta.total, 0);
  }

  // --- 3. Método para cambiar el tab ---
  seleccionarTab(tab: string): void {
    this.activeTab = tab;
    // Aquí, en el futuro, cargarías los datos para ese tab
    // Ej: this.cargarVentasDelDia();
  }

  // 4. Método para seleccionar una venta y ver sus detalles
  seleccionarVenta(venta: Venta): void {
    if (this.ventaSeleccionada === venta) {
      this.ventaSeleccionada = null; // Si se hace clic de nuevo, se deselecciona
    } else {
      this.ventaSeleccionada = venta;
    }
  }

  // 5. Método para aplicar los filtros
  aplicarFiltros(): void {
    let ventas = [...this.listaVentas]; // Copiamos la lista original para no modificarla

    // Filtrar por cliente
    if (this.filtroCliente) {
      ventas = ventas.filter(venta =>
        venta.cliente.toLowerCase().includes(this.filtroCliente.toLowerCase())
      );
    }

    // Filtrar por fecha desde
    if (this.filtroFechaDesde) {
      ventas = ventas.filter(venta => new Date(venta.fecha) >= new Date(this.filtroFechaDesde));
    }

    // Filtrar por fecha hasta
    if (this.filtroFechaHasta) {
      ventas = ventas.filter(venta => new Date(venta.fecha) <= new Date(this.filtroFechaHasta));
    }

    this.ventasFiltradas = ventas;
  }

  limpiarFiltros(): void {
    this.filtroFechaDesde = '';
    this.filtroFechaHasta = '';
    this.filtroCliente = '';
    this.ventasFiltradas = [...this.listaVentas]; // Restauramos la lista completa
  }

  // --- Lógica para controlar el modal ---
  isVentaModalOpen = false;

  abrirModalNuevaVenta(): void {
    this.isVentaModalOpen = true;
  }

  cerrarModalNuevaVenta(): void {
    this.isVentaModalOpen = false;
  }

  onVentaGuardada(totalDeLaVenta: number): void {
    // Simulamos la creación de una nueva venta para agregarla a la lista
    const nuevaVenta: Venta = {
      id: this.listaVentas.length + 1,
      fecha: new Date().toISOString().split('T')[0], // Fecha de hoy
      cliente: 'Cliente Modal', // Podrías pasar el cliente desde el modal también
      total: totalDeLaVenta,
      productos: [] // En una implementación real, pasarías los productos
    };
    this.listaVentas.unshift(nuevaVenta); // Agregamos la nueva venta al inicio de la lista
    this.ventasFiltradas = this.listaVentas; // Actualizamos la lista filtrada
    console.log(`Venta registrada por ${totalDeLaVenta}.`);
    this.cerrarModalNuevaVenta();
  }
}
