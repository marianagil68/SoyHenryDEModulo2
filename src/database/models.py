from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Numeric, ForeignKey, Text, Boolean, MetaData

class Base(DeclarativeBase):
    metadata = MetaData(schema="staging")

# Tabla: 1.usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    dni: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    contrasena: Mapped[str] = mapped_column(String(200), nullable=False)

# Tabla: 2.categorias
class Categoria(Base):
    __tablename__ = "categorias"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text)

# Tabla: 3.productos
class Producto(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)
    precio: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    categoria_id: Mapped[int] = mapped_column(Integer, nullable=False)

# Tabla: 4.ordenes
class Orden(Base):
    __tablename__ = "ordenes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_orden: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    total: Mapped[float] = mapped_column(Numeric(14,2), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)

# Tabla: 5.detalle_ordenes
class DetalleOrden(Base):
    __tablename__ = "detalle_ordenes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)

# Tabla: 6.direcciones_envio.csv 
class DireccionEnvio(Base):
    __tablename__ = "direcciones_envio"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    calle: Mapped[str | None] = mapped_column(String(200))
    ciudad: Mapped[str | None] = mapped_column(String(120))
    departamento: Mapped[str | None] = mapped_column(String(120))
    provincia: Mapped[str | None] = mapped_column(String(120))
    distrito: Mapped[str | None] = mapped_column(String(120))
    estado: Mapped[str | None] = mapped_column(String(120))
    codigo_postal: Mapped[str | None] = mapped_column(String(20))
    pais: Mapped[str | None] = mapped_column(String(80))

# Tabla: 7.carrito.csv 
class Carrito(Base):
    __tablename__ = "carrito"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_agregado: Mapped["DateTime"] = mapped_column(DateTime, nullable=True)

# Tabla: 8.metodos_pago.csv
class MetodoPago(Base):
    __tablename__ = "metodos_pago"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text)

# Tabla: 9.ordenes_metodospago.csv 
class OrdenMetodoPago(Base):
    __tablename__ = "ordenes_metodos_pago"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column(Integer, nullable=False)
    metodo_pago_id: Mapped[int] = mapped_column(Integer, nullable=False)
    monto_pagado: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)

# Tabla: 10.resenas_productos.csv
class ResenaProducto(Base):
    __tablename__ = "resenas_productos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, nullable=False)

    calificacion: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..5
    comentario: Mapped[str | None] = mapped_column(Text)
    fecha: Mapped["DateTime"] = mapped_column(DateTime, nullable=True)

# Tabla: 11.historial_pagos.csv
class HistorialPago(Base):
    __tablename__ = "historial_pagos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    orden_id: Mapped[int] = mapped_column(Integer, nullable=False)
    metodo_pago_id: Mapped[int] = mapped_column(Integer, nullable=True)

    monto: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    fecha_pago: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    estado_pago: Mapped[str | None] = mapped_column(String(50))
