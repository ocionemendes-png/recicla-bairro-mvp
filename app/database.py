"""Conexão e inicialização do banco SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    """Retorna uma conexão SQLite associada ao contexto da requisição."""
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection

    return g.db


def close_db(error: BaseException | None = None) -> None:
    """Fecha a conexão SQLite ao final do contexto da aplicação."""
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db() -> None:
    """Executa o esquema SQL inicial do projeto."""
    schema_path = Path(__file__).with_name("schema.sql")
    schema = schema_path.read_text(encoding="utf-8")
    get_db().executescript(schema)
