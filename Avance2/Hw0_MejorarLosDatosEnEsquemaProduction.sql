-- Creación y volcado de las tablas staging a production
-- Creación de las claves primarias y foráneas

CREATE SCHEMA IF NOT EXISTS production;

CREATE TABLE production.usuarios AS
SELECT * FROM staging.usuarios;

ALTER TABLE production.usuarios
    ADD PRIMARY KEY (id);

ALTER TABLE production.usuarios
    ADD CONSTRAINT usuarios_dni_key UNIQUE (dni);

ALTER TABLE production.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


CREATE TABLE production.categorias AS
SELECT * FROM staging.categorias;

ALTER TABLE production.categorias
    ADD PRIMARY KEY (id);

ALTER TABLE production.categorias
    ADD CONSTRAINT categorias_nombre_key UNIQUE (nombre);

CREATE TABLE production.productos AS
SELECT * FROM staging.productos;

ALTER TABLE production.productos
    ADD PRIMARY KEY (id);

ALTER TABLE production.productos
    ADD CONSTRAINT fk_productos_categoria
    FOREIGN KEY (categoria_id) REFERENCES production.categorias(id);

CREATE TABLE production.direcciones_envio AS
SELECT * FROM staging.direcciones_envio;

ALTER TABLE production.direcciones_envio
    ADD PRIMARY KEY (id);

ALTER TABLE production.direcciones_envio
    ADD CONSTRAINT fk_direcciones_usuario
    FOREIGN KEY (usuario_id) REFERENCES production.usuarios(id);

CREATE TABLE production.ordenes AS
SELECT * FROM staging.ordenes;

ALTER TABLE production.ordenes
    ADD PRIMARY KEY (id);

ALTER TABLE production.ordenes
    ADD CONSTRAINT fk_ordenes_usuario
    FOREIGN KEY (usuario_id) REFERENCES production.usuarios(id);

CREATE TABLE production.detalle_ordenes AS
SELECT * FROM staging.detalle_ordenes;

ALTER TABLE production.detalle_ordenes
    ADD PRIMARY KEY (id);

ALTER TABLE production.detalle_ordenes
    ADD CONSTRAINT fk_detalle_ordenes_orden
    FOREIGN KEY (orden_id) REFERENCES production.ordenes(id);

ALTER TABLE production.detalle_ordenes
    ADD CONSTRAINT fk_detalle_ordenes_producto
    FOREIGN KEY (producto_id) REFERENCES production.productos(id);

CREATE TABLE production.metodos_pago AS
SELECT * FROM staging.metodos_pago;

ALTER TABLE production.metodos_pago
    ADD PRIMARY KEY (id);

ALTER TABLE production.metodos_pago
    ADD CONSTRAINT metodos_pago_nombre_key UNIQUE (nombre);

CREATE TABLE production.ordenes_metodos_pago AS
SELECT * FROM staging.ordenes_metodos_pago;

ALTER TABLE production.ordenes_metodos_pago
    ADD PRIMARY KEY (id);

ALTER TABLE production.ordenes_metodos_pago
    ADD CONSTRAINT fk_omp_orden
    FOREIGN KEY (orden_id) REFERENCES production.ordenes(id);

ALTER TABLE production.ordenes_metodos_pago
    ADD CONSTRAINT fk_omp_metodo_pago
    FOREIGN KEY (metodo_pago_id) REFERENCES production.metodos_pago(id);

CREATE TABLE production.historial_pagos AS
SELECT * FROM staging.historial_pagos;

ALTER TABLE production.historial_pagos
    ADD PRIMARY KEY (id);

ALTER TABLE production.historial_pagos
    ADD CONSTRAINT fk_historial_orden
    FOREIGN KEY (orden_id) REFERENCES production.ordenes(id);

ALTER TABLE production.historial_pagos
    ADD CONSTRAINT fk_historial_metodo_pago
    FOREIGN KEY (metodo_pago_id) REFERENCES production.metodos_pago(id);

CREATE TABLE production.resenas_productos AS
SELECT * FROM staging.resenas_productos;

ALTER TABLE production.resenas_productos
    ADD PRIMARY KEY (id);

ALTER TABLE production.resenas_productos
    ADD CONSTRAINT fk_resena_usuario
    FOREIGN KEY (usuario_id) REFERENCES production.usuarios(id);

ALTER TABLE production.resenas_productos
    ADD CONSTRAINT fk_resena_producto
    FOREIGN KEY (producto_id) REFERENCES production.productos(id);

CREATE TABLE production.carrito AS
SELECT * FROM staging.carrito;

ALTER TABLE production.carrito
    ADD PRIMARY KEY (id);

ALTER TABLE production.carrito
    ADD CONSTRAINT fk_carrito_usuario
    FOREIGN KEY (usuario_id) REFERENCES production.usuarios(id);

ALTER TABLE production.carrito
    ADD CONSTRAINT fk_carrito_producto
    FOREIGN KEY (producto_id) REFERENCES production.productos(id);

-- Creación de las tablas SCD: contraseñas y precios

CREATE TABLE production.productos_precio_scd (
    precio_scd_id   SERIAL PRIMARY KEY,
    producto_id     INTEGER NOT NULL,
    precio          NUMERIC(12,2) NOT NULL,
    fecha_inicio    TIMESTAMP NOT NULL,
    fecha_fin       TIMESTAMP,
    es_actual       BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_pps_producto
        FOREIGN KEY (producto_id)
        REFERENCES production.productos(id)
);

INSERT INTO production.productos_precio_scd (
    producto_id,
    precio,
    fecha_inicio,
    fecha_fin,
    es_actual
)
SELECT
    p.id          AS producto_id,
    p.precio,
    NOW()         AS fecha_inicio,
    NULL          AS fecha_fin,
    TRUE          AS es_actual
FROM production.productos p;


CREATE TABLE production.usuarios_contrasena_scd (
    contrasena_scd_id  SERIAL PRIMARY KEY,
    usuario_id         INTEGER NOT NULL,
    contrasena         VARCHAR(200) NOT NULL,   -- idealmente HASH
    fecha_inicio       TIMESTAMP NOT NULL,
    fecha_fin          TIMESTAMP,
    es_actual          BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_ucs_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES production.usuarios(id)
);

INSERT INTO production.usuarios_contrasena_scd (
    usuario_id,
    contrasena,
    fecha_inicio,
    fecha_fin,
    es_actual
)
SELECT
    u.id           AS usuario_id,
    u.contrasena,
    NOW()          AS fecha_inicio,
    NULL           AS fecha_fin,
    TRUE           AS es_actual
FROM production.usuarios u;

-- Arreglo la inconsistencia del total de orden con la suma del detalle
WITH total_detalles AS (
    SELECT 
        orden_id, 
        SUM(cantidad * precio_unitario) AS total_detalle
    FROM production.detalle_ordenes
    GROUP BY orden_id
)
UPDATE production.ordenes o
SET total = d.total_detalle
FROM total_detalles d
WHERE o.id = d.orden_id
  AND o.total <> d.total_detalle;
