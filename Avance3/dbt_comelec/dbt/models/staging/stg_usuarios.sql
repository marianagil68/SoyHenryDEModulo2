{{ config(
    alias='stg_usuarios'
) }}

with raw as (

    select
        id                as usuarioid,
        nombre            as nombre,
        apellido          as apellido,
        email             as email,
        ciudad            as ciudad,
        departamento      as departamento,
        password          as password,
        created_at        as fecha_creacion,
        updated_at        as fecha_actualizacion
    from {{ source('ecommerce', 'usuarios') }}

),

clean as (

    select
        usuarioid,
        trim(lower(nombre))        as nombre,
        trim(lower(apellido))      as apellido,
        lower(email)               as email,
        trim(ciudad)               as ciudad,
        trim(departamento)         as departamento,
        password,                  
        fecha_creacion,
        coalesce(fecha_actualizacion, fecha_creacion) as fecha_actualizacion
    from raw

)

select * from clean;
