"""Testes de cadastro e persistência de solicitações."""

import re

from app.database import get_db, init_db


def token_csrf(client) -> str:
    response = client.get("/solicitacoes/nova")
    assert response.status_code == 200
    match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
    assert match, "Token CSRF não encontrado no formulário"
    return match.group(1).decode("utf-8")


def dados_validos(csrf_token: str) -> dict:
    return {
        "csrf_token": csrf_token,
        "nome": "Carlos Exemplo",
        "contato": "carlos.exemplo@teste.invalid",
        "endereco": "Rua das Acácias, 100",
        "tipo_material_id": "1",
    }


def test_formulario_de_cadastro_carrega_opcoes_de_material(client):
    response = client.get("/solicitacoes/nova")

    assert response.status_code == 200
    assert b"Nova solicita\xc3\xa7\xc3\xa3o" in response.data
    assert b"Papel" in response.data
    assert b"Pl\xc3\xa1stico" in response.data


def test_cadastro_valido_persiste_e_mostra_confirmacao(app, client):
    csrf = token_csrf(client)
    response = client.post(
        "/solicitacoes/nova",
        data=dados_validos(csrf),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Solicita\xc3\xa7\xc3\xa3o cadastrada com sucesso" in response.data
    assert b"SOL-0001" in response.data
    assert b"Carlos Exemplo" in response.data
    assert b"Pendente" in response.data

    with app.app_context():
        row = get_db().execute(
            """
            SELECT s.nome, s.contato, sc.endereco, sc.status, tm.nome AS material
            FROM SolicitacaoColeta sc
            JOIN Solicitante s ON s.id_solicitante = sc.id_solicitante
            JOIN TipoMaterial tm ON tm.id_tipo_material = sc.id_tipo_material
            WHERE sc.id_solicitacao = 1
            """
        ).fetchone()

    assert row["nome"] == "Carlos Exemplo"
    assert row["contato"] == "carlos.exemplo@teste.invalid"
    assert row["endereco"] == "Rua das Acácias, 100"
    assert row["status"] == "pendente"
    assert row["material"] == "Papel"


def test_cadastro_rejeita_campos_obrigatorios_vazios(client):
    csrf = token_csrf(client)
    data = dados_validos(csrf)
    data["nome"] = ""
    data["endereco"] = ""

    response = client.post("/solicitacoes/nova", data=data)

    assert response.status_code == 422
    assert "Informe o nome do solicitante." in response.get_data(as_text=True)
    assert "Informe o endereço da coleta." in response.get_data(as_text=True)


def test_cadastro_rejeita_contato_invalido(client):
    csrf = token_csrf(client)
    data = dados_validos(csrf)
    data["contato"] = "contato-invalido"

    response = client.post("/solicitacoes/nova", data=data)

    assert response.status_code == 422
    assert "Informe um e-mail válido ou telefone" in response.get_data(as_text=True)


def test_cadastro_rejeita_tipo_de_material_inexistente(client):
    csrf = token_csrf(client)
    data = dados_validos(csrf)
    data["tipo_material_id"] = "9999"

    response = client.post("/solicitacoes/nova", data=data)

    assert response.status_code == 422
    assert "Selecione um tipo de material disponível." in response.get_data(as_text=True)


def test_cadastro_rejeita_post_sem_token_csrf(client):
    response = client.post("/solicitacoes/nova", data=dados_validos(""))
    assert response.status_code == 400


def test_cadastro_nao_cria_registro_quando_dados_sao_invalidos(app, client):
    csrf = token_csrf(client)
    data = dados_validos(csrf)
    data["nome"] = " "
    client.post("/solicitacoes/nova", data=data)

    with app.app_context():
        init_db()
        count = get_db().execute(
            "SELECT COUNT(*) AS total FROM SolicitacaoColeta"
        ).fetchone()["total"]

    assert count == 0
