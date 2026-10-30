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
        "message": "Estrutura inicial da aplicação disponível.",
    }


def test_data_sqlite_e_apresentada_no_horario_de_brasilia(app):
    formatter = app.jinja_env.filters["datetime_br"]

    # CURRENT_TIMESTAMP do SQLite é UTC; a tela deve apresentar UTC-03.
    assert formatter("2026-10-30 17:44:55") == "30/10/2026 às 14:44:55"
