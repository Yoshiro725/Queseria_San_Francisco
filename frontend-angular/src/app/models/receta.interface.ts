export interface InsumoReceta {
  insumo_id: string;
  nombre_insumo?: string;    // Para mostrar en el frontend
  cantidad: number;
  unidad: string;
}

export interface Receta {
  id: string;
  producto_id: string;
  nombre_producto?: string;  // Para mostrar en vez de "nombre"
  rendimiento: number;
  unidad_rendimiento: string; // Nombre correcto del backend
  observaciones: string;
  insumos: InsumoReceta[];
  estado: boolean;           // boolean en vez de string
}