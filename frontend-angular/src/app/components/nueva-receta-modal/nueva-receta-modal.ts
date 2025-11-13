import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  ReactiveFormsModule, 
  FormBuilder, 
  FormGroup, 
  FormArray, 
  Validators 
} from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import { RecetaService } from '../../services/receta';
import { InsumoService, Insumo } from '../../services/insumo.service';
import { ProductoService, ProductoLacteo } from '../../services/producto.service';
import { Receta } from '../../models/receta.interface';

@Component({
  selector: 'app-nueva-receta-modal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule], 
  templateUrl: './nueva-receta-modal.html',
  styleUrl: './nueva-receta-modal.scss'
})
export class NuevaRecetaModal implements OnInit {
  @Output() cerrar = new EventEmitter<void>();
  @Output() recetaCreada = new EventEmitter<void>();

  recetaForm: FormGroup;
  loading = false;
  modoNuevoProducto = true;

  insumosDisponibles: Insumo[] = [];
  productosExistentes: ProductoLacteo[] = [];

  constructor(
    private fb: FormBuilder, 
    private recetaService: RecetaService,
    private insumoService: InsumoService,
    private productoService: ProductoService
  ) {
    this.recetaForm = this.createForm();
  }

  ngOnInit() {
    this.cargarInsumosReales();
    this.cargarProductosExistentes();
  }

  cargarInsumosReales() {
    this.insumoService.getInsumos().subscribe({
      next: (insumos) => {
        this.insumosDisponibles = insumos;
      },
      error: (error) => {
        console.error('Error cargando insumos:', error);
      }
    });
  }

  cargarProductosExistentes() {
    this.productoService.getProductos().subscribe({
      next: (productos) => {
        this.productosExistentes = productos;
      },
      error: (error) => {
        console.error('Error cargando productos:', error);
      }
    });
  }

  createForm(): FormGroup {
    return this.fb.group({
      // Para nuevo producto
      nombre_receta: ['', Validators.required],
      
      // Para producto existente
      producto_existente_id: [''],
      
      observaciones: [''],
      estado: [true],

      // Rendimiento
      rendimiento: this.fb.group({
        cantidad: ['', [Validators.required, Validators.min(0.1)]],
        unidad: ['kg', Validators.required]
      }),

      insumos: this.fb.array([], Validators.required)
    });
  }

  get insumos() {
    return this.recetaForm.get('insumos') as FormArray;
  }

  get rendimiento() {
    return this.recetaForm.get('rendimiento') as FormGroup;
  }

  cambiarModo(nuevoModo: boolean) {
    this.modoNuevoProducto = nuevoModo;
    
    if (nuevoModo) {
      this.recetaForm.get('producto_existente_id')?.clearValidators();
      this.recetaForm.get('nombre_receta')?.setValidators([Validators.required]);
    } else {
      this.recetaForm.get('nombre_receta')?.clearValidators();
      this.recetaForm.get('producto_existente_id')?.setValidators([Validators.required]);
    }
    
    this.recetaForm.get('nombre_receta')?.updateValueAndValidity();
    this.recetaForm.get('producto_existente_id')?.updateValueAndValidity();
  }

  nuevoInsumo(): FormGroup {
    return this.fb.group({
      insumo_id: ['', Validators.required],
      cantidad: ['', [Validators.required, Validators.min(0.1)]],
      unidad: ['', Validators.required]
    });
  }

  getNombreInsumo(insumoId: string): string {
    const insumo = this.insumosDisponibles.find(i => i.id === insumoId);
    return insumo ? insumo.nombre_insumo : 'Seleccionar insumo';
  }

  getUnidadInsumo(insumoId: string): string {
    const insumo = this.insumosDisponibles.find(i => i.id === insumoId);
    return insumo ? insumo.unidad : '';
  }

  onInsumoSeleccionado(index: number) {
    const insumoControl = this.insumos.at(index);
    const insumoId = insumoControl.get('insumo_id')?.value;
    
    if (insumoId) {
      const unidad = this.getUnidadInsumo(insumoId);
      insumoControl.patchValue({ unidad: unidad });
    }
  }

  agregarInsumo() {
    this.insumos.push(this.nuevoInsumo());
  }

  quitarInsumo(index: number) {
    this.insumos.removeAt(index);
  }

  onCerrarClick(): void {
    this.cerrar.emit();
  }

  // ✅ FLUJO COMPLETO CORREGIDO
  async guardarReceta() {
    if (this.recetaForm.valid && this.insumos.length > 0) {
      this.loading = true;

      try {
        const formValue = this.recetaForm.value;
        const rendimiento = formValue.rendimiento;

        let productoId: string;
        let nombreProducto: string;

        // PASO 1: Crear o seleccionar producto
        if (this.modoNuevoProducto) {
          // Crear nuevo producto (SIN PRECIO por ahora)
          const nuevoProducto = await firstValueFrom(
            this.productoService.createProducto({
              desc_queso: formValue.nombre_receta,
              precio: 0, // Precio por defecto
              totalInventario: 0
            })
          );

          productoId = nuevoProducto.id;
          nombreProducto = nuevoProducto.desc_queso;
        } else {
          // Usar producto existente
          productoId = formValue.producto_existente_id;
          const productoExistente = this.productosExistentes.find(p => p.id === productoId);
          nombreProducto = productoExistente ? productoExistente.desc_queso : '';
        }

        // PASO 2: Preparar datos de la receta
        const recetaData: Receta = {
          id: '',
          producto_id: productoId,
          nombre_producto: nombreProducto,
          rendimiento: rendimiento.cantidad,
          unidad_rendimiento: rendimiento.unidad,
          observaciones: formValue.observaciones,
          estado: formValue.estado,
          insumos: formValue.insumos.map((insumo: any) => ({
            insumo_id: insumo.insumo_id,
            nombre_insumo: this.getNombreInsumo(insumo.insumo_id),
            cantidad: insumo.cantidad,
            unidad: insumo.unidad
          }))
        };

        console.log('📤 Creando receta:', recetaData);

        // PASO 3: Crear la receta
        this.recetaService.createReceta(recetaData).subscribe({
          next: (recetaCreada) => {
            console.log('✅ Receta creada exitosamente:', recetaCreada);
            this.loading = false;
            this.recetaCreada.emit();
            this.onCerrarClick();
          },
          error: (error) => {
            console.error('❌ Error creando receta:', error);
            this.loading = false;
            alert('Error al crear la receta: ' + error.message);
          }
        });

      } catch (error) {
        console.error('❌ Error en el proceso:', error);
        this.loading = false;
        alert('Error en el proceso de creación');
      }

    } else {
      this.recetaForm.markAllAsTouched();
      if (this.insumos.length === 0) {
        alert('⚠️ Debes agregar al menos un insumo');
      } else {
        alert('⚠️ Por favor completa todos los campos requeridos');
      }
    }
  }
}