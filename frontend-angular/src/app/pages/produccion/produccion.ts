import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Subscription, forkJoin } from 'rxjs';

// Importa las interfaces desde los servicios
import { Receta } from '../../models/receta.interface';
import { RecetaService } from '../../services/receta';
import { InsumoService, Insumo } from '../../services/insumo.service';
import { ProductoService, ProductoLacteo } from '../../services/producto.service';

// Importa el modal correctamente
import { NuevaRecetaModal } from '../../components/nueva-receta-modal/nueva-receta-modal';

interface InsumoRecetaEnriquecido {
  insumo_id: string;
  cantidad: number;
  unidad: string;
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
    HttpClientModule,
    FormsModule,
    NuevaRecetaModal // ✅ Ahora está correctamente importado
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
  
  cantidadProducir: number = 1;
  produccionEnProceso: boolean = false;
  
  private recetasSubscription: Subscription | undefined;
  private insumosSubscription: Subscription | undefined;

  constructor(
    private recetaService: RecetaService,
    private insumoService: InsumoService,
    private productoService: ProductoService
  ) {
    console.log('✅ Produccion component initialized');
  }

  ngOnInit() {
    console.log('🔄 ngOnInit ejecutado');
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
    
    console.log('🔄 Cargando recetas...');
    this.recetasSubscription = this.recetaService.getRecetas().subscribe({
      next: (recetas) => {
        console.log('📦 Recetas cargadas:', recetas);
        this.listaRecetas = recetas;
        this.loading = false;
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
    console.log('🔄 Cargando insumos...');
    this.insumosSubscription = this.insumoService.getInsumos().subscribe({
      next: (insumos) => {
        console.log('📦 Insumos cargados:', insumos);
        this.insumosReales = insumos;
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

  getInsumoInfo(insumoId: string): Insumo | null {
    return this.insumosReales.find(i => i.id === insumoId) || null;
  }

  getStockActual(insumoId: string): number {
    const insumo = this.getInsumoInfo(insumoId);
    return insumo ? insumo.stock_actual : 0;
  }

  getUnidadInsumo(insumoId: string): string {
    const insumo = this.getInsumoInfo(insumoId);
    return insumo ? insumo.unidad : '';
  }

  getStatusText(insumoId: string): string {
    const insumo = this.getInsumoInfo(insumoId);
    if (!insumo) return 'No encontrado';
    
    const cantidadRequerida = this.getCantidadRequerida(insumoId);
    
    if (insumo.stock_actual === 0) return 'Agotado';
    if (insumo.stock_actual < cantidadRequerida) return 'Insuficiente';
    if (insumo.stock_actual <= insumo.stock_minimo) return 'Bajo';
    return 'Ok';
  }

  getCantidadRequerida(insumoId: string): number {
    if (!this.recetaSeleccionada) return 0;
    const insumoReceta = this.recetaSeleccionada.insumos.find(i => i.insumo_id === insumoId);
    return insumoReceta ? insumoReceta.cantidad : 0;
  }

  getStatusClass(insumoId: string): any {
    const status = this.getStatusText(insumoId);
    return {
      'bg-green-100 text-green-800': status === 'Ok',
      'bg-yellow-100 text-yellow-800': status === 'Bajo',
      'bg-orange-100 text-orange-800': status === 'Insuficiente',
      'bg-red-100 text-red-800': status === 'Agotado' || status === 'No encontrado'
    };
  }

  getProduccionPosible(): boolean {
    if (!this.recetaSeleccionada || this.cantidadProducir <= 0) return false;
    
    return this.recetaSeleccionada.insumos.every(insumo => {
      const stockActual = this.getStockActual(insumo.insumo_id);
      const cantidadTotalRequerida = insumo.cantidad * this.cantidadProducir;
      return stockActual >= cantidadTotalRequerida;
    });
  }

  getCantidadTotalRequerida(insumoId: string): number {
    if (!this.recetaSeleccionada) return 0;
    const insumoReceta = this.recetaSeleccionada.insumos.find(i => i.insumo_id === insumoId);
    return insumoReceta ? insumoReceta.cantidad * this.cantidadProducir : 0;
  }

  onRecetaCreada() {
    console.log('📢 Receta creada - recargando lista...');
    this.cargarRecetasReactivamente(); // Recarga las recetas cuando se crea una nueva
  }

  seleccionarReceta(receta: Receta): void {
    this.recetaSeleccionada = receta;
    this.cantidadProducir = 1;
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
        this.cantidadProducir = 1;
      }
    }
  }

  recargarManual() {
    console.log('🔄 Recarga manual');
    this.cargarRecetasReactivamente();
  }

  confirmarProduccion(): void {
    if (!this.recetaSeleccionada || !this.getProduccionPosible()) {
      alert('❌ No hay suficiente stock para realizar la producción');
      return;
    }

    if (this.cantidadProducir <= 0) {
      alert('❌ La cantidad a producir debe ser mayor a 0');
      return;
    }

    this.produccionEnProceso = true;

    // 1. Calcular los nuevos stocks para cada insumo
    const actualizacionesInsumos = this.recetaSeleccionada.insumos.map(insumoReceta => {
      const cantidadTotalRequerida = insumoReceta.cantidad * this.cantidadProducir;
      const nuevoStock = this.getStockActual(insumoReceta.insumo_id) - cantidadTotalRequerida;
      
      return this.insumoService.actualizarStockInsumo(
        insumoReceta.insumo_id, 
        nuevoStock
      );
    });

    // 2. Calcular la nueva cantidad del producto lácteo
    const cantidadProducidaTotal = this.recetaSeleccionada.rendimiento * this.cantidadProducir;
    
    // 3. Actualizar el inventario del producto lácteo
    const actualizacionProducto = this.productoService.actualizarInventarioProducto(
      this.recetaSeleccionada.producto_id,
      cantidadProducidaTotal
    );

    // 4. Ejecutar todas las actualizaciones en paralelo
    forkJoin([...actualizacionesInsumos, actualizacionProducto]).subscribe({
      next: (results) => {
        console.log('✅ Producción registrada exitosamente', results);
        this.produccionEnProceso = false;
        
        // Mostrar resumen de la producción
        alert(`✅ Producción exitosa!\n\n` +
              `Producto: ${this.recetaSeleccionada?.nombre_producto}\n` +
              `Cantidad producida: ${this.cantidadProducir} lotes\n` +
              `Total producido: ${cantidadProducidaTotal} ${this.recetaSeleccionada?.unidad_rendimiento}\n\n` +
              `Los insumos han sido descontados del inventario.`);

        // Recargar datos actualizados
        this.cargarInsumosReales();
        this.cancelarProduccion();
      },
      error: (error) => {
        console.error('❌ Error en la producción:', error);
        this.produccionEnProceso = false;
        alert('❌ Error al registrar la producción. Por favor, intenta nuevamente.');
      }
    });
  }

  cancelarProduccion(): void {
    this.recetaSeleccionada = null;
    this.insumosEnriquecidos = [];
    this.cantidadProducir = 1;
    console.log('❌ Producción cancelada');
  }

  onCantidadChange(): void {
    if (this.cantidadProducir < 1) {
      this.cantidadProducir = 1;
    }
  }

  incrementarCantidad(): void {
    this.cantidadProducir++;
  }

  decrementarCantidad(): void {
    if (this.cantidadProducir > 1) {
      this.cantidadProducir--;
    }
  }
}