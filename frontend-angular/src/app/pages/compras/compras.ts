import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Proveedor } from '../../models/proveedor.interface';
import { Insumo } from '../../models/insumo.interface';
import { 
  ReactiveFormsModule, 
  FormBuilder, 
  FormGroup, 
  FormArray, 
  Validators 
} from '@angular/forms';

@Component({
  selector: 'app-compras',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './compras.html',
  styleUrl: './compras.scss',
})
export class Compras implements OnInit{
  // --- Datos Simulados ---
  listaProveedores: Proveedor[] = [
    { id: '1', nombre: 'Lechería Don Pepe', domicilio: 'Camino Rural #120', estado: 'A' },
    { id: '2', nombre: 'Rancho Los Pinos', domicilio: 'Carretera Estatal #55', estado: 'A' },
    { id: '3', nombre: 'AgroInsumos San José', domicilio: 'Av. Ganadera 45', estado: 'I' }
  ];

  // Lista de insumos que se pueden comprar (para el dropdown)
  listaInsumos: Insumo[] = [
    { id: 'i1', nombre_insumo: 'Leche entera', unidad: 'L', stock_actual: 2500 },
    { id: 'i2', nombre_insumo: 'Sal', unidad: 'kg', stock_actual: 100 },
    { id: 'i3', nombre_insumo: 'Cuajo', unidad: 'mL', stock_actual: 500 },
    { id: 'i4', nombre_insumo: 'Azúcar', unidad: 'kg', stock_actual: 200 }
  ];

  // --- Lógica de la página ---
  proveedorSeleccionado: Proveedor | null = null;
  compraForm: FormGroup;

  constructor(private fb: FormBuilder) {
    // Definimos el formulario de "Registrar Compra"
    this.compraForm = this.fb.group({
      // El 'proveedor_id' se llenará con 'proveedorSeleccionado.id'
      // 'insumos' será una lista dinámica
      insumos: this.fb.array([]) 
    });
  }

  ngOnInit(): void {
    // Por defecto, seleccionamos el primer proveedor
    if (this.listaProveedores.length > 0) {
      this.seleccionarProveedor(this.listaProveedores[0]);
    }
  }

  // --- Métodos para el Formulario Dinámico ---
  get insumos() {
    return this.compraForm.get('insumos') as FormArray;
  }

  nuevoInsumo(): FormGroup {
    return this.fb.group({
      insumo_id: ['', Validators.required],
      cantidad: [0, [Validators.required, Validators.min(1)]],
      costo_unitario: [0, [Validators.required, Validators.min(0.01)]]
    });
  }

  agregarInsumo() {
    this.insumos.push(this.nuevoInsumo());
  }

  quitarInsumo(index: number) {
    this.insumos.removeAt(index);
  }

  // --- Métodos de la Página ---
  seleccionarProveedor(proveedor: Proveedor) {
    if (proveedor.estado === 'I') return; // No se puede seleccionar inactivos
    this.proveedorSeleccionado = proveedor;
    
    // Limpiamos el formulario al cambiar de proveedor
    this.insumos.clear();
    this.agregarInsumo(); // Añade una fila por defecto
  }

  registrarCompra() {
    if (!this.proveedorSeleccionado) {
      console.error('No hay proveedor seleccionado');
      return;
    }
    if (this.compraForm.invalid) {
      console.error('Formulario inválido');
      this.compraForm.markAllAsTouched();
      return;
    }

    const datosFinales = {
      proveedor_id: this.proveedorSeleccionado.id,
      ...this.compraForm.value
    };
    
    console.log('--- ENVIANDO COMPRA AL BACKEND ---', datosFinales);
    // Aquí iría la llamada al this.comprasService.crearCompra(...)
  }
}
