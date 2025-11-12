import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NuevaVentaModal } from '../../components/nueva-venta-modal/nueva-venta-modal';

@Component({
  selector: 'app-ventas',
  standalone: true,
  imports: [CommonModule, NuevaVentaModal],
  templateUrl: './ventas.html',
  styleUrl: './ventas.scss',
})
export class Ventas {
  // --- 1. Variable para guardar el tab activo ---
  activeTab: string = 'dia'; // 'dia', 'semana', 'mes', 'año'

  // --- 2. Datos simulados ---
  totalVentas: string = '$4,500';

  // --- 3. Método para cambiar el tab ---
  seleccionarTab(tab: string): void {
    this.activeTab = tab;
    // Aquí, en el futuro, cargarías los datos para ese tab
    // Ej: this.cargarVentasDelDia();
  }

  // --- Lógica para controlar el modal ---
  isVentaModalOpen = false;

  abrirModalNuevaVenta(): void {
    this.isVentaModalOpen = true;
  }

  cerrarModalNuevaVenta(): void {
    this.isVentaModalOpen = false;
  }
}
