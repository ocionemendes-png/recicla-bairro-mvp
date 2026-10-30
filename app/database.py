"""Conexão e inicialização do banco SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import current_app, g

MATERIAIS_INICIAIS = (
    ("Papel", "Papel e papelão limpos e secos."),
    ("Plástico", "Embalagens e outros materiais plásticos recicláveis."),
    ("Vidro", "Garrafas e recipientes de vidro."),
    ("Metal", "Latas e outros materiais metálicos."),
)


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
        if error is not None:
            connection.rollback()
        connection.close()


def init_db() -> None:
    """Cria as tabelas e cadastra os tipos de materiais iniciais."""
    schema_path = Path(__file__).with_name("schema.sql")
    schema = schema_path.read_text(encoding="utf-8")
    db = get_db()
    db.executescript(schema)
    db.executemany(
        "INSERT OR IGNORE INTO TipoMaterial (nome, descricao) VALUES (?, ?)",
        MATERIAIS_INICIAIS,
    )
    db.commit()
