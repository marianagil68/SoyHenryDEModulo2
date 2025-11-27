{{ config(alias='int_ventas_enriquecidas') }}

with v as (
    select * from {{ ref('stg_ventas') }}
),

u as (
    select * from {{ ref('DimUsuario') }}
),

p as (
    select * from {{ ref('DimProducto') }}
),

d as (
    select * from {{ ref('DimDireccionEnvio') }}
),

t as (
    select * from {{ ref('DimTiempo') }}
),

joined as (

    select
        v.hehoventaid,
        u.usuariosk,
        p.productosk,
        d.direccionsk,
        v.metodopagoid,
        t.fechapk,
        v.cantidad,
        v.total
    from v
    left join u
        on v.usuarioid = u.usuarioid
       and v.fecha_venta between u.fechainicio and u.fechafin
    left join p
        on v.productoid = p.productoid
       and v.fecha_venta between p.fechainicio and p.fechafin
    left join d
        on v.direccionid = d.direccionid
    left join t
        on date_trunc('day', v.fecha_venta)::date = t.fechapk
)

select * from joined;
