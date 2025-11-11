export interface InsumoFormulario {
    nombre: string;
    cantidad: string;
    stock: string;
    status: 'ok' | 'Bajo' | 'Agotado';
}