from __future__ import annotations
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from src.database.connection import DB
from src.database.models import Base, Usuario, Categoria, Producto, Orden, DetalleOrden, DireccionEnvio, MetodoPago, OrdenMetodoPago, ResenaProducto,HistorialPago, Carrito
from src.services.csv_factory import CSVFactory

def create_schema():
    """Crea las tablas según modelos ORM."""
    Base.metadata.create_all(DB.engine())

def _df_required(df: pd.DataFrame, required_cols: list[str]):
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")

def load_usuarios(sess: Session):
    src = CSVFactory.get("usuarios")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)
    objs = [
        Usuario(
            nombre=row["Nombre"],
            apellido=row["Apellido"],
            dni=str(row["DNI"]),
            email=str(row["Email"]).strip(),
            contrasena=str(row["Contraseña"]),
        )
        for _, row in df.iterrows()
    ]
    sess.bulk_save_objects(objs)

def load_categorias(sess: Session):
    src = CSVFactory.get("categorias")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)
    objs = [Categoria(nombre=row["Nombre"], descripcion=row["Descripcion"]) for _, row in df.iterrows()]
    sess.bulk_save_objects(objs)

def load_productos(sess: Session):
    src = CSVFactory.get("productos")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)
    objs = [
        Producto(
            nombre=row["Nombre"],
            descripcion=row["Descripcion"],
            precio=float(row["Precio"]),
            stock=int(row["Stock"]),
            categoria_id=int(row["CategoriaID"]),
        )
        for _, row in df.iterrows()
    ]
    sess.bulk_save_objects(objs)

def load_ordenes(sess: Session):
    src = CSVFactory.get("ordenes")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)
    # parseo fecha
    df["FechaOrden"] = pd.to_datetime(df["FechaOrden"])
    objs = [
        Orden(
            usuario_id=int(row["UsuarioID"]),
            fecha_orden=row["FechaOrden"].to_pydatetime(),
            total=float(row["Total"]),
            estado=str(row["Estado"]),
        )
        for _, row in df.iterrows()
    ]
    # Para obtener ids consistentes con Detalle, usamos inserción por orden natural
    sess.bulk_save_objects(objs)

def load_detalle(sess: Session):
    src = CSVFactory.get("detalle")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)
    objs = [
        DetalleOrden(
            orden_id=int(row["OrdenID"]),
            producto_id=int(row["ProductoID"]),
            cantidad=int(row["Cantidad"]),
            precio_unitario=float(row["PrecioUnitario"]),
        )
        for _, row in df.iterrows()
    ]
    sess.bulk_save_objects(objs)

def load_direcciones_envio(sess: Session):
    src = CSVFactory.get("direcciones_envio")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)

    objs = [
        DireccionEnvio(
            usuario_id=int(r["UsuarioID"]),
            calle=(None if pd.isna(r["Calle"]) else str(r["Calle"])),
            ciudad=(None if pd.isna(r["Ciudad"]) else str(r["Ciudad"])),
            departamento=(None if pd.isna(r["Departamento"]) else str(r["Departamento"])),
            provincia=(None if pd.isna(r["Provincia"]) else str(r["Provincia"])),
            distrito=(None if pd.isna(r["Distrito"]) else str(r["Distrito"])),
            estado=(None if pd.isna(r["Estado"]) else str(r["Estado"])),
            codigo_postal=(None if pd.isna(r["CodigoPostal"]) else str(r["CodigoPostal"])),
            pais=(None if pd.isna(r["Pais"]) else str(r["Pais"])),
        )
        for _, r in df.iterrows()
    ]
    sess.bulk_save_objects(objs)


def load_metodos_pago(sess: Session):
    src = CSVFactory.get("metodos_pago")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)

    objs = [
        MetodoPago(
            nombre=str(r["Nombre"]).strip(),
            descripcion=None if pd.isna(r["Descripcion"]) else str(r["Descripcion"])
        )
        for _, r in df.iterrows()
    ]
    sess.bulk_save_objects(objs)


def load_ordenes_metodos_pago(sess: Session):
    src = CSVFactory.get("ordenes_metodos_pago")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)

    objs = [
        OrdenMetodoPago(
            orden_id=int(r["OrdenID"]),
            metodo_pago_id=int(r["MetodoPagoID"]),
            monto_pagado=float(r["MontoPagado"])
        )
        for _, r in df.iterrows()
    ]
    sess.bulk_save_objects(objs)


def load_resenas_productos(sess: Session):
    src = CSVFactory.get("resenas_productos")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)

    # parseo de fecha (permite vacíos)
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

    objs = [
        ResenaProducto(
            usuario_id=int(r["UsuarioID"]),
            producto_id=int(r["ProductoID"]),
            calificacion=int(r["Calificacion"]),
            comentario=None if pd.isna(r["Comentario"]) else str(r["Comentario"]),
            fecha=None if pd.isna(r["Fecha"]) else r["Fecha"].to_pydatetime(),
        )
        for _, r in df.iterrows()
    ]
    sess.bulk_save_objects(objs)


def load_historial_pagos(sess: Session):
    src = CSVFactory.get("historial_pagos")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)

    df["FechaPago"] = pd.to_datetime(df["FechaPago"], errors="coerce")

    objs = [
        HistorialPago(
            orden_id=int(r["OrdenID"]),
            metodo_pago_id=None if pd.isna(r["MetodoPagoID"]) else int(r["MetodoPagoID"]),
            monto=float(r["Monto"]),
            fecha_pago=None if pd.isna(r["FechaPago"]) else r["FechaPago"].to_pydatetime(),
            estado_pago=None if pd.isna(r["EstadoPago"]) else str(r["EstadoPago"]),
        )
        for _, r in df.iterrows()
    ]
    sess.bulk_save_objects(objs)


def load_carrito(sess: Session):
    src = CSVFactory.get("carrito")
    df = pd.read_csv(src.path)
    _df_required(df, src.required_cols)

    df["FechaAgregado"] = pd.to_datetime(df["FechaAgregado"], errors="coerce")

    objs = [
        Carrito(
            usuario_id=int(r["UsuarioID"]),
            producto_id=int(r["ProductoID"]),
            cantidad=int(r["Cantidad"]),
            fecha_agregado=None if pd.isna(r["FechaAgregado"]) else r["FechaAgregado"].to_pydatetime(),
        )
        for _, r in df.iterrows()
    ]
    sess.bulk_save_objects(objs)

def load_all():
    """Crea tablas y carga en orden correcto (FKs)."""
    create_schema()
    SessionLocal = DB.session()
    with SessionLocal() as sess:
        try:
           # bases
            load_usuarios(sess)
            load_categorias(sess)

            # catálogos dependientes / maestros
            load_metodos_pago(sess)

            # entidades que dependen de maestros
            load_productos(sess)          # depende de categorias
            load_ordenes(sess)            # depende de usuarios
            load_direcciones_envio(sess)  # depende de usuarios

            # detalle y asociaciones
            load_detalle(sess)            # depende de ordenes y productos
            load_ordenes_metodos_pago(sess)  # depende de ordenes y metodos_pago

            # actividad derivada
            load_resenas_productos(sess)  # depende de usuarios y productos
            load_historial_pagos(sess)    # depende de ordenes (y opcionalmente metodos_pago)
            load_carrito(sess)            # depende de usuarios y productos

            sess.commit()

        except Exception:
            sess.rollback()
            raise
