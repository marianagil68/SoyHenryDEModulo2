#  Proyecto Integrador – Data Engineering: Optimización de Plataforma E-Commerce

### Descripción general
Este proyecto tiene como objetivo el diseño e implementación de una arquitectura de datos escalable para un e-commerce en crecimiento.  
El trabajo principal es **centralizar fuentes CSV dispersas** en una base de datos relacional optimizada (PostgreSQL), **modelar un esquema dimensional** y permitir el análisis de métricas clave del negocio en ventas, logística y marketing.

### Objetivos principales
- Unificar múltiples fuentes de datos (CSV) en un modelo relacional consistente.  
- Diseñar un **modelo de datos dimensional (Star Schema)** que facilite consultas analíticas.  
- Implementar un **pipeline reproducible** para carga y transformación de datos.  
- Optimizar el rendimiento mediante índices, relaciones y vistas materializadas.  
- Responder preguntas de negocio clave relacionadas con ventas, clientes, logística y finanzas.

###  Tecnología utilizadap
- **Python 3.12.6**
- **PostgreSQL** (Docker + pgAdmin)
- **SQLAlchemy ORM**
- **Pandas**
- **Docker Desktop**
- **Jupyter Notebook / VS Code**
- **Patrones de diseño:** Singleton / Factory para la gestión de sesiones y conexión.

### Arquitectura del proyecto
```bash
project/
│
├── README.md
├── .env
├── requirements.txt
├── docker-compose.yml
├── data/
│   ├── clientes.csv
│   ├── productos.csv
│   ├── ventas.csv
│   └── ...
├── src/
│   ├── main.py
│   ├── database/
│   │   ├── connection.py        # patrón Singleton para engine y session
│   │   └── models.py            # clases ORM
│   ├── services/
│   │   └── loader.py            # carga desde CSV a PostgreSQL
│   └── utils/
│       └── factory.py           # patrón Factory para manejo modular
└── notebooks/
    └── exploracion.ipynb
```

### Preguntas de negocio abordadas
- Productos más vendidos por categoría y periodo.  
- Identificación de clientes recurrentes vs. nuevos.  
- Análisis de rotación de stock y demoras logísticas.  
- Impacto de campañas de marketing en ventas.  
- Evolución mensual de ingresos y rentabilidad por categoría.  
- Distribución geográfica de clientes y oportunidades de expansión.

---

### Flujo general
1. **Creación del entorno** y despliegue de contenedor PostgreSQL.  
2. **Diseño del modelo ORM** y generación de tablas desde SQLAlchemy.  
3. **Carga automática de datos CSV** mediante scripts Python.  
4. **Consultas analíticas** y visualización de resultados en notebooks.  
5. **Optimización** (índices, vistas materializadas, etc.).

---

### Autor
**Mariana Gil**  
Data Engineer | Proyecto Integrador – Curso de Data Engineering  
[LinkedIn](https://www.linkedin.com/in/mariana-gil-24667718/) · [GitHub](https://github.com/marianagil68/SoyHenryDEModulo2)