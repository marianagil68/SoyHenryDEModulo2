{{ config(
    alias='DimUsuario',
    materialized='table'
) }}

with historico as (

    select * from {{ ref('int_dim_usuario_scd') }}

),

dim as (

    select
        {{ dbt_utils.surrogate_key(['usuarioid', 'fechainicio']) }} as usuariosk,
        usuarioid,
        nombre,
        apellido,
        email,
        ciudad,
        departamento,
        fechainicio,
        fechafin,
        esactual
    from historico
)

select * from dim;
