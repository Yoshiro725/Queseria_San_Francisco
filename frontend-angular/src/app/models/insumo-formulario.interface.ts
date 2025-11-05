export interface InsumoFormulario {
    nombre: string;
    cantidad: string;
    stock: string;
    status: 'ok' | 'low' | 'out';
}