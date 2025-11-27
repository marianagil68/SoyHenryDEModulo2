{{ config(alias='int_dim_usuario_scd') }}

with base as (

    select
        usuarioid,
        nombre,
        apellido,
        email,
        ciudad,
        departamento,
        password,
        fecha_actualizacion as fecha_cambio
    from {{ ref('stg_usuarios') }}

),

ordenado as (

    select
        *,
        lead(fecha_cambio) over (
            partition by usuarioid
            order by fecha_cambio
        ) as fecha_siguiente
    from base
),

rango_fechas as (

    select
        usuarioid,
        nombre,
        apellido,
        email,
        ciudad,
        departamento,
        password,
        fecha_cambio                           as fechainicio,
        coalesce(fecha_siguiente, '9999-12-31') as fechafin,
        case when fecha_siguiente is null then true else false end as esactual
    from ordenado
)

select * from rango_fechas;
