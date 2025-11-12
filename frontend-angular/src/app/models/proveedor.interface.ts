//   src/app/models/proveedor.interface.ts
export interface Proveedor {
  id: string;
  nombre: string;
  domicilio: string;
  estado: 'A' | 'I';
}