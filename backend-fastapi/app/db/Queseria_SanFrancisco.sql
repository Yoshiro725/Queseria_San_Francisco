use Queseria_SanFrancisco

// ================================
// 1. CIUDADES
// ================================
const queretaroId = ObjectId();
const sanJuanId = ObjectId();
const celayaId = ObjectId();

db.ciudades.insertMany([
  { _id: queretaroId, nom_ciudad: "Querétaro", estado: "Querétaro" },
  { _id: sanJuanId, nom_ciudad: "San Juan del Río", estado: "Querétaro" },
  { _id: celayaId, nom_ciudad: "Celaya", estado: "Guanajuato" }
]);

// ================================
// 2. PROVEEDORES
// ================================
const donPepeId = ObjectId();
const losPinosId = ObjectId();

db.proveedores.insertMany([
  {
    _id: donPepeId,
    nombre: "Lechería Don Pepe",
    estado: "A",
    domicilio: "Camino Rural #120",
    ciudad_id: queretaroId
  },
  {
    _id: losPinosId,
    nombre: "Rancho Los Pinos",
    estado: "A",
    domicilio: "Carretera Estatal #55",
    ciudad_id: sanJuanId
  }
]);

// ================================
// 3. CLIENTES
// ================================
const supermercadoId = ObjectId();

db.clientes.insertMany([
  {
    _id: supermercadoId,
    nombre_cliente: "Supermercado El Buen Queso",
    RFC_cliente: "BQ123456789",
    domicilio: "Av. Central 200, Querétaro",
    ciudad_id: queretaroId
  }
]);

// ================================
// 4. CATEGORÍAS DE INSUMOS
// ================================
const catMateriaId = ObjectId();
const catEmbalajeId = ObjectId();
const catIngredienteId = ObjectId();
const catDerivadoId = ObjectId();

db.categorias_insumo.insertMany([
  { _id: catMateriaId, nombre_categoria: "Materia Prima" },
  { _id: catEmbalajeId, nombre_categoria: "Embalaje" },
  { _id: catIngredienteId, nombre_categoria: "Ingrediente" },
  { _id: catDerivadoId, nombre_categoria: "Derivado" }
]);

// ================================
// 5. INSUMOS
// ================================
const lecheId = ObjectId();
const salId = ObjectId();

db.insumos.insertMany([
  {
    _id: lecheId,
    nombre_insumo: "Leche entera",
    unidad: "L",
    categoria_id: catMateriaId,
    stock_actual: 2500,
    stock_minimo: 500,
    costo_unitario: 12.5
  },
  {
    _id: salId,
    nombre_insumo: "Sal",
    unidad: "kg",
    categoria_id: catIngredienteId,
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
    insumo_id: lecheId,
    fecha: new Date(),
    tipo_mov: "Entrada",
    cantidad: 500,
    descripcion: "Compra semanal a proveedores"
  },
  {
    insumo_id: salId,
    fecha: new Date(),
    tipo_mov: "Salida",
    cantidad: 2,
    descripcion: "Uso en producción de queso fresco"
  }
]);

// ================================
// 7. PRODUCTOS LÁCTEOS
// ================================
const quesoFrescoId = ObjectId();
const quesilloId = ObjectId();

db.productos_lacteos.insertMany([
  { _id: quesoFrescoId, desc_queso: "Queso Fresco", precio: 90, totalInventario: 50 },
  { _id: quesilloId, desc_queso: "Quesillo", precio: 120, totalInventario: 30 }
]);

// ================================
// 8. RECETAS
// ================================
db.recetas.insertMany([
  {
    _id: ObjectId(),
    producto_id: quesoFrescoId,
    rendimiento: 10,
    unidad_rendimiento: "kg",
    observaciones: "Receta base",
    insumos: [
      { insumo_id: lecheId, cantidad: 100, unidad: "L" },
      { insumo_id: salId, cantidad: 2, unidad: "kg" }
    ]
  }
]);

// ================================
// 9. DERIVADOS
// ================================
db.derivados.insertMany([
  {
    _id: ObjectId(),
    receta_origen_id: quesoFrescoId,
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
    receta_id: quesoFrescoId,
    fecha_produccion: new Date(),
    cantidad_producida: 10,
    unidad: "kg",
    observaciones: "Lote de prueba",
    insumos_consumidos: [
      { insumo_id: lecheId, cantidad: 100 },
      { insumo_id: salId, cantidad: 2 }
    ]
  }
]);

