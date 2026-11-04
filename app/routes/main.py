"""Rotas públicas iniciais do projeto."""

import sqlite3

from flask import Blueprint, jsonify, render_template

from app.database import get_db

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    """Apresenta a página inicial do MVP."""
    return render_template("index.html")


@main_bp.get("/health")
def health():
    """Verifica se a aplicação e a tabela principal do SQLite estão disponíveis."""
    try:
        tabela = get_db().execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table' AND name = 'SolicitacaoColeta'
            """
        ).fetchone()
    except sqlite3.Error:
        return jsonify(
            {
                "application": "Recicla Bairro",
                "status": "error",
                "message": "Banco de dados indisponível.",
            }
        ), 503

    if tabela is None:
        return jsonify(
            {
                "application": "Recicla Bairro",
                "status": "error",
                "message": "Banco de dados ainda não inicializado.",
            }
        ), 503

    return jsonify(
        {
            "application": "Recicla Bairro",
            "status": "ok",
            "message": "Aplicação e banco de dados disponíveis.",
        }
    ), 200
