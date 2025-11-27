#  Proyecto Integrador – Data Engineering: Optimización de Plataforma E-Commerce: Data Staging & Exploration

El primer avance contiene la primera etapa del desarrollo de una plataforma de datos para un sistema de ecommerce. El objetivo es construir la capa de **staging**, realizar la carga inicial desde archivos CSV, ejecutar un proceso de perfilamiento de datos y establecer las bases para futuras transformaciones y modelado analítico.

---
# PI 1 - Configuración del entorno de trabajo
##  Arquitectura del entorno

###  Base de datos (Docker + PostgreSQL)

El sistema utiliza **PostgreSQL** desplegado en un contenedor Docker, garantizando portabilidad y aislamiento del entorno.

###  Administración de la base

**pgAdmin 4** instalado en el host local se utiliza para la administración visual del servidor PostgreSQL.

###  Conexión desde Python

El proyecto implementa un módulo de conexión mediante **SQLAlchemy**, configurado con variables de entorno.

Las credenciales se almacenan en el archivo `.env`:

```
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=<password>
PG_DB=ecommerce
```

---

## 📂 Estructura del proyecto

```
project/
│── data/                                               # Archivos CSV originales
│── src/
│   ├── database/
│   │   ├── connection.py                               # Engine + Session
│   │   ├── models.py                                   # Tablas staging (sin FK)
│   ├── services/
│   │   ├── loader.py                                   # Proceso de ingestión inicial
│   │   ├── csv_factory.py
│   └── Avance1     /                                   # Análisis exploratorio
│       └── Avance1_Pi1_2_ORM_CreacionDeTablasYCarga.ipynb
│       └── Avence1_Pi3_CamposSemiEstructurados.iypnb
│       └── Avence1_Pi4_CalidadDeLosDatos.iypnb
│       └── Avence1_Pi4__modelo_datos.ipynb
│       └── Avence1_Pi5__ReporteDeHallazgos.ipynb
│   └── Avance2     /                                   # Mejora de detos, modelos, SCD y KPI
│       └── Hw0_MejorarLosDatosEnEsquemaProduction.sql
│       └── Hw1_KPI.ipynb
│       └── hw1_PreguntasDeNegocio.ipynb
│       └── hw1_PreguntasDeNegocio.sql
│       └── Hw2_Documentacion.pdf
│       └── Hw2_ModeloConceptual.jpg
│       └── Hw2_ModeloLogico.png
│       └── Hw3_4_5_DiagramaHechosDimensiones.png
│       └── Hw2_ModeloFisico.png
│       └── Hw7_DocumentacionFinalConSCD.pdf
│   └── Avance3     /                                   # Desarrollo de DBT
│       └── dbt
│           └── models
│               └── intermediate
│               └── marts
│               └── staging
│           └── target
│       └── docker-compose.yml
│       └── Dockerfile
│── .env
│── README.md
│── requirements.txt
```

---

## ⚙️ Configuración y despliegue

### 1. Levantar la base de datos con Docker

```bash
docker-compose up -d
```

Esto despliega:

* Servidor PostgreSQL
* Volumen persistente
* Puerto expuesto en `5432`

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar conexión (ORM)

La conexión se gestiona desde `src/database/connection.py` usando SQLAlchemy.

```python
engine = DB.engine()
SessionLocal = DB.session()
```

---
# PI2 - Carga inicial de datos
## Ingesta inicial de datos (Staging Layer)

La capa de staging permite cargar datos crudos provenientes de archivos CSV sin validación de integridad referencial.

### Creación de tablas

```python
from src.database.models import Base
from src.database.connection import DB
Base.metadata.create_all(DB.engine())
```

### Proceso de carga

```python
from src.services.loader import load_all
load_all()
```

### Registros cargados

| Tabla           | Filas |
| --------------- | ----- |
| usuarios        | 1000  |
| categorias      | 12    |
| productos       | 36    |
| ordenes         | 10000 |
| detalle_ordenes | 10000 |

---
# PI3 - Tratamiento de campos semiestructurados
## Revisión del contenido de las tablas

La capa de staging permite cargar datos crudos provenientes de archivos CSV sin validación de integridad referencial.


---

## Exploración y evaluación de calidad de datos

El análisis exploratorio combina consultas SQL y procesamiento en Python.

### Se evaluaron los siguientes aspectos:

