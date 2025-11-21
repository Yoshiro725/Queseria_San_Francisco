import { Component, EventEmitter, Output, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-modal-produccion',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule], 
  templateUrl: './modal-produccion.html',
  styleUrl: './modal-produccion.scss'
})
export class ModalProduccionComponent implements OnInit {
  @Output() cerrar = new EventEmitter<void>();
  @Output() produccionCreada = new EventEmitter<any>();

  @Input() recetaSeleccionada: any; // Recibe la receta seleccionada
  @Input() insumos: any[] = []; // Recibe los insumos para verificar stock
  @Input() cantidadProducir: number = 1; // Recibe la cantidad ya seleccionada

  loading = false;
  codigoBarrasGenerado: string = '';

  constructor() {}

  ngOnInit() {
    // Generar código de barras al abrir el modal
    this.codigoBarrasGenerado = this.generarCodigoBarras();
  }

  onCerrarClick(): void {
    this.cerrar.emit();
  }

  crearProduccion() {
    this.loading = true;

    const produccionData = {
      receta: this.recetaSeleccionada,
      cantidad: this.cantidadProducir,
      fechaProduccion: new Date().toISOString(),
      codigoBarras: this.codigoBarrasGenerado,
      totalProducido: this.recetaSeleccionada.rendimiento * this.cantidadProducir
    };

    // Simular proceso de producción
    setTimeout(() => {
      this.loading = false;
      this.produccionCreada.emit(produccionData);
      this.onCerrarClick();
    }, 1500);
  }

  // Función para obtener el nombre del insumo
  getNombreInsumo(insumoId: string): string {
    const insumo = this.insumos.find(i => i.id === insumoId);
    return insumo ? insumo.nombre_insumo : 'Insumo no encontrado';
  }

  generarCodigoBarras(): string {
    const timestamp = Date.now().toString();
    const random = Math.random().toString(36).substr(2, 9).toUpperCase();
    return `CB-${timestamp}-${random}`;
  }
}