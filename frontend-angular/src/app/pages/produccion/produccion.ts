import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Subscription, forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';
import { Receta } from '../../models/receta.interface';
import { NuevaRecetaModal } from '../../components/nueva-receta-modal/nueva-receta-modal';
import { RecetaService } from '../../services/receta';
import { InsumoService, Insumo } from '../../services/insumo.service';

// Interface para los insumos enriquecidos con datos reales
interface InsumoRecetaEnriquecido {
  insumo_id: string;
  cantidad: number;
  unidad: string;
  // Datos reales del insumo
  nombre_insumo?: string;
  stock_actual?: number;
  stock_minimo?: number;
  costo_unitario?: number;
}

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
export class Produccion implements OnInit, OnDestroy {
  
  listaRecetas: Receta[] = [];
  recetaSeleccionada: Receta | null = null;
  insumosEnriquecidos: InsumoRecetaEnriquecido[] = [];
  isModalOpen = false;
  loading = true;
  error = '';
  insumosReales: Insumo[] = [];
  
  private recetasSubscription: Subscription | undefined;
  private insumosSubscription: Subscription | undefined;

  constructor(
    private recetaService: RecetaService,
    private insumoService: InsumoService
  ) {}

  ngOnInit() {
    this.cargarRecetasReactivamente();
    this.cargarInsumosReales();
  }

  ngOnDestroy() {
    if (this.recetasSubscription) {
      this.recetasSubscription.unsubscribe();
    }
    if (this.insumosSubscription) {
      this.insumosSubscription.unsubscribe();
    }
  }

  cargarRecetasReactivamente() {
    this.loading = true;
    this.error = '';
    
    this.recetasSubscription = this.recetaService.getRecetas().subscribe({
      next: (recetas) => {
        this.listaRecetas = recetas;
        this.loading = false;
        console.log('📦 Recetas cargadas:', recetas.length);
      },
      error: (error) => {
        console.error('❌ Error cargando recetas:', error);
        this.error = 'Error al cargar las recetas';
        this.loading = false;
        this.listaRecetas = [];
      }
    });
  }

  cargarInsumosReales() {
    this.insumoService.getInsumos().subscribe({
      next: (insumos) => {
        this.insumosReales = insumos;
        console.log('📦 Insumos cargados:', this.insumosReales.length);
        // Si ya hay una receta seleccionada, actualizar los insumos enriquecidos
        if (this.recetaSeleccionada) {
          this.enriquecerInsumosReceta();
        }
      },
      error: (error) => {
        console.error('❌ Error cargando insumos:', error);
        this.insumosReales = [];
      }
    });
  }

  // ✅ NUEVO MÉTODO: Enriquecer los insumos de la receta con datos reales
  enriquecerInsumosReceta() {
    if (!this.recetaSeleccionada) return;
    
    this.insumosEnriquecidos = this.recetaSeleccionada.insumos.map(insumoReceta => {
      const insumoReal = this.insumosReales.find(i => i.id === insumoReceta.insumo_id);
      
      return {
        ...insumoReceta,
        nombre_insumo: insumoReal?.nombre_insumo || 'Insumo no encontrado',
        stock_actual: insumoReal?.stock_actual || 0,
        stock_minimo: insumoReal?.stock_minimo || 0,
        costo_unitario: insumoReal?.costo_unitario || 0
      };
    });
    
    console.log('🔍 Insumos enriquecidos:', this.insumosEnriquecidos);
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

  // ✅ Obtener nombre del insumo
  getNombreInsumo(insumoId: string): string {
    const insumo = this.getInsumoInfo(insumoId);
    return insumo ? insumo.nombre_insumo : 'Insumo no encontrado';
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

  // ✅ Obtener cantidad requerida de la receta
  getCantidadRequerida(insumoId: string): number {
    if (!this.recetaSeleccionada) return 0;
    const insumoReceta = this.recetaSeleccionada.insumos.find(i => i.insumo_id === insumoId);
    return insumoReceta ? insumoReceta.cantidad : 0;
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

  // ✅ Verificar si todos los insumos tienen stock suficiente
  getProduccionPosible(): boolean {
    if (!this.recetaSeleccionada) return false;
    
    return this.recetaSeleccionada.insumos.every(insumo => {
      const stockActual = this.getStockActual(insumo.insumo_id);
      return stockActual >= insumo.cantidad;
    });
  }

  onRecetaCreada() {
    console.log('📢 Receta creada - la lista se actualizará automáticamente');
  }

  seleccionarReceta(receta: Receta): void {
    this.recetaSeleccionada = receta;
    this.enriquecerInsumosReceta();
    console.log('🎯 Receta seleccionada:', receta.nombre_producto);
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
      const estadoOriginal = receta.estado;
      receta.estado = nuevoEstado;
      
      this.recetaService.toggleRecetaEstado(id, nuevoEstado).subscribe({
        error: (error) => {
          console.error('Error actualizando estado:', error);
          receta.estado = estadoOriginal;
        }
      });

      if (!nuevoEstado && this.recetaSeleccionada?.id === id) {
        this.recetaSeleccionada = null;
        this.insumosEnriquecidos = [];
      }
    }
  }

  recargarManual() {
    console.log('🔄 Recarga manual de recetas');
    this.cargarRecetasReactivamente();
  }

  // ✅ MÉTODO PARA CONFIRMAR PRODUCCIÓN
  confirmarProduccion(): void {
    if (!this.recetaSeleccionada) return;
    
    if (!this.getProduccionPosible()) {
      alert('❌ No hay suficiente stock para realizar la producción');
      return;
    }
    
    // Aquí iría la lógica para registrar la producción
    console.log('✅ Confirmando producción de:', this.recetaSeleccionada.nombre_producto);
    alert(`✅ Producción de ${this.recetaSeleccionada.nombre_producto} confirmada`);
  }

  cancelarProduccion(): void {
    this.recetaSeleccionada = null;
    this.insumosEnriquecidos = [];
    console.log('❌ Producción cancelada');
  }
}