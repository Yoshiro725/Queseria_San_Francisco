import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { ProductoLacteo } from '../../models/producto-lacteo.interface';

@Component({
  selector: 'app-nueva-venta-modal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './nueva-venta-modal.html',
  styleUrls: ['./nueva-venta-modal.scss']
})
export class NuevaVentaModal implements OnInit {
  @Output() cerrar = new EventEmitter<void>();

  ventaForm: FormGroup;
  totalVenta: number = 0;

  // Simulación de productos que podrías obtener de tu inventario
  // **CAMBIO:** Se actualiza la estructura para que coincida con la interfaz ProductoLacteo
  productosDisponibles: ProductoLacteo[] = [
    { _id: 'prod-01', desc_queso: 'Queso Fresco 1kg', precio: 90, totalInventario: 50, codigo_barras: '850100200202' },
    { _id: 'prod-02', desc_queso: 'Quesillo 1kg', precio: 110, totalInventario: 30, codigo_barras: '850100200203' },
    { _id: 'prod-03', desc_queso: 'Requesón 500g', precio: 45, totalInventario: 25, codigo_barras: '850100200204' },
    { _id: 'prod-04', desc_queso: 'Crema 1L', precio: 80, totalInventario: 15, codigo_barras: '850100200205' },
  ];

  constructor(private fb: FormBuilder) {
    this.ventaForm = this.fb.group({
      cliente: ['Cliente General'],
      productos: this.fb.array([])
    });
  }

  ngOnInit(): void {
    // Agrega un producto vacío al iniciar
    this.agregarProducto();

    // Escucha cambios en los productos para recalcular el total
    this.productos.valueChanges.subscribe(productos => {
      this.recalcularTotal(productos);
    });
  }

  get productos() {
    return this.ventaForm.get('productos') as FormArray;
  }

  nuevoProducto(): FormGroup {
    return this.fb.group({
      productoId: ['', Validators.required],
      nombre: [{ value: '', disabled: true }],
      cantidad: [1, [Validators.required, Validators.min(1)]],
      precioUnitario: [0],
      subtotal: [{ value: 0, disabled: true }]
    });
  }

  agregarProducto() {
    this.productos.push(this.nuevoProducto());
  }

  quitarProducto(index: number) {
    this.productos.removeAt(index);
  }

  onProductoSeleccionado(index: number, event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    const productoId = selectElement.value;
    // **CAMBIO:** Se busca por `_id` en lugar de `id`
    const productoSeleccionado = this.productosDisponibles.find(p => p._id === productoId);

    if (productoSeleccionado) {
      const productoFormGroup = this.productos.at(index);
      productoFormGroup.patchValue({
        nombre: productoSeleccionado.desc_queso, // **CAMBIO:** Se usa `desc_queso`
        precioUnitario: productoSeleccionado.precio
      });
    }
  }

  recalcularTotal(productos: any[]) {
    this.totalVenta = productos.reduce((acc, prod) => {
      const subtotal = (prod.cantidad || 0) * (prod.precioUnitario || 0);
      const productoControl = this.productos.controls.find(c => c.value === prod);
      if (productoControl) {
        productoControl.get('subtotal')?.setValue(subtotal, { emitEvent: false });
      }
      return acc + subtotal;
    }, 0);
  }

  onCerrarClick(): void {
    this.cerrar.emit();
  }

  guardarVenta() {
    if (this.ventaForm.valid) {
      console.log('Venta Guardada:', this.ventaForm.getRawValue());
      // Aquí llamarías a tu servicio para guardar la venta en la BD
      this.onCerrarClick(); // Cierra el modal después de guardar
    } else {
      console.log('Formulario de venta inválido');
      this.ventaForm.markAllAsTouched();
    }
  }
}
