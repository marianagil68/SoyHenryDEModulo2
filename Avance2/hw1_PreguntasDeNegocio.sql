-- CONSULTAS PARA RESPONDER LAS PREGUNTAS DE NEGOCIO

-- PRIMER GRUPO: VENTAS

-- 1. Productos más vendidos por volumen
select p.nombre, SUM(det.cantidad) as total_vendido
from production.detalle_ordenes det
inner join production.productos p 
	on det.producto_id = p.id
group by p.nombre
order by total_vendido desc
limit 10

-- 2. Ticket promedio por orden
select avg(total) as ticket_promedio
from production.ordenes

-- 2. Variación para hacer KPI: Ticket promedio por mes

SELECT
    make_date(EXTRACT(YEAR FROM fecha_orden)::int,
              EXTRACT(MONTH FROM fecha_orden)::int,
              1) AS fecha,
    AVG(total) AS ticket_promedio
FROM production.ordenes
GROUP BY fecha
ORDER BY fecha;

-- 3. categorías con mayor número de productos vendidos
select c.nombre, sum(deo.cantidad) as productos_vendidos
from production.detalle_ordenes deo
inner join production.productos p on deo.producto_id = p.id
inner join production.categorias c ON c.id = p.categoria_id
group by c.nombre
order by productos_vendidos desc

-- 4. Día de la semana con más ventas
SELECT
    TO_CHAR(o.fecha_orden, 'Day') AS dia_de_la_semana,
    COUNT(*) AS ventas
FROM production.ordenes o
GROUP BY dia_de_la_semana
ORDER BY ventas DESC
LIMIT 1;

-- 5. Cuántas órdenes se generan cada mes y cuál es su variación
WITH resumen AS (
    SELECT
        EXTRACT(YEAR FROM fecha_orden)::int AS anio,
        EXTRACT(MONTH FROM fecha_orden)::int AS mes,
        COUNT(*) AS cantidad_ordenes
    FROM production.ordenes
    GROUP BY anio, mes
    ORDER BY anio, mes
)
SELECT
    anio,
    mes,
    cantidad_ordenes,
    ROUND(
        (cantidad_ordenes - LAG(cantidad_ordenes) OVER (ORDER BY anio, mes))::numeric
        / NULLIF(LAG(cantidad_ordenes) OVER (ORDER BY anio, mes), 0)
        * 100, 2
    ) AS variacion_porcentual
FROM resumen;

-- PAGOS Y TRANSACCIONES

-- 1. Cantidad de órdenes por mes
SELECT EXTRACT(YEAR FROM fecha_orden)::int as anio,
EXTRACT(MONTH FROM fecha_orden)::int as mes,
COUNT(*) as cantidad_ventas
FROM production.ordenes
GROUP BY anio, mes
ORDER BY anio, mes

-- 2. Métodos de pago más utilizados
select m.nombre as metodo_de_pago, count(*) as cantidad
from production.ordenes_metodos_pago o
inner join production.metodos_pago m ON m.id = o.metodo_pago_id
group by metodo_de_pago
order by cantidad desc

--3. Monto promedio por método de pago
select m.nombre as metodo_de_pago, avg(o.monto_pagado) as promedio
from production.ordenes_metodos_pago o
inner join production.metodos_pago m ON m.id = o.metodo_pago_id
group by metodo_de_pago
order by metodo_de_pago

-- 4. Órdenes pagadas con múltiples métodos
select o.orden_id orden, count(*) as cantidad
from production.ordenes_metodos_pago o
inner join production.metodos_pago m ON m.id = o.metodo_pago_id
group by orden
having count(*) > 1
order by orden desc

-- 5. monto total recaudado por mes
SELECT
    make_date(EXTRACT(YEAR FROM fecha_orden)::int,
              EXTRACT(MONTH FROM fecha_orden)::int,
              1) AS fecha,
    SUM(total) AS monto_total
FROM production.ordenes
GROUP BY fecha
ORDER BY fecha;



