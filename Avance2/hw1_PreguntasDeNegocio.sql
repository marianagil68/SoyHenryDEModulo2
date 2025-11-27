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

-- 5. monto total recaudado por mes
SELECT
    make_date(EXTRACT(YEAR FROM fecha_orden)::int,
              EXTRACT(MONTH FROM fecha_orden)::int,
              1) AS fecha,
    SUM(total) AS monto_total
FROM production.ordenes
GROUP BY fecha
ORDER BY fecha;



