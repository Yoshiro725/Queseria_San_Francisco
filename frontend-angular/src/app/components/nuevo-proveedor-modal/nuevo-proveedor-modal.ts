import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
// --- 1. Importa las herramientas de formularios ---
import { 
  ReactiveFormsModule, 
  FormBuilder, 
  FormGroup, 
  Validators 
} from '@angular/forms';

@Component({
  selector: 'app-nuevo-proveedor-modal',
  standalone: true,
  // --- 2. Añade ReactiveFormsModule ---
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './nuevo-proveedor-modal.html',
  styleUrl: './nuevo-proveedor-modal.scss'
})
export class NuevoProveedorModal {
  
  // --- 3. Lógica para emitir el evento 'cerrar' ---
  @Output() cerrar = new EventEmitter<void>();

  // --- 4. Lógica del formulario ---
  proveedorForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.proveedorForm = this.fb.group({
      nombre: ['', Validators.required],
      domicilio: ['', Validators.required],
      estado: ['A', Validators.required] // Por defecto 'Activo'
    });
  }

  onCerrarClick(): void {
    this.cerrar.emit();
  }

  guardarProveedor(): void {
    if (this.proveedorForm.valid) {
      console.log('--- ENVIANDO NUEVO PROVEEDOR ---', this.proveedorForm.value);
      // Aquí iría la llamada al this.proveedorService.crearProveedor(...)
      
      // (Opcional) Luego puedes cerrar el modal y refrescar la lista
      this.onCerrarClick(); 
    } else {
      console.error('Formulario de proveedor inválido');
      this.proveedorForm.markAllAsTouched();
    }
  }

}