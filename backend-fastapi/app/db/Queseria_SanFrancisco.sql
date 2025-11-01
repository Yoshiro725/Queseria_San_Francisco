use Queseria_SanFrancisco


// ================================
// 1. CIUDADES
// ================================
db.ciudades.insertMany([
  { _id: ObjectId(), nom_ciudad: "Querétaro", estado: "Querétaro" },
  { _id: ObjectId(), nom_ciudad: "San Juan del Río", estado: "Querétaro" },
  { _id: ObjectId(), nom_ciudad: "Celaya", estado: "Guanajuato" }
]);

// ================================
// 2. PROVEEDORES
// ================================
db.proveedores.insertMany([
  {
    _id: ObjectId(),
    nombre: "Lechería Don Pepe",
    estado: "A",
    domicilio: "Camino Rural #120",
    ciudad: { nom_ciudad: "Querétaro", estado: "Querétaro" }
  },
  {
    _id: ObjectId(),
    nombre: "Rancho Los Pinos",
    estado: "A",
    domicilio: "Carretera Estatal #55",
    ciudad: { nom_ciudad: "San Juan del Río", estado: "Querétaro" }
  }
]);

// ================================
// 3. CLIENTES
// ================================
db.clientes.insertMany([
  {
    _id: ObjectId(),
    nombre_cliente: "Supermercado El Buen Queso",
    RFC_cliente: "BQ123456789",
    domicilio: "Av. Central 200, Querétaro",
    ciudad: { nom_ciudad: "Querétaro", estado: "Querétaro" }
  }
]);

// ================================
// 4. CATEGORÍAS DE INSUMOS
// ================================
db.categorias_insumo.insertMany([
  { _id: ObjectId(), nombre_categoria: "Materia Prima" },
  { _id: ObjectId(), nombre_categoria: "Embalaje" },
  { _id: ObjectId(), nombre_categoria: "Ingrediente" },
  { _id: ObjectId(), nombre_categoria: "Derivado" }
]);

// ================================
// 5. INSUMOS
// ================================
db.insumos.insertMany([
  {
    _id: ObjectId(),
    nombre_insumo: "Leche entera",
    unidad: "L",
    categoria: "Materia Prima",
    stock_actual: 2500,
    stock_minimo: 500,
    costo_unitario: 12.5
  },
  {
    _id: ObjectId(),
    nombre_insumo: "Sal",
    unidad: "kg",
    categoria: "Ingrediente",
    stock_actual: 100,
    stock_minimo: 10,
    costo_unitario: 5.0
  }
]);

// ================================
// 6. MOVIMIENTOS DE INSUMOS
// ================================
db.movimientos_insumo.insertMany([
  {
    id_insumo: "Leche entera",
    fecha: new Date(),
    tipo_mov: "Entrada",
    cantidad: 500,
    descripcion: "Compra semanal a proveedores"
  },
  {
    id_insumo: "Sal",
    fecha: new Date(),
    tipo_mov: "Salida",
    cantidad: 2,
    descripcion: "Uso en producción de queso fresco"
  }
]);

// ================================
// 7. PRODUCTOS LÁCTEOS
// ================================
db.productos_lacteos.insertMany([
  {
    _id: ObjectId(),
    desc_queso: "Queso Fresco",
    precio: 90,
    totalInventario: 50
  },
  {
    _id: ObjectId(),
    desc_queso: "Quesillo",
    precio: 120,
    totalInventario: 30
  }
]);

// ================================
// 8. RECETAS
// ================================
db.recetas.insertMany([
  {
    _id: ObjectId(),
    nombre_producto: "Queso Fresco",
    rendimiento: 10,
    unidad_rendimiento: "kg",
    observaciones: "Receta base",
    insumos: [
      { nombre: "Leche entera", cantidad: 100, unidad: "L" },
      { nombre: "Sal", cantidad: 2, unidad: "kg" }
    ]
  }
]);

// ================================
// 9. DERIVADOS
// ================================
db.derivados.insertMany([
  {
    _id: ObjectId(),
    receta_origen: "Queso Fresco",
    nombre_derivado: "Suero de leche",
    cantidad_generada: 5,
    unidad: "L"
  }
]);

// ================================
// 10. PRODUCCIÓN
// ================================
db.producciones.insertMany([
  {
    _id: ObjectId(),
    receta: "Queso Fresco",
    fecha_produccion: new Date(),
    cantidad_producida: 10,
    unidad: "kg",
    observaciones: "Lote de prueba",
    insumos_consumidos: [
      { nombre: "Leche entera", cantidad: 100 },
      { nombre: "Sal", cantidad: 2 }
    ]
  }
]);

// ================================
// 11. INVENTARIO DE PRODUCTOS TERMINADOS
// ================================
db.inventario_productos.insertMany([
  {
    _id: ObjectId(),
    producto: "Queso Fresco",
    fecha_entrada: new Date(),
    cantidad_disponible: 10,
    costo_unitario: 80,
    ubicacion: "Almacén Central"
  }
]);

// ================================
// 12. VENTAS
// ================================
db.ventas.insertMany([
  {
    _id: ObjectId(),
    fecha_venta: new Date(),
    total: 900,
    IVA: 144,
    cliente: "Supermercado El Buen Queso",
    detalle: [
      { producto: "Queso Fresco", cantidad: 10, precioVenta: 90 }
    ]
  }
]);

// ================================
// 13. PRECIO DEL LITRO DE LECHE
// ================================
db.precios_litro.insertMany([
  {
    anno: 2025,
    semana: 44,
    fec_ini: new Date("2025-10-28"),
    fec_fin: new Date("2025-11-03"),
    precio: 12.5
  }
]);

// ================================
// 14. ENTREGAS DIARIAS
// ================================
db.entregas_diarias.insertMany([
  {
    proveedor: "Lechería Don Pepe",
    fecha: new Date("2025-10-29"),
    cantidad: 500
  }
]);

// ================================
// 15. PAGOS SEMANALES
// ================================
db.pagos_semanales.insertMany([
  {
    proveedor: "Lechería Don Pepe",
    anno: 2025,
    semana: 44,
    importe: 6250,
    cantidad: 500
  }
]);

// ================================
// 16. DENOMINACIONES
// ================================
db.denominaciones.insertMany([
  { nominal: 20 },
  { nominal: 50 },
  { nominal: 100 },
  { nominal: 200 },
  { nominal: 500 }
]);

// ================================
// 17. DISTRIBUCIÓN DE PAGOS
// ================================
db.distribucion_pagos.insertMany([
  {
    proveedor: "Lechería Don Pepe",
    anno: 2025,
    semana: 44,
    denominacion: 200,
    cantidad: 25
  }
]);

// ================================
// 18. REPORTES DE INVENTARIO
// ================================
db.reportes_inventario.insertMany([
  {
    fecha: new Date(),
    tipo: "General",
    descripcion: "Inventario actualizado de insumos y productos terminados"
  }
]);

// ================================
// 19. REPORTES DE PRODUCCIÓN
// ================================
db.reportes_produccion.insertMany([
  {
    fecha_inicio: new Date("2025-10-20"),
    fecha_fin: new Date("2025-10-27"),
    total_producido: 100,
    observaciones: "Producción estable durante la semana"
  }
]);
