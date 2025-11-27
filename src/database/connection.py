from __future__ import annotations
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

class DB:
    """Singleton para administrar Engine y Session."""
    _engine = None
    _SessionLocal = None

    @staticmethod
    def _server_url_no_db() -> str:
        user = os.getenv("PG_USER")
        pwd = os.getenv("PG_PASSWORD")
        host = os.getenv("PG_HOST", "localhost")
        port = os.getenv("PG_PORT", "5432")
        # URL al "server" usando DB postgres por defecto
        return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/postgres"

    @staticmethod
    def _db_url() -> str:
        user = os.getenv("PG_USER")
        pwd = os.getenv("PG_PASSWORD")
        host = os.getenv("PG_HOST", "localhost")
        port = os.getenv("PG_PORT", "5432")
        db   = os.getenv("PG_DB", "ecommerce")
        return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"

    @classmethod
    def ensure_database(cls):
        """Crea la base si no existe (conecta a 'postgres' y hace CREATE DATABASE)."""
        target_db = os.getenv("PG_DB", "ecommerce")
        server_engine = create_engine(cls._server_url_no_db(), isolation_level="AUTOCOMMIT")
        with server_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :d"), {"d": target_db}
            ).scalar()
            if not exists:
                conn.execute(text(f'CREATE DATABASE "{target_db}"'))
        server_engine.dispose()

    @classmethod
    def ensure_schemas(cls):
        """Crea los esquemas necesarios si no existen."""
        engine = create_engine(cls._db_url(), isolation_level="AUTOCOMMIT")

        with engine.connect() as conn:
            conn.execute(text('CREATE SCHEMA IF NOT EXISTS staging'))
            # Si quisieras otros:
            # conn.execute(text('CREATE SCHEMA IF NOT EXISTS raw'))
            # conn.execute(text('CREATE SCHEMA IF NOT EXISTS mart'))

        engine.dispose()

    @classmethod
    def engine(cls):
        """Devuelve (y crea una única vez) el Engine a la DB objetivo."""
        if cls._engine is None:
            cls.ensure_database()
            cls.ensure_schemas()
            cls._engine = create_engine(cls._db_url(), echo=False, future=True)
        return cls._engine

    @classmethod
    def session(cls):
        """Devuelve un Session factory (Singleton)."""
        if cls._SessionLocal is None:
            cls._SessionLocal = sessionmaker(bind=cls.engine(), autoflush=False, autocommit=False)
        return cls._SessionLocal