* Valores nulos
* Duplicados
* Inconsistencias entre entidades
* Campos con formato no estándar o semi-estructurado
* Atributos clave y dependencias entre tablas

Los análisis se encuentran en:

```
src/exploration/
```

---


## Preguntas de negocio

### Ventas

* Productos más vendidos por volumen
* Ticket promedio
* Categorías con mayor volumen de ventas
* Actividad por día de la semana
* Variación mensual de órdenes

### Pagos

* Métodos de pago más utilizados
* Monto promedio por método
* Órdenes con múltiples métodos
* Pagos con estado fallido o procesando
* Recaudación mensual

### Usuarios

* Altas de usuarios por mes
* Usuarios con múltiples compras
* Usuarios registrados sin compras
* Usuarios con mayor gasto acumulado
* Usuarios que dejaron reseñas

### Productos y stock

* Productos con alto stock y bajas ventas
* Productos sin stock
* Productos peor calificados
* Productos con más reseñas
* Categorías con mayor valor económico vendido

---

## Avance 2 – Modelado, Mejora de Datos, SCD y KPIs

### Mejora de Datos en el Esquema Production
Durante este avance se implementaron procesos de estandarización, limpieza y enriquecimiento de datos dentro del esquema `production`. Entre las mejoras realizadas se incluyen:

- Normalización de formatos de texto y fechas.
- Corrección de claves inconsistentes entre entidades.
- Deduplicación y control de integridad.
- Transformación y validación de campos numéricos y categóricos.
- Ajustes derivados del análisis de calidad del avance 1.

El desarrollo se encuentra en:

```
src/Avance2/Hw0_MejorarLosDatosEnEsquemaProduction.sql
```

### Modelado Conceptual, Lógico y Físico
Se desarrollaron los modelos fundamentales para soportar el futuro Data Warehouse:

- Modelo conceptual: `Hw2_ModeloConceptual.jpg`
- Modelo lógico: `Hw2_ModeloLogico.png`
- Modelo físico: `Hw2_ModeloFisico.png`

Estos modelos definen entidades, relaciones, cardinalidades y reglas del negocio, y sirven como base para el diseño dimensional.

### Implementación de Slowly Changing Dimensions (SCD)
Se definió e implementó la estrategia de SCD Tipo 2 para dimensiones como usuarios, productos y categorías, preservando la trazabilidad histórica de cambios.

La documentación correspondiente se encuentra en:

```
src/Avance2/Hw7_DocumentacionFinalConSCD.pdf
```

### KPIs y Preguntas de Negocio
Se desarrollaron métricas y análisis orientados al negocio, incluyendo ventas, recaudación, ticket promedio, actividad de usuarios y comportamiento por categoría y producto.

Los materiales generados se encuentran en:

```
src/Avance2/Hw1_KPI.ipynb
src/Avance2/hw1_PreguntasDeNegocio.ipynb
src/Avance2/hw1_PreguntasDeNegocio.sql
src/Avance2/Hw2_Documentacion.pdf
```

---

## Avance 3 – Desarrollo del Proyecto con DBT

### Estructura del Proyecto DBT
Se construyó un proyecto DBT completo siguiendo un enfoque por capas:

```
src/Avance3/dbt/
│── models/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
│── target/
│── docker-compose.yml
│── Dockerfile
```

### Modelos Implementados

#### Modelos de staging
- Limpieza y estandarización de columnas.
- Tipificación de datos.
- Renombrado siguiendo convenciones DBT.

#### Modelos intermediate
- Transformaciones intermedias.
- Enriquecimiento de entidades.
- Cálculo de campos derivados.

#### Modelos marts (modelo dimensional)
- Tablas de hechos: ventas, detalle de órdenes, pagos.
- Dimensiones: productos, usuarios, categorías, fechas.
- Incorporación de SCD donde corresponde.

### Despliegue y Ejecución con Docker
Para garantizar un entorno reproducible se configuraron contenedores Docker:

- `Dockerfile` para la imagen de DBT.
- `docker-compose.yml` para ejecutar DBT junto con PostgreSQL.



### Autor
**Mariana Gil**  
Data Engineer | Proyecto Integrador – Curso de Data Engineering  
[LinkedIn](https://www.linkedin.com/in/mariana-gil-24667718/) · [GitHub](https://github.com/marianagil68/SoyHenryDEModulo2)