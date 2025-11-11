import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

// Definimos una interfaz para la estructura de nuestros insumos
export interface Insumo {
  nombre: string;
  stockActual: number;
  unidad: string;
  estado: 'ok' | 'bajo' | 'agotado';
  categoria: 'Materia Prima' | 'Embalaje' | 'Ingrediente' | 'Derivado';
}

@Component({
  selector: 'app-inventario',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inventario.html',
  styleUrl: './inventario.scss',
})
export class Inventario {
  // Lista de insumos de prueba que coincide con tus categorías de filtro
  listaInsumos: Insumo[] = [
    { nombre: 'Leche entera', stockActual: 2500, unidad: 'L', estado: 'ok', categoria: 'Materia Prima' },
    { nombre: 'Bolsas de empaque', stockActual: 500, unidad: 'unidades', estado: 'ok', categoria: 'Embalaje' },
    { nombre: 'Sal', stockActual: 8, unidad: 'kg', estado: 'bajo', categoria: 'Ingrediente' },
    { nombre: 'Cuajo', stockActual: 0, unidad: 'L', estado: 'agotado', categoria: 'Ingrediente' },
    { nombre: 'Suero de leche', stockActual: 50, unidad: 'L', estado: 'ok', categoria: 'Derivado' },
  ];

  insumoSeleccionado: Insumo | null = null;

  // Método para seleccionar o deseleccionar un insumo
  seleccionarInsumo(insumo: Insumo): void {
    if (this.insumoSeleccionado === insumo) {
      // Si el insumo ya está seleccionado, lo deseleccionamos (lo volvemos null)
      this.insumoSeleccionado = null;
    } else {
      // Si es un insumo nuevo, lo seleccionamos
      this.insumoSeleccionado = insumo;
    }
  }
}
