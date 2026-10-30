"""Testes do esquema inicial do SQLite."""

import sqlite3

import pytest

from app.database import get_db, init_db


def test_init_db_creates_expected_tables(app):
    with app.app_context():
        init_db()
        rows = get_db().execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()

    table_names = {row["name"] for row in rows}
    assert {
        "Solicitante",
        "TipoMaterial",
        "UsuarioResponsavel",
        "SolicitacaoColeta",
    }.issubset(table_names)


def test_solicitacao_rejects_invalid_status(app):
    with app.app_context():
        init_db()
        db = get_db()

        solicitante = db.execute(
            "INSERT INTO Solicitante (nome, contato) VALUES (?, ?)",
            ("Pessoa de Teste", "teste@example.invalid"),
        )
        tipo = db.execute(
            "SELECT id_tipo_material FROM TipoMaterial WHERE nome = ?",
            ("Papel",),
        ).fetchone()
        assert tipo is not None

        with pytest.raises(sqlite3.IntegrityError):
            db.execute(
                """
                INSERT INTO SolicitacaoColeta
                    (id_solicitante, id_tipo_material, endereco, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    solicitante.lastrowid,
                    tipo["id_tipo_material"],
                    "Rua de Teste, 100",
                    "status inválido",
                ),
            )
