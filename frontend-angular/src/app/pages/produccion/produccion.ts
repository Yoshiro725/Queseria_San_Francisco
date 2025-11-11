import { Component} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Receta } from '../../models/receta.interface';
import { InsumoFormulario } from '../../models/insumo-formulario.interface';
import { NuevaRecetaModal } from '../../components/nueva-receta-modal/nueva-receta-modal'; //importamos el nuevo modal para nuevas recetas 

@Component({
  selector: 'app-produccion',
  standalone: true,
  imports: [CommonModule, NuevaRecetaModal],
  templateUrl: './produccion.html',
  styleUrl: './produccion.scss',
})
export class Produccion{
  // --- 3. Datos de prueba para el RECETARIO ---
listaRecetas: Receta[] = [
    { 
      id: '1', 
      nombre: 'Queso Fresco', 
      rendimiento: 18, 
      unidad: 'Kg', 
      observaciones: 'Receta base', 
      estado: 'activo' 
    },
    { 
      id: '2', 
      nombre: 'Queso Seco', 
      rendimiento: 30, 
      unidad: 'Kg', 
      observaciones: 'Maduración de 30 días', 
      estado: 'activo' 
    },
    { 
      id: '3', 
      nombre: 'Quesillo', 
      rendimiento: 17, 
      unidad: 'Kg', 
      observaciones: 'Pasta hilada', 
      estado: 'activo' 
    },
    { 
      id: '4', 
      nombre: 'Yogurt', 
      rendimiento: 100, 
      unidad: 'L', 
      observaciones: 'Fermentación 6 horas', 
      estado: 'activo' 
    },
    { 
      id: '5', 
      nombre: 'Crema', 
      rendimiento: 10, 
      unidad: 'L', 
      observaciones: 'A partir de 100L de leche', 
      estado: 'activo' 
    },
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

  isModalOpen = false;
  recetaSeleccionada: Receta | null = null;
  seleccionarReceta(receta: Receta): void {
    this.recetaSeleccionada = receta;
  }
  
  abrirModalNuevaReceta(): void {
    this.isModalOpen = true;
  }

  cerrarModalNuevaReceta(): void {
    this.isModalOpen = false;
  }
  cambiarEstadoReceta(id: string, nuevoEstado: 'activo' | 'inactivo'): void {
    const receta = this.listaRecetas.find(r => r.id === id);
    if (receta) {
      receta.estado = nuevoEstado;
      console.log(`Receta ${receta.nombre} ahora está ${nuevoEstado}`);

      // Lógica extra: Si la receta que se inactivó era la seleccionada,
      // la quitamos del formulario de abajo.
      if (nuevoEstado === 'inactivo' && this.recetaSeleccionada?.id === id) {
        this.recetaSeleccionada = null;
      }
    }
  }
}
