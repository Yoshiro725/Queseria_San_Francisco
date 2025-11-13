import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Receta } from '../../models/receta.interface';
import { InsumoFormulario } from '../../models/insumo-formulario.interface';
import { NuevaRecetaModal } from '../../components/nueva-receta-modal/nueva-receta-modal';
import { RecetaService } from '../../services/receta';

@Component({
  selector: 'app-produccion',
  standalone: true,
  imports: [CommonModule, NuevaRecetaModal],
  templateUrl: './produccion.html',
  styleUrl: './produccion.scss',
})
export class Produccion implements OnInit {
  
  // Variables principales
  listaRecetas: Receta[] = [];
  recetaSeleccionada: Receta | null = null;
  insumosFormulario: InsumoFormulario[] = [];
  isModalOpen = false;
  loading = true;
  error = '';

  constructor(private recetaService: RecetaService) {}

  ngOnInit() {
    this.cargarRecetasDesdeBackend();
    this.cargarInsumosFormulario();
  }

  // ✅ MÉTODO NUEVO: Para cuando se crea una receta
  onRecetaCreada() {
    console.log('Receta creada - recargando lista...');
    this.cargarRecetasDesdeBackend(); // Recargar las recetas desde el backend
  }

  cargarRecetasDesdeBackend() {
    this.loading = true;
    this.recetaService.getRecetas().subscribe({
      next: (recetas) => {
        this.listaRecetas = recetas;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error cargando recetas:', error);
        this.error = 'Error al cargar las recetas';
        this.loading = false;
        // Mantenemos datos de prueba como fallback
        this.listaRecetas = this.getDatosPrueba();
      }
    });
  }

  // Método para cargar los insumos del formulario
  private cargarInsumosFormulario() {
    this.insumosFormulario = [
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
        status: 'Bajo'
      },
      { 
        nombre: 'Cuajo', 
        cantidad: '25 Ml', 
        stock: '10 Ml', 
        status: 'Agotado'
      },
    ];
  }

  // Mantener datos de prueba como respaldo
  private getDatosPrueba(): Receta[] {
    return [
      { 
        id: '1', 
        producto_id: '1',
        nombre_producto: 'Queso Fresco',
        rendimiento: 18, 
        unidad_rendimiento: 'Kg',
        observaciones: 'Receta base', 
        estado: true,
        insumos: [
          { insumo_id: '1', nombre_insumo: 'Leche Entera', cantidad: 15, unidad: 'L' },
          { insumo_id: '2', nombre_insumo: 'Sal', cantidad: 0.5, unidad: 'kg' }
        ]
      },
      { 
        id: '2', 
        producto_id: '2',
        nombre_producto: 'Queso Seco',
        rendimiento: 30, 
        unidad_rendimiento: 'Kg',
        observaciones: 'Maduración de 30 días', 
        estado: true,
        insumos: [
          { insumo_id: '1', nombre_insumo: 'Leche Entera', cantidad: 20, unidad: 'L' },
          { insumo_id: '2', nombre_insumo: 'Sal', cantidad: 0.8, unidad: 'kg' }
        ]
      }
    ];
  }

  seleccionarReceta(receta: Receta): void {
    this.recetaSeleccionada = receta;
  }
  
  abrirModalNuevaReceta(): void {
    this.isModalOpen = true;
  }

  cerrarModalNuevaReceta(): void {
    this.isModalOpen = false;
  }

  cambiarEstadoReceta(id: string, nuevoEstado: boolean): void {
    const receta = this.listaRecetas.find(r => r.id === id);
    if (receta) {
      // Actualizar localmente primero para respuesta rápida
      receta.estado = nuevoEstado;
      
      // Enviar al backend
      this.recetaService.toggleRecetaEstado(id, nuevoEstado).subscribe({
        error: (error) => {
          console.error('Error actualizando estado:', error);
          // Revertir cambio local si falla
          receta.estado = !nuevoEstado;
        }
      });

      // Si la receta que se inactivó era la seleccionada, la quitamos
      if (!nuevoEstado && this.recetaSeleccionada?.id === id) {
        this.recetaSeleccionada = null;
      }
    }
  }
}