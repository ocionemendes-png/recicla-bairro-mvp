"""Fixtures compartilhadas dos testes."""

import pytest

from app import create_app
from app.database import init_db


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test_recicla.sqlite3"
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "DATABASE": str(database_path),
        }
    )
    with application.app_context():
        init_db()
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()
