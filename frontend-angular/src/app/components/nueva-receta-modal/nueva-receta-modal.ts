import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-nueva-receta-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './nueva-receta-modal.html',
  styleUrl: './nueva-receta-modal.scss',
})
export class NuevaRecetaModal {
// 'Output' es como un "emisor" de eventos.
  // 'cerrar' es el nombre del evento que 'produccion.html' escucha.
  @Output() cerrar = new EventEmitter<void>();

  // Esta función se llamará desde nuestro HTML para emitir el evento.
  onCerrarClick(): void {
    this.cerrar.emit();
  }
}
