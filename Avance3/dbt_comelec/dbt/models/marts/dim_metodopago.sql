{{ config(alias='DimMetodoPago', materialized='table') }}

select
    metodopagoid,
    nombre,
    descripcion
from {{ ref('stg_metodos_pago') }};
