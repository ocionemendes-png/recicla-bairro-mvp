"""Fábrica da aplicação Flask e registro das rotas."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask

from app.database import close_db


def create_app(test_config: dict | None = None) -> Flask:
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get(
            "RECICLA_SECRET_KEY",
            "chave-local-de-desenvolvimento-nao-usar-em-producao",
        ),
        DATABASE=os.environ.get(
            "RECICLA_DATABASE",
            str(Path(app.instance_path) / "recicla.sqlite3"),
        ),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from app.routes.main import main_bp

    app.register_blueprint(main_bp)
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command() -> None:
        """Cria as tabelas iniciais do banco SQLite."""
        from app.database import init_db

        init_db()
        print("Banco SQLite inicializado com sucesso.")

    return app
