from __future__ import annotations
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class CSVSource:
    path: str
    required_cols: list[str]
    friendly_name: str

class CSVFactory:
    """Factory: devuelve metadatos de la fuente CSV por nombre lógico."""
    # BASE_DIR = os.getenv("DATA_DIR", "./data")
    # BASE_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "../data"))
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

    SOURCES = {
        "usuarios": CSVSource(
            path=os.path.join(BASE_DIR, "1.Usuarios.csv"),
            required_cols=["Nombre", "Apellido", "DNI", "Email", "Contraseña"],
            friendly_name="Usuarios"
        ),
        "categorias": CSVSource(
            path=os.path.join(BASE_DIR, "2.Categorias.csv"),
            required_cols=["Nombre", "Descripcion"],
            friendly_name="Categorias"
        ),
        "productos": CSVSource(
            path=os.path.join(BASE_DIR, "3.Productos.csv"),
            required_cols=["Nombre", "Descripcion", "Precio", "Stock", "CategoriaID"],
            friendly_name="Productos"
        ),
        "ordenes": CSVSource(
            path=os.path.join(BASE_DIR, "4.ordenes.csv"),
            required_cols=["UsuarioID", "FechaOrden", "Total", "Estado"],
            friendly_name="Ordenes"
        ),
        "detalle": CSVSource(
            path=os.path.join(BASE_DIR, "5.detalle_ordenes.csv"),
            required_cols=["OrdenID", "ProductoID", "Cantidad", "PrecioUnitario"],
            friendly_name="DetalleOrdenes"
        ),
        "direcciones_envio": CSVSource(
            path=os.path.join(BASE_DIR, "6.direcciones_envio.csv"),
            required_cols=[
                "UsuarioID","Calle","Ciudad","Departamento","Provincia",
                "Distrito","Estado","CodigoPostal","Pais"
            ],
            friendly_name="DireccionesEnvio"
        ),
        "carrito": CSVSource(
            path=os.path.join(BASE_DIR, "7.carrito.csv"),
            required_cols=["UsuarioID","ProductoID","Cantidad","FechaAgregado"],
            friendly_name="Carrito"
        ),
        "metodos_pago": CSVSource(
            path=os.path.join(BASE_DIR, "8.metodos_pago.csv"),
            required_cols=["Nombre","Descripcion"],
            friendly_name="MetodosPago"
        ),
        "ordenes_metodos_pago": CSVSource(
            path=os.path.join(BASE_DIR, "9.ordenes_metodospago.csv"),
            required_cols=["OrdenID","MetodoPagoID","MontoPagado"],
            friendly_name="OrdenesMetodosPago"
        ),
        "resenas_productos": CSVSource(
            path=os.path.join(BASE_DIR, "10.resenas_productos.csv"),
            required_cols=["UsuarioID","ProductoID","Calificacion","Comentario","Fecha"],
            friendly_name="ResenasProductos"
        ),
        "historial_pagos": CSVSource(
            path=os.path.join(BASE_DIR, "11.historial_pagos.csv"),
            required_cols=["OrdenID","MetodoPagoID","Monto","FechaPago","EstadoPago"],
            friendly_name="HistorialPagos"
        ),
    }

    @classmethod
    def get(cls, key: str) -> CSVSource:
        if key not in cls.SOURCES:
            raise KeyError(f"CSV '{key}' no configurado")
        return cls.SOURCES[key]
