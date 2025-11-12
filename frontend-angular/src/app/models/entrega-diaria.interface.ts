//   src/app/models/entrega-diaria.interface.ts
export interface EntregaDiaria {
  id: string;
  proveedor_id: string;
  proveedor_nombre: string; // (Lo simularemos para la tabla)
  fecha: string; // (Usaremos un string simple para la simulación)
  cantidad: number; // Litros de leche
}