// ================================
// 11. INVENTARIO DE PRODUCTOS TERMINADOS
// ================================
db.inventario_productos.insertMany([
  {
    _id: ObjectId(),
    producto_id: quesoFrescoId,
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
    cliente_id: supermercadoId,
    detalle: [
      { producto_id: quesoFrescoId, cantidad: 10, precioVenta: 90 }
    ]
  }
]);

// ================================
// 13. PRECIO DEL LITRO DE LECHE
// ================================
db.precios_litro.insertMany([
  {
    _id: ObjectId(),
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
    _id: ObjectId(),
    proveedor_id: donPepeId,
    fecha: new Date("2025-10-29"),
    cantidad: 500
  }
]);

// ================================
// 15. PAGOS SEMANALES
// ================================
db.pagos_semanales.insertMany([
  {
    _id: ObjectId(),
    proveedor_id: donPepeId,
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
  { _id: ObjectId(), nominal: 20 },
  { _id: ObjectId(), nominal: 50 },
  { _id: ObjectId(), nominal: 100 },
  { _id: ObjectId(), nominal: 200 },
  { _id: ObjectId(), nominal: 500 }
]);

// ================================
// 17. DISTRIBUCIÓN DE PAGOS
// ================================
db.distribucion_pagos.insertMany([
  {
    _id: ObjectId(),
    proveedor_id: donPepeId,
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
    _id: ObjectId(),
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
    _id: ObjectId(),
    fecha_inicio: new Date("2025-10-20"),
    fecha_fin: new Date("2025-10-27"),
    total_producido: 100,
    observaciones: "Producción estable durante la semana"
  }
]);




// ================================
// Inserts
// ================================

// 1. Insertar 2 nuevos insumos
const azucarId = ObjectId();
const mantequillaId = ObjectId();

db.insumos.insertMany([
  {
    _id: azucarId,
    nombre_insumo: "Azúcar",
    unidad: "kg",
    categoria_id: catIngredienteId,
    stock_actual: 200,
    stock_minimo: 20,
    costo_unitario: 8.0
  },
  {
    _id: mantequillaId,
    nombre_insumo: "Mantequilla",
    unidad: "kg",
    categoria_id: catMateriaId,
    stock_actual: 50,
    stock_minimo: 10,
    costo_unitario: 50
  }
]);

// 2. Insertar un nuevo producto lácteo
const requesonId = ObjectId();

db.productos_lacteos.insertOne({
  _id: requesonId,
  desc_queso: "Requesón",
  precio: 70,
  totalInventario: 20
});

// 3. Insertar una nueva venta usando `_id`
db.ventas.insertOne({
  _id: ObjectId(),
  fecha_venta: new Date(),
  total: 350,
  IVA: 56,
  cliente_id: supermercadoId,
  detalle: [
    { producto_id: requesonId, cantidad: 5, precioVenta: 70 }
  ]
});

// 4. Insertar un movimiento de insumo
db.movimientos_insumo.insertOne({
  _id: ObjectId(),
  insumo_id: azucarId,
  fecha: new Date(),
  tipo_mov: "Entrada",
  cantidad: 50,
  descripcion: "Compra semanal"
});

// 5. Insertar un nuevo reporte de inventario
db.reportes_inventario.insertOne({
  _id: ObjectId(),
  fecha: new Date(),
  tipo: "General",
  descripcion: "Reporte de prueba con Requesón"
});

// ================================
// Consultas
// ================================

// 1. Ver todos los insumos
db.insumos.find().pretty()

// 2. Ver todos los productos lácteos
db.productos_lacteos.find().pretty()

// 3. Ver todas las ventas con el detalle de productos
db.ventas.find().pretty()

// 4. Buscar movimientos de un insumo específico (ej. Azúcar)
db.movimientos_insumo.find({ insumo_id: azucarId }).pretty()

// 5. Ver todos los reportes de inventario
db.reportes_inventario.find().pretty()


const venta = db.ventas.findOne({ _id: ObjectId("6913582d0e21d45e781e2451") });

if (venta && venta.detalle) {
  venta.detalle.forEach(item => {
    db.productos_lacteos.updateOne(
      { _id: item.producto_id },
      { $inc: { totalInventario: -item.cantidad } }
    );
  });
} else {
  print("⚠️ No se encontró la venta o no tiene detalle.");
}


//Insertar un ejemplo // Crear una venta de ejemplo con productos vendidos
const producto1 = ObjectId();
const producto2 = ObjectId();

db.productos_lacteos.insertMany([
  { _id: producto1, nombre: "Queso Fresco", totalInventario: 50 },
  { _id: producto2, nombre: "Queso Oaxaca", totalInventario: 30 }
]);

db.ventas.insertOne({
  fecha_venta: new Date(),
  cliente: "Supermercado El Buen Queso",
  detalle: [
    { producto_id: producto1, cantidad: 5 },
    { producto_id: producto2, cantidad: 3 }
  ]
});




db.productos_lacteos.find().pretty()




// 1️⃣ Insertar una nueva venta
const nuevaVenta = {
  fecha_venta: new Date(),
  cliente_id: ObjectId("690d23adcbc976714263b13d"), // Cliente existente
  total: 250,
  IVA: 40,
  detalle: [
    { producto_id: ObjectId("690d23adcbc976714263b146"), cantidad: 3, precioVenta: 90 }, // Queso Fresco
    { producto_id: ObjectId("690d23afcbc976714263b15a"), cantidad: 2, precioVenta: 70 }  // Requesón
  ]
};

db.ventas.insertOne(nuevaVenta);



// 1️⃣ Insertar una nueva venta y guardar el ID generado
const resultadoVenta = db.ventas.insertOne({
  fecha_venta: new Date(),
  cliente_id: ObjectId("690d23adcbc976714263b13d"),
  total: 250,
  IVA: 40,
  detalle: [
    { producto_id: ObjectId("690d23adcbc976714263b146"), cantidad: 3, precioVenta: 90 },
    { producto_id: ObjectId("690d23afcbc976714263b15a"), cantidad: 2, precioVenta: 70 }
  ]
});

// Guardar el ID en una variable
const venta = db.ventas.findOne({ _id: resultadoVenta.insertedId });

// 2️⃣ Verificar si hay suficiente inventario antes de rebajar stock
let stockSuficiente = true;

venta.detalle.forEach(item => {
  const producto = db.productos_lacteos.findOne({ _id: item.producto_id });
  if (!producto || producto.totalInventario < item.cantidad) {
    stockSuficiente = false;
    print(`❌ No hay suficiente stock de: ${producto ? producto.desc_queso : 'Producto no encontrado'}`);
  }
});

if (stockSuficiente) {
  print("✅ Stock suficiente. Descontando inventario...");
} else {
  print("⛔ Venta detenida por falta de inventario.");
}



if (stockSuficiente) {
  venta.detalle.forEach(item => {
    db.productos_lacteos.updateOne(
      { _id: item.producto_id },
      { $inc: { totalInventario: -item.cantidad } }
    );
  });
  print("✅ Inventario actualizado correctamente.");
}



Inserts 

db.proveedores.insertMany([
  {
    nombre: "Lácteos del Norte",
    telefono: "5553214567",
    direccion: "Carretera Lechera Km 12, Chihuahua"
  },
  {
    nombre: "AgroInsumos San José",
    telefono: "5556547890",
    direccion: "Av. Ganadera 45, Querétaro"
  },
  {
    nombre: "Granja El Potrero",
    telefono: "5558796543",
    direccion: "Rancho El Rosario, Jalisco"
  },
  {
    nombre: "Sistemas Alimentarios MX",
    telefono: "5559012345",
    direccion: "Parque Industrial los Pinos, CDMX"
  },
  {
    nombre: "Santa Clara Proveeduría",
    telefono: "5551135789",
    direccion: "Zona Rural 23, Hidalgo"
  }
]);


db.insumos.insertMany([
  { nombre: "Leche de Vaca", unidad: "Litros", costoUnitario: 15, stockActual: 500 },
  { nombre: "Cuajo", unidad: "Gramos", costoUnitario: 4, stockActual: 200 },
  { nombre: "Sal", unidad: "Kg", costoUnitario: 10, stockActual: 50 },
  { nombre: "Cloruro de Calcio", unidad: "Litros", costoUnitario: 25, stockActual: 30 },
  { nombre: "Fermento Láctico", unidad: "Gramos", costoUnitario: 8, stockActual: 100 }
]);


db.producciones.insertMany([
  {
    fecha: new Date(),
    producto_id: ObjectId(), // remplazar por ID real de "Queso Fresco"
    cantidadProducida: 20,
    insumos_usados: [
      { insumo: "Leche de Vaca", cantidad: 100 },
      { insumo: "Cuajo", cantidad: 10 }
    ]
  },
  {
    fecha: new Date(),
    producto_id: ObjectId(), // "Requesón"
    cantidadProducida: 15,
    insumos_usados: [
      { insumo: "Leche de Vaca", cantidad: 80 },
      { insumo: "Sal", cantidad: 5 }
    ]
  }
]);


db.producciones.insertMany([
  {
    fecha: new Date(),
    producto_id: ObjectId(), // remplazar por ID real de "Queso Fresco"
    cantidadProducida: 20,
    insumos_usados: [
      { insumo: "Leche de Vaca", cantidad: 100 },
      { insumo: "Cuajo", cantidad: 10 }
    ]
  },
  {
    fecha: new Date(),
    producto_id: ObjectId(), // "Requesón"
    cantidadProducida: 15,
    insumos_usados: [
      { insumo: "Leche de Vaca", cantidad: 80 },
      { insumo: "Sal", cantidad: 5 }
    ]
  }
]);


db.ventas.insertMany([
  {
    fecha_venta: new Date(),
    cliente_id: ObjectId(), // Cliente 1
    total: 900,
    IVA: 144,
    detalle: [
      { producto_id: ObjectId(), cantidad: 10, precioVenta: 90 } // Queso Fresco
    ]
  },
  {
    fecha_venta: new Date(),
    cliente_id: ObjectId(), // Cliente 2
    total: 350,
    IVA: 56,
    detalle: [
      { producto_id: ObjectId(), cantidad: 5, precioVenta: 70 } // Requesón
    ]
  }
]);



INSERTS COMPLETOS con ObjectId() reales

// === PRODUCTOS LÁCTEOS ===
const quesoFresco = {
  _id: ObjectId(),
  desc_queso: "Queso Fresco",
  precio: 90,
  totalInventario: 50
};

const requeson = {
  _id: ObjectId(),
  desc_queso: "Requesón",
  precio: 70,
  totalInventario: 30
};

db.productos_lacteos.insertMany([quesoFresco, requeson]);

// === CLIENTES ===
const cliente1 = {
  _id: ObjectId(),
  nombre_cliente: "Supermercado El Buen Queso",
  RFC_cliente: "BQ123456789",
  domicilio: "Av. Central 200",
  ciudad: "Querétaro"
};

const cliente2 = {
  _id: ObjectId(),
  nombre_cliente: "Distribuidora Láctea MX",
  RFC_cliente: "DLX987654321",
  domicilio: "Calle Industria 45",
  ciudad: "CDMX"
};

db.clientes.insertMany([cliente1, cliente2]);


2. INSERTS de VENTAS usando IDs reales

// === VENTA 1 ===
db.ventas.insertOne({
  _id: ObjectId(),
  fecha_venta: new Date(),
  cliente_id: cliente1._id,
  total: 900,
  IVA: 144,
  detalle: [
    { producto_id: quesoFresco._id, cantidad: 10, precioVenta: 90 }
  ]
});

// === VENTA 2 ===
db.ventas.insertOne({
  _id: ObjectId(),
  fecha_venta: new Date(),
  cliente_id: cliente2._id,
  total: 350,
  IVA: 56,
  detalle: [
    { producto_id: requeson._id, cantidad: 5, precioVenta: 70 }
  ]
});


Consulta para ver resultado de la venta + producto
db.ventas.aggregate([
  {
    $lookup: {
      from: "productos_lacteos",
      localField: "detalle.producto_id",
      foreignField: "_id",
      as: "productos_detalle"
    }
  }
]).pretty();

Descontar automáticamente stock del inventario

// 1️⃣ Buscar la última venta
const ultimaVenta = db.ventas.findOne({}, { sort: { _id: -1 } });

// 2️⃣ Restar inventario de cada producto vendido
ultimaVenta.detalle.forEach(item => {
  db.productos_lacteos.updateOne(
    { _id: item.producto_id },
    { $inc: { totalInventario: -item.cantidad } }
  );
});


Ver si se actualizó el inventario

db.productos_lacteos.find().pretty();


Validar stock antes de vender (alerta de falta de inventario)

let venta = db.ventas.findOne({ _id: ultimaVenta._id });
let stockSuficiente = true;

venta.detalle.forEach(item => {
  const producto = db.productos_lacteos.findOne({ _id: item.producto_id });
  if (!producto || producto.totalInventario < item.cantidad) {
    stockSuficiente = false;
    print(`❌ Stock insuficiente de: ${producto ? producto.desc_queso : "Producto no encontrado"}`);
  }
});

if (stockSuficiente) {
  print("✅ Stock suficiente. Descontando inventario...");
} else {
  print("⛔ Venta detenida por falta de inventario.");
}






