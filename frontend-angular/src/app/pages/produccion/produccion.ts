import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Receta } from '../../models/receta.interface';
import { InsumoFormulario } from '../../models/insumo-formulario.interface'; 

@Component({
  selector: 'app-produccion',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './produccion.html',
  styleUrl: './produccion.scss',
})
export class Produccion {
  // --- 3. Datos de prueba para el RECETARIO ---
  listaRecetas: Receta[] = [
    { id: '1', nombre: 'Queso Fresco', rendimiento: '18-20 Kg' },
    { id: '2', nombre: 'Queso Seco', rendimiento: '30-40 Kg' },
    { id: '3', nombre: 'Queso Fresco', rendimiento: '18-20 Kg' },
    { id: '4', nombre: 'Queso Fresco', rendimiento: '18-20 Kg' },
    { id: '5', nombre: 'Queso Seco', rendimiento: '30-40 Kg' },
    { id: '6', nombre: 'Queso Fresco', rendimiento: '18-20 Kg' }
  ];

  // --- 4. Datos de prueba para el FORMULARIO ---
  // (En el futuro, esto se llenaría al hacer clic en "Iniciar Producción")
  insumosFormulario: InsumoFormulario[] = [
    { 
      nombre: 'Leche Entera', 
      cantidad: '10L', 
      stock: '150L', 
      status: 'ok' 
    },
    { 
      nombre: 'Sal', 
      cantidad: '2.5 Kg', 
      stock: '6 Kg', 
      status: 'low' // Amarillo
    },
    { 
      nombre: 'Cuajo', 
      cantidad: '25 Ml', 
      stock: '10 Ml', 
      status: 'out' // Rojo
    },
  ];
}
