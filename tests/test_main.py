"""Testes básicos das rotas iniciais."""


def test_home_page_returns_success(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Bem-vindo ao Recicla Bairro" in response.data
    assert b"MVP em desenvolvimento" in response.data


def test_health_endpoint_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "application": "Recicla Bairro",
        "status": "ok",
        "message": "Aplicação e banco de dados disponíveis.",
    }


def test_health_endpoint_fails_when_database_schema_is_missing(app, client):
    from app.database import get_db

    with app.app_context():
        get_db().execute("DROP TABLE SolicitacaoColeta")
        get_db().commit()

    response = client.get("/health")

    assert response.status_code == 503
    assert response.get_json()["status"] == "error"
