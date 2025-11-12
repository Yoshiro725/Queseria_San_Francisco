import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  ReactiveFormsModule, 
  FormBuilder, 
  FormGroup, 
  FormArray, 
  Validators 
} from '@angular/forms';

// Interfaces para Pestaña 1
import { Proveedor } from '../../models/proveedor.interface';
import { Insumo } from '../../models/insumo.interface';

// Interfaces para Pestaña 2
import { EntregaDiaria } from '../../models/entrega-diaria.interface';
import { PrecioLitro } from '../../models/precio-litro.interface';
import { PagoSemanal } from '../../models/pago-semanal.interface'; // <-- 1. IMPORTA LA NUEVA INTERFACE

// Componentes (Modales)
import { NuevoProveedorModal } from '../../components/nuevo-proveedor-modal/nuevo-proveedor-modal';

@Component({
  selector: 'app-compras',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, NuevoProveedorModal],
  templateUrl: './compras.html',
  styleUrl: './compras.scss'
})
export class Compras implements OnInit {

  // --- Variable para los TABS ---
  activeTab: string = 'registro';

  // --- Variables para Pestaña 1: REGISTRO ---
  listaProveedores: Proveedor[] = [
    { id: '1', nombre: 'Lechería Don Pepe', domicilio: 'Camino Rural #120', estado: 'A' },
    { id: '2', nombre: 'Rancho Los Pinos', domicilio: 'Carretera Estatal #55', estado: 'A' },
    { id: '3', nombre: 'AgroInsumos San José', domicilio: 'Av. Ganadera 45', estado: 'I' }
  ];
  listaInsumos: Insumo[] = [
    { id: 'i1', nombre_insumo: 'Leche entera', unidad: 'L', stock_actual: 2500 },
    { id: 'i2', nombre_insumo: 'Sal', unidad: 'kg', stock_actual: 100 },
  ];
  proveedorSeleccionado: Proveedor | null = null;
  compraForm: FormGroup;
  isProveedorModalOpen = false;

  // --- Variables para Pestaña 2: PAGOS Y ENTREGAS ---
  listaEntregas: EntregaDiaria[] = [
    { id: 'e1', proveedor_id: '1', proveedor_nombre: 'Lechería Don Pepe', fecha: '2025-11-12', cantidad: 500 },
    { id: 'e2', proveedor_id: '2', proveedor_nombre: 'Rancho Los Pinos', fecha: '2025-11-12', cantidad: 350 },
    { id: 'e3', proveedor_id: '1', proveedor_nombre: 'Lechería Don Pepe', fecha: '2025-11-11', cantidad: 490 }
  ];
  precioLecheActual: PrecioLitro = {
    id: 'p1', semana: 45, anno: 2025, precio: 12.50
  };
  entregaForm: FormGroup;
  precioForm: FormGroup;
  
  // --- 2. AÑADE LA NUEVA LISTA DE DATOS SIMULADOS ---
  listaPagos: PagoSemanal[] = [
    { id: 'ps1', proveedor_nombre: 'Lechería Don Pepe', anno: 2025, semana: 44, importe: 6125, cantidad: 490 },
    { id: 'ps2', proveedor_nombre: 'Rancho Los Pinos', anno: 2025, semana: 44, importe: 4375, cantidad: 350 }
  ];


  constructor(private fb: FormBuilder) {
    // Formulario para Pestaña 1
    this.compraForm = this.fb.group({
      insumos: this.fb.array([]) 
    });

    // Formularios para Pestaña 2
    this.entregaForm = this.fb.group({
      proveedor_id: ['', Validators.required],
      fecha: [new Date().toISOString().split('T')[0], Validators.required],
      cantidad: [null, [Validators.required, Validators.min(1)]]
    });

    this.precioForm = this.fb.group({
      precio: [12.50, [Validators.required, Validators.min(0.01)]]
    });
  }

  ngOnInit(): void {
    if (this.listaProveedores.length > 0) {
      this.seleccionarProveedor(this.listaProveedores[0]);
    }
    this.precioForm.setValue({ precio: this.precioLecheActual.precio });
  }

  // --- Método para los TABS ---
  seleccionarTab(tab: string): void {
    this.activeTab = tab;
  }

  // --- Métodos de Pestaña 1: REGISTRO ---
  get insumos() { return this.compraForm.get('insumos') as FormArray; }
  nuevoInsumo(): FormGroup { /* ... (tu código) ... */ 
    return this.fb.group({
      insumo_id: ['', Validators.required],
      cantidad: [0, [Validators.required, Validators.min(1)]],
      costo_unitario: [0, [Validators.required, Validators.min(0.01)]]
    });
  }
  agregarInsumo() { this.insumos.push(this.nuevoInsumo()); }
  quitarInsumo(index: number) { this.insumos.removeAt(index); }
  seleccionarProveedor(proveedor: Proveedor) { /* ... (tu código) ... */ 
    if (proveedor.estado === 'I') return;
    this.proveedorSeleccionado = proveedor;
    this.insumos.clear();
    this.agregarInsumo();
  }
  registrarCompra() { /* ... (tu código) ... */ 
    if (!this.proveedorSeleccionado || this.compraForm.invalid) {
      this.compraForm.markAllAsTouched(); return;
    }
    console.log('--- ENVIANDO COMPRA AL BACKEND ---', {
      proveedor_id: this.proveedorSeleccionado.id, ...this.compraForm.value
    });
  }
  abrirModalProveedor(): void { this.isProveedorModalOpen = true; }
  cerrarModalProveedor(): void { this.isProveedorModalOpen = false; }


  // --- Métodos de Pestaña 2: PAGOS Y ENTREGAS ---
  
  registrarEntrega(): void {
    if (this.entregaForm.invalid) {
      this.entregaForm.markAllAsTouched(); return;
    }
    console.log('--- REGISTRANDO ENTREGA ---', this.entregaForm.value);
  }

  actualizarPrecio(): void {
    if (this.precioForm.invalid) return;
    console.log('--- ACTUALIZANDO PRECIO DE LA LECHE ---', this.precioForm.value);
  }

  // --- 3. AÑADE EL NUEVO MÉTODO PARA GENERAR PAGOS ---
  generarPagos(): void {
    console.log('--- GENERANDO PAGOS SEMANALES ---');
    // Lógica futura:
    // 1. Llamar al servicio para que el backend calcule
    //    (Entregas de la semana * Precio de la semana)
    // 2. Guardar en 'db.pagos_semanales'
    // 3. Refrescar 'listaPagos'
    alert('¡Pagos generados! (Simulación)');
  }
}