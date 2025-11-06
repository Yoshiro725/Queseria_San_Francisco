import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
// --- 1. Importa las herramientas para formularios ---
import { 
  ReactiveFormsModule, 
  FormBuilder, 
  FormGroup, 
  FormArray, 
  Validators 
} from '@angular/forms';

@Component({
  selector: 'app-nueva-receta-modal',
  standalone: true,
  // --- 2. Añade ReactiveFormsModule a los imports ---
  imports: [CommonModule, ReactiveFormsModule], 
  templateUrl: './nueva-receta-modal.html',
  styleUrl: './nueva-receta-modal.scss'
})
export class NuevaRecetaModal {
  @Output() cerrar = new EventEmitter<void>();

  // --- 3. Define tu Formulario Principal ---
  recetaForm: FormGroup;

  // --- 4. Inyecta el FormBuilder (constructor) ---
  constructor(private fb: FormBuilder) {
      this.recetaForm = this.fb.group({
      
      // --- SECCIÓN 1 (Se queda igual) ---
      nombre: ['', Validators.required],
      categoria: ['Queso', Validators.required],
      descripcion: [''],
      estado: ['Activo'],

      // --- SECCIÓN 2 (Se queda igual) ---
      insumos: this.fb.array([]),

      // --- 3. AÑADE ESTA NUEVA SECCIÓN ---
      rendimiento: this.fb.group({
        cantidadProducida: ['', Validators.required],
        unidadRendimiento: ['kg', Validators.required],
        rangoOpcional: [''],
        // El porcentaje lo calcularemos luego, por ahora es solo un campo
        porcentajeRendimiento: [{ value: '', disabled: true }] 
      })

    });
  }

  // --- 6. Getter para acceder fácil a 'insumos' desde el HTML ---
  get insumos() {
    return this.recetaForm.get('insumos') as FormArray;
  }

  // --- 7. Método para crear un nuevo FormGroup de insumo ---
  nuevoInsumo(): FormGroup {
    return this.fb.group({
      nombre: ['', Validators.required],
      cantidad: ['', Validators.required],
      unidad: ['kg', Validators.required]
    });
  }

  // --- 8. Método para AÑADIR un insumo a la lista ---
  agregarInsumo() {
    this.insumos.push(this.nuevoInsumo());
  }

  // --- 9. Método para QUITAR un insumo de la lista ---
  quitarInsumo(index: number) {
    this.insumos.removeAt(index);
  }

  // --- (Tu método de cerrar se queda igual) ---
  onCerrarClick(): void {
    this.cerrar.emit();
  }

  // --- 10. Método para guardar (por ahora solo imprime) ---
  guardarReceta() {
    if (this.recetaForm.valid) {
      console.log('Formulario Válido:', this.recetaForm.value);
      // Aquí iría la llamada al servicio
      // this.onCerrarClick(); // Cierra el modal al guardar
    } else {
      console.log('Formulario Inválido');
      // Marcar campos como tocados para mostrar errores
      this.recetaForm.markAllAsTouched(); 
    }
  }

}