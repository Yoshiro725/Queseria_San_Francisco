import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Receta } from '../../models/receta.interface';
import { NuevaRecetaModal } from '../../components/nueva-receta-modal/nueva-receta-modal';
import { RecetaService } from '../../services/receta';
import { InsumoService, Insumo } from '../../services/insumo.service';

@Component({
  selector: 'app-produccion',
  standalone: true,
  imports: [
    CommonModule, 
    NuevaRecetaModal,
    HttpClientModule
  ],
  templateUrl: './produccion.html',
  styleUrl: './produccion.scss',
})
export class Produccion implements OnInit {
  
  listaRecetas: Receta[] = [];
  recetaSeleccionada: Receta | null = null;
  isModalOpen = false;
  loading = true;
  error = '';
  insumosReales: Insumo[] = [];

  constructor(
    private recetaService: RecetaService,
    private insumoService: InsumoService
  ) {}

  ngOnInit() {
    this.cargarRecetasDesdeBackend();
    this.cargarInsumosReales();
  }

  // ✅ Cargar insumos reales desde el backend
  cargarInsumosReales() {
    this.insumoService.getInsumos().subscribe({
      next: (insumos) => {
        this.insumosReales = insumos;
        console.log('Insumos cargados:', this.insumosReales);
      },
      error: (error) => {
        console.error('Error cargando insumos:', error);
      }
    });
  }

  // ✅ Obtener información completa de un insumo por ID
  getInsumoInfo(insumoId: string): Insumo | null {
    return this.insumosReales.find(i => i.id === insumoId) || null;
  }

  // ✅ Obtener stock actual de un insumo
  getStockActual(insumoId: string): number {
    const insumo = this.getInsumoInfo(insumoId);
    return insumo ? insumo.stock_actual : 0;
  }

  // ✅ Obtener unidad del insumo
  getUnidadInsumo(insumoId: string): string {
    const insumo = this.getInsumoInfo(insumoId);
    return insumo ? insumo.unidad : '';
  }

  // ✅ Obtener cantidad requerida de la receta (PÚBLICA para el HTML)
  getCantidadRequerida(insumoId: string): number {
    if (!this.recetaSeleccionada) return 0;
    const insumoReceta = this.recetaSeleccionada.insumos.find(i => i.insumo_id === insumoId);
    return insumoReceta ? insumoReceta.cantidad : 0;
  }

  // ✅ Determinar estado del insumo
  getStatusText(insumoId: string): string {
    const insumo = this.getInsumoInfo(insumoId);
    if (!insumo) return 'No encontrado';
    
    const cantidadRequerida = this.getCantidadRequerida(insumoId);
    
    if (insumo.stock_actual === 0) return 'Agotado';
    if (insumo.stock_actual < cantidadRequerida) return 'Insuficiente';
    if (insumo.stock_actual <= insumo.stock_minimo) return 'Bajo';
    return 'Ok';
  }

  // ✅ Obtener clase CSS para el estado
  getStatusClass(insumoId: string): any {
    const status = this.getStatusText(insumoId);
    return {
      'bg-green-100 text-green-800': status === 'Ok',
      'bg-yellow-100 text-yellow-800': status === 'Bajo',
      'bg-orange-100 text-orange-800': status === 'Insuficiente',
      'bg-red-100 text-red-800': status === 'Agotado' || status === 'No encontrado'
    };
  }

  // Los demás métodos se mantienen igual...
  onRecetaCreada() {
    this.cargarRecetasDesdeBackend();
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
      }
    });
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
      receta.estado = nuevoEstado;
      this.recetaService.toggleRecetaEstado(id, nuevoEstado).subscribe({
        error: (error) => {
          console.error('Error actualizando estado:', error);
          receta.estado = !nuevoEstado;
        }
      });

      if (!nuevoEstado && this.recetaSeleccionada?.id === id) {
        this.recetaSeleccionada = null;
      }
    }
  }
}