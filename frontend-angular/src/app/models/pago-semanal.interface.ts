//   src/app/models/pago-semanal.interface.ts

export interface PagoSemanal {
  id: string;
  proveedor_nombre: string; // Simulado (en la BD real es proveedor_id)
  anno: number;
  semana: number;
  importe: number; // El total en $
  cantidad: number; // El total en Litros
}