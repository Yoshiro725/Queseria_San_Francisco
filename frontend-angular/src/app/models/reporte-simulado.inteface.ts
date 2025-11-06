//   src/app/models/reporte-simulado.interface.ts

export interface ReporteSimulado {
  fecha: string;
  // Usamos tipos específicos para que el filtro sea exacto
  tipo: 'Venta' | 'Producción' | 'Inventario'; 
  descripcion: string;
}