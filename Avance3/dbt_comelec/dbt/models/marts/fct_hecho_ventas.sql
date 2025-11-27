{{ config(
    alias='HechoVentas',
    materialized='table'
) }}

select * from {{ ref('int_ventas_enriquecidas') }};
