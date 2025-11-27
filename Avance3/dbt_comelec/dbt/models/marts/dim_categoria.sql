{{ config(alias='DimCategoria', materialized='table') }}

select
    categoriaid    as categoriaid,
    nombre,
    descripcion
from {{ ref('stg_categorias') }};
