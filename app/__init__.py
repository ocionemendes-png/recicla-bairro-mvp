"""Fábrica da aplicação Flask e registro das rotas."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import Flask

from app.database import close_db


def format_datetime_br(value: str | datetime | None) -> str:
    """Converte timestamps UTC do SQLite para o horário de Brasília (UTC-03).

    O SQLite CURRENT_TIMESTAMP armazena data/hora em UTC sem informação
    explícita de fuso. A conversão ocorre apenas na apresentação; o valor
    original permanece inalterado no banco de dados.
    """
    if value is None or value == "":
        return ""

    try:
        parsed = datetime.fromisoformat(value) if isinstance(value, str) else value
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        brasilia_timezone = timezone(timedelta(hours=-3))
        local_time = parsed.astimezone(brasilia_timezone)
        return local_time.strftime("%d/%m/%Y às %H:%M:%S")
    except (TypeError, ValueError):
        return str(value)


def create_app(test_config: dict | None = None) -> Flask:
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)
    app.add_template_filter(format_datetime_br, "datetime_br")

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
    from app.routes.solicitacoes import solicitacoes_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(solicitacoes_bp)
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command() -> None:
        """Cria as tabelas iniciais do banco SQLite."""
        from app.database import init_db

        init_db()
        print("Banco SQLite inicializado com sucesso.")

    return app
