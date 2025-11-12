export interface ProductoLacteo {
  _id?: string; // El ID de MongoDB, opcional en la creación
  desc_queso: string; // Descripción o nombre del queso
  codigo_barras?: string; // Campo para el código de barras del producto terminado
  precio: number;
  totalInventario: number; // Stock actual del producto terminado
}