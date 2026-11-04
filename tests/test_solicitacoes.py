"""Testes de cadastro e persistência de solicitações."""

import re
import sqlite3

import pytest

from app.database import get_db, init_db
from app.models.solicitacao import criar_solicitacao


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



def cadastrar_pedido_teste(client, nome: str, material_id: str = "1") -> None:
    """Cadastra um pedido de teste usando o formulário e seu token CSRF."""
    csrf = token_csrf(client)
    data = dados_validos(csrf)
    data["nome"] = nome
    data["tipo_material_id"] = material_id
    response = client.post("/solicitacoes/nova", data=data)
    assert response.status_code == 303


def test_lista_de_solicitacoes_exibe_pedido_persistido(client):
    cadastrar_pedido_teste(client, "Maria Exemplo")

    response = client.get("/solicitacoes")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Solicitações de coleta" in html
    assert "SOL-0001" in html
    assert "Maria Exemplo" in html
    assert "Pendente" in html
    assert "Ver detalhes" in html


def test_lista_filtra_pelo_status_selecionado(app, client):
    cadastrar_pedido_teste(client, "Maria Exemplo")
    cadastrar_pedido_teste(client, "João Exemplo", material_id="2")

    with app.app_context():
        db = get_db()
        db.execute(
            "UPDATE SolicitacaoColeta SET status = ? WHERE id_solicitacao = ?",
            ("concluída", 2),
        )
        db.commit()

    response = client.get("/solicitacoes?status=conclu%C3%ADda")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "SOL-0002" in html
    assert "João Exemplo" in html
    assert "SOL-0001" not in html


def test_lista_rejeita_filtro_de_status_desconhecido(client):
    response = client.get("/solicitacoes?status=cancelada")

    assert response.status_code == 400


def test_detalhes_da_solicitacao_podem_ser_abertos_pela_lista(client):
    cadastrar_pedido_teste(client, "Carlos Exemplo")

    response = client.get("/solicitacoes/1")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Detalhes da solicitação" in html
    assert "Carlos Exemplo" in html
    assert "Pendente" in html
    assert "Voltar às solicitações" in html


def test_detalhes_exibem_formulario_de_atualizacao_com_csrf(client):
    cadastrar_pedido_teste(client, "Ana Exemplo")
    response = client.get("/solicitacoes/1")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Atualizar status da coleta" in html
    assert 'name="csrf_token"' in html
    assert "Em andamento" in html


def test_atualizacao_para_em_andamento_persiste_e_reflete_na_lista(app, client):
    cadastrar_pedido_teste(client, "Ana Exemplo")
    csrf = token_csrf(client)

    response = client.post(
        "/solicitacoes/1/status",
        data={"csrf_token": csrf, "status": "em andamento"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Status atualizado para Em andamento com sucesso." in response.get_data(as_text=True)
    assert "Em andamento" in response.get_data(as_text=True)

    with app.app_context():
        row = get_db().execute(
            "SELECT status FROM SolicitacaoColeta WHERE id_solicitacao = 1"
        ).fetchone()
    assert row["status"] == "em andamento"

    lista = client.get("/solicitacoes?status=em%20andamento")
    assert lista.status_code == 200
    assert "SOL-0001" in lista.get_data(as_text=True)


def test_atualizacao_para_concluida_persiste_e_remove_opcoes(app, client):
    cadastrar_pedido_teste(client, "Ana Exemplo")
    csrf = token_csrf(client)

    response = client.post(
        "/solicitacoes/1/status",
        data={"csrf_token": csrf, "status": "concluída"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Status atualizado para Concluída com sucesso." in html
    assert "Esta solicitação já foi concluída" in html
    assert 'id="novo-status"' not in html

    with app.app_context():
        row = get_db().execute(
            "SELECT status FROM SolicitacaoColeta WHERE id_solicitacao = 1"
        ).fetchone()
    assert row["status"] == "concluída"


def test_atualizacao_rejeita_status_desconhecido_sem_alterar_banco(app, client):
    cadastrar_pedido_teste(client, "Ana Exemplo")
    csrf = token_csrf(client)

    response = client.post(
        "/solicitacoes/1/status",
        data={"csrf_token": csrf, "status": "cancelada"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "A mudança de status selecionada não é permitida" in response.get_data(as_text=True)
    with app.app_context():
        row = get_db().execute(
            "SELECT status FROM SolicitacaoColeta WHERE id_solicitacao = 1"
        ).fetchone()
    assert row["status"] == "pendente"


def test_atualizacao_exige_token_csrf(client):
    cadastrar_pedido_teste(client, "Ana Exemplo")
    response = client.post(
        "/solicitacoes/1/status",
        data={"status": "em andamento"},
    )
    assert response.status_code == 400


def test_atualizacao_rejeita_retrocesso_de_status(app, client):
    cadastrar_pedido_teste(client, "Ana Exemplo")
    csrf = token_csrf(client)
    client.post(
        "/solicitacoes/1/status",
        data={"csrf_token": csrf, "status": "concluída"},
    )

    response = client.post(
        "/solicitacoes/1/status",
        data={"csrf_token": csrf, "status": "pendente"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "A mudança de status selecionada não é permitida" in response.get_data(as_text=True)
    with app.app_context():
        row = get_db().execute(
            "SELECT status FROM SolicitacaoColeta WHERE id_solicitacao = 1"
        ).fetchone()
    assert row["status"] == "concluída"


def test_atualizacao_de_solicitacao_inexistente_retorna_404(client):
    # Obtém um token válido antes de consultar o recurso inexistente.
    csrf = token_csrf(client)
    response = client.post(
        "/solicitacoes/999/status",
        data={"csrf_token": csrf, "status": "em andamento"},
    )
    assert response.status_code == 404



def test_cadastro_reverte_solicitante_quando_insercao_da_solicitacao_falha(app):
    """A falha na segunda inserção não pode deixar um solicitante órfão."""
    with app.app_context():
        with pytest.raises(sqlite3.IntegrityError):
            criar_solicitacao(
                nome="Teste de rollback",
                contato="rollback@teste.invalid",
                endereco="Rua de Teste, 10",
                tipo_material_id=9999,
            )

        total_solicitantes = get_db().execute(
            "SELECT COUNT(*) AS total FROM Solicitante"
        ).fetchone()["total"]
        total_solicitacoes = get_db().execute(
            "SELECT COUNT(*) AS total FROM SolicitacaoColeta"
        ).fetchone()["total"]

    assert total_solicitantes == 0
    assert total_solicitacoes == 0
