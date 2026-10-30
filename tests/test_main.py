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
