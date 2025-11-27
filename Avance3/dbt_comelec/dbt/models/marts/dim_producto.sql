{{ config(
    alias='DimProducto',
    materialized='table'
) }}

with historico as (

    select * from {{ ref('int_dim_producto_scd') }}

),

dim as (

    select
        {{ dbt_utils.surrogate_key(['productoid', 'fechainicio']) }} as productosk,
        productoid,
        nombre,
        precio,
        stock,
        categoriaid,
        fechainicio,
        fechafin,
        esactual
    from historico
)

select * from dim;
