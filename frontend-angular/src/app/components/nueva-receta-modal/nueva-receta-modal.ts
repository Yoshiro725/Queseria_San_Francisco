import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  ReactiveFormsModule, 
  FormBuilder, 
  FormGroup, 
  FormArray, 
  Validators 
} from '@angular/forms';
import { RecetaService } from '../../services/receta';
import { Receta } from '../../models/receta.interface';

@Component({
  selector: 'app-nueva-receta-modal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule], 
  templateUrl: './nueva-receta-modal.html',
  styleUrl: './nueva-receta-modal.scss'
})
export class NuevaRecetaModal {
  @Output() cerrar = new EventEmitter<void>();
  @Output() recetaCreada = new EventEmitter<void>();

  recetaForm: FormGroup;

  // Datos para los selects (IDs reales de tu MongoDB)
  productos = [
    { id: '690d6490f8a037abefeec4b7', nombre: 'Queso Fresco' },
    { id: '690d6490f8a037abefeec4b8', nombre: 'Quesillo' },
    { id: '690d657bf8a037abefeec4cb', nombre: 'Requesón' }
  ];

  insumosDisponibles = [
    { id: '690d6471f8a037abefeec4b3', nombre: 'Leche Entera', unidad: 'L' },
    { id: '690d6471f8a037abefeec4b4', nombre: 'Sal', unidad: 'kg' },
    { id: '690d6471f8a037abefeec4b5', nombre: 'Cuajo', unidad: 'ml' }
  ];

  constructor(private fb: FormBuilder, private recetaService: RecetaService) {
    this.recetaForm = this.fb.group({
      // CAMBIO: Cambiar 'nombre' por 'producto_id' para el backend
      nombre: ['', Validators.required], // Lo mantengo temporalmente para tu HTML
      producto_id: [''], // ← NUEVO: para el backend
      
      descripcion: [''],
      estado: ['Activo'],

      // Rendimiento - adaptado para tu HTML
      rendimiento: this.fb.group({
        cantidadProducida: ['', [Validators.required, Validators.min(0.1)]],
        unidadRendimiento: ['kg', Validators.required],
        rangoOpcional: [''],
        porcentajeRendimiento: [{ value: '', disabled: true }]
      }),

      insumos: this.fb.array([]),
    });

    // Sincronizar nombre con producto_id
    this.recetaForm.get('nombre')?.valueChanges.subscribe(nombre => {
      const producto = this.productos.find(p => p.nombre === nombre);
      if (producto) {
        this.recetaForm.patchValue({ producto_id: producto.id });
      }
    });
  }

  get insumos() {
    return this.recetaForm.get('insumos') as FormArray;
  }

  get rendimiento() {
    return this.recetaForm.get('rendimiento') as FormGroup;
  }

  // MÉTODO ACTUALIZADO: Para crear insumos compatibles con backend
  nuevoInsumo(): FormGroup {
    return this.fb.group({
      nombre: ['', Validators.required],     // Para mostrar en el form
      insumo_id: [''],                       // Para el backend
      cantidad: ['', [Validators.required, Validators.min(0.1)]],
      unidad: ['', Validators.required]
    });
  }

  // ACTUALIZADO: Sincronizar insumo seleccionado con ID real
  onInsumoSeleccionado(index: number) {
    const insumoControl = this.insumos.at(index);
    const nombreInsumo = insumoControl.get('nombre')?.value;
    
    const insumo = this.insumosDisponibles.find(i => i.nombre === nombreInsumo);
    if (insumo) {
      insumoControl.patchValue({
        insumo_id: insumo.id,
        unidad: insumo.unidad
      });
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

  // MÉTODO ACTUALIZADO: Para guardar en el backend
guardarReceta() {
  if (this.recetaForm.valid && this.insumos.length > 0) {
    
    const formValue = this.recetaForm.value;
    const rendimiento = formValue.rendimiento;

    // ✅ CORREGIR: Obtener el producto_id correctamente
    const productoSeleccionado = this.productos.find(p => p.nombre === formValue.nombre);
    const producto_id = productoSeleccionado ? productoSeleccionado.id : '';

    // ✅ CORREGIR: Mapear insumos correctamente
    const insumosMapeados = formValue.insumos.map((insumo: any) => {
      const insumoEncontrado = this.insumosDisponibles.find(i => i.nombre === insumo.nombre);
      return {
        insumo_id: insumoEncontrado ? insumoEncontrado.id : '',
        nombre_insumo: insumo.nombre,
        cantidad: insumo.cantidad,
        unidad: insumo.unidad
      };
    });

    // Preparar datos para el backend
    const recetaData: Receta = {
      id: '',
      producto_id: producto_id,
      nombre_producto: formValue.nombre,
      rendimiento: rendimiento.cantidadProducida,
      unidad_rendimiento: rendimiento.unidadRendimiento,
      observaciones: formValue.descripcion,
      estado: formValue.estado === 'Activo',
      insumos: insumosMapeados
    };

    console.log('✅ Enviando al backend:', recetaData);

    // Validar que tengamos producto_id
    if (!producto_id) {
      alert('❌ Error: No se pudo encontrar el ID del producto seleccionado');
      return;
    }

    // Validar que todos los insumos tengan ID
    const insumosSinId = recetaData.insumos.filter(insumo => !insumo.insumo_id);
    if (insumosSinId.length > 0) {
      alert('❌ Error: Algunos insumos no tienen ID válido');
      return;
    }

    // Llamar al servicio
    this.recetaService.createReceta(recetaData).subscribe({
      next: (recetaCreada) => {
        console.log('✅ Receta creada exitosamente:', recetaCreada);
        this.recetaCreada.emit();
        this.onCerrarClick();
      },
      error: (error) => {
        console.error('❌ Error creando receta:', error);
        alert('Error al crear la receta. Verifica la consola.');
      }
    });

  } else {
    console.log('Formulario Inválido o sin insumos');
    this.recetaForm.markAllAsTouched(); 
    
    if (this.insumos.length === 0) {
      alert('Debes agregar al menos un insumo');
    }
  }
}

  // Helper para obtener ID del producto por nombre
  private getProductoIdPorNombre(nombre: string): string {
    const producto = this.productos.find(p => p.nombre === nombre);
    return producto ? producto.id : '';
  }

  // Helper para obtener ID del insumo por nombre
  private getInsumoIdPorNombre(nombre: string): string {
    const insumo = this.insumosDisponibles.find(i => i.nombre === nombre);
    return insumo ? insumo.id : '';
  }
}