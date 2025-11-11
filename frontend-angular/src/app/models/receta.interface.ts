export interface Receta {
    id: string;
    nombre: string;
    rendimiento: number; //la cantidad de rendimiento 
    unidad: string; //unida de rendimiento kg etc
    observaciones: string;
    estado: 'activo' | 'inactivo'; 
}