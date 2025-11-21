import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Subscription, forkJoin, firstValueFrom } from 'rxjs';

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
    NuevaRecetaModal
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
    this.cargarRecetasReactivamente();
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

  async confirmarProduccion(): Promise<void> {
    if (!this.recetaSeleccionada || !this.getProduccionPosible()) {
      alert('❌ No hay suficiente stock para realizar la producción');
      return;
    }

    if (this.cantidadProducir <= 0) {
      alert('❌ La cantidad a producir debe ser mayor a 0');
      return;
    }

    this.produccionEnProceso = true;

    try {
      // 1. Calcular los nuevos stocks para cada insumo
      const actualizacionesInsumos = this.recetaSeleccionada.insumos.map(insumoReceta => {
        const cantidadTotalRequerida = insumoReceta.cantidad * this.cantidadProducir;
        const nuevoStock = this.getStockActual(insumoReceta.insumo_id) - cantidadTotalRequerida;
        
        console.log(`📦 Actualizando insumo ${insumoReceta.insumo_id}: ${this.getStockActual(insumoReceta.insumo_id)} - ${cantidadTotalRequerida} = ${nuevoStock}`);
        
        return this.insumoService.actualizarStockInsumo(
          insumoReceta.insumo_id, 
          nuevoStock
        );
      });

      // 2. Calcular la nueva cantidad del producto lácteo
      const cantidadProducidaTotal = this.recetaSeleccionada.rendimiento * this.cantidadProducir;
      
      // 3. Obtener el stock actual del producto para SUMAR (no reemplazar)
      const productos = await firstValueFrom(this.productoService.getProductos());
      const productoActual = productos.find(p => p.id === this.recetaSeleccionada!.producto_id);
      
      const inventarioActual = productoActual?.totalInventario || 0;
      const nuevoInventario = inventarioActual + cantidadProducidaTotal;

      console.log(`📦 Actualizando producto ${this.recetaSeleccionada.producto_id}: ${inventarioActual} + ${cantidadProducidaTotal} = ${nuevoInventario}`);

      // 4. Actualizar el inventario del producto lácteo
      const actualizacionProducto = this.productoService.actualizarInventarioProducto(
        this.recetaSeleccionada.producto_id,
        nuevoInventario
      );

      // 5. Ejecutar todas las actualizaciones en paralelo
      await firstValueFrom(
        forkJoin([...actualizacionesInsumos, actualizacionProducto])
      );

      console.log('✅ Producción registrada exitosamente');

      // 6. Mostrar resumen de la producción
      alert(`✅ Producción exitosa!\n\n` +
            `Producto: ${this.recetaSeleccionada.nombre_producto}\n` +
            `Cantidad producida: ${this.cantidadProducir} lotes\n` +
            `Total producido: ${cantidadProducidaTotal} ${this.recetaSeleccionada.unidad_rendimiento}\n\n` +
            `Los insumos han sido descontados del inventario.`);

      // 7. Recargar datos actualizados y limpiar UI
      await this.recargarDatosDespuesProduccion();

    } catch (error: any) {
      console.error('❌ Error en la producción:', error);
      
      let mensajeError = 'Error al registrar la producción.';
      
      if (error.status === 405) {
        mensajeError += '\n\n⚠️ Error 405: Método no permitido.';
      } else if (error.status === 404) {
        mensajeError += '\n\n⚠️ Error 404: Endpoint no encontrado.';
      } else {
        mensajeError += `\n\nDetalles: ${error.message}`;
      }
      
      alert(mensajeError);
    } finally {
      // 8. SIEMPRE limpiar el estado de carga
      this.produccionEnProceso = false;
    }
  }

  // ✅ NUEVO MÉTODO: Recargar datos después de producción
  async recargarDatosDespuesProduccion(): Promise<void> {
    try {
      // Recargar insumos para obtener datos actualizados
      await firstValueFrom(this.insumoService.getInsumos()).then(insumos => {
        this.insumosReales = insumos;
        console.log('📦 Insumos actualizados después de producción:', this.insumosReales.length);
      });

      // Limpiar la selección actual
      this.recetaSeleccionada = null;
      this.insumosEnriquecidos = [];
      this.cantidadProducir = 1;
      
      console.log('🔄 Producción completada y UI limpiada');
      
    } catch (error) {
      console.error('❌ Error recargando datos después de producción:', error);
      // Aún así limpiamos la UI
      this.recetaSeleccionada = null;
      this.insumosEnriquecidos = [];
      this.cantidadProducir = 1;
    }
  }

  cancelarProduccion(): void {
    // Solo cancelar si no hay producción en proceso
    if (!this.produccionEnProceso) {
      this.recetaSeleccionada = null;
      this.insumosEnriquecidos = [];
      this.cantidadProducir = 1;
      console.log('❌ Producción cancelada por el usuario');
    } else {
      console.log('⚠️ No se puede cancelar durante producción en proceso');
    }
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