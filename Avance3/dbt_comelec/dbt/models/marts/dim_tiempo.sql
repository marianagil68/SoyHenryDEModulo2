{{ config(alias='DimTiempo', materialized='table') }}

with fechas as (

    select
        date_trunc('day', fecha_venta)::date as fecha
    from {{ ref('stg_ventas') }}
    group by 1
),

dim as (

    select
        fecha                      as fechapk,
        extract(year  from fecha)  as año,
        extract(month from fecha)  as mes,
        extract(day   from fecha)  as día,
        ceil(extract(month from fecha) / 3.0)::int as trimestre
    from fechas
)

select * from dim;
