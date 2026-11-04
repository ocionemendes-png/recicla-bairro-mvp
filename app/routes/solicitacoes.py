"""Rotas e validações do cadastro de solicitações."""

from __future__ import annotations

import hmac
import re
import secrets
import sqlite3

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app.models.solicitacao import (
    buscar_solicitacao,
    atualizar_status_solicitacao,
    TRANSICOES_STATUS,
    contar_solicitacoes_por_status,
    criar_solicitacao,
    listar_solicitacoes,
    listar_tipos_materiais,
    tipo_material_ativo,
    STATUS_PERMITIDOS,
)

solicitacoes_bp = Blueprint("solicitacoes", __name__, url_prefix="/solicitacoes")

MAX_NOME = 120
MAX_CONTATO = 120
MAX_ENDERECO = 250
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def contato_valido(contato: str) -> bool:
    """Aceita um e-mail simples ou telefone com ao menos oito dígitos."""
    if EMAIL_PATTERN.fullmatch(contato):
        return True
    digits = re.sub(r"\D", "", contato)
    return len(digits) >= 8 and bool(re.fullmatch(r"[0-9+().\-\s]+", contato))


def obter_token_csrf() -> str:
    """Gera e mantém token CSRF na sessão do formulário."""
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def validar_token_csrf(token_recebido: str | None) -> bool:
    token_sessao = session.get("csrf_token", "")
    return bool(token_sessao and token_recebido and hmac.compare_digest(token_sessao, token_recebido))


def validar_formulario(form) -> tuple[dict, dict, int | None]:
    """Normaliza e valida campos; retorna dados, erros e tipo válido."""
    dados = {
        "nome": form.get("nome", "").strip(),
        "contato": form.get("contato", "").strip(),
        "endereco": form.get("endereco", "").strip(),
        "tipo_material_id": form.get("tipo_material_id", "").strip(),
    }
    erros: dict[str, str] = {}

    if not dados["nome"]:
        erros["nome"] = "Informe o nome do solicitante."
    elif len(dados["nome"]) > MAX_NOME:
        erros["nome"] = f"O nome deve ter no máximo {MAX_NOME} caracteres."

    if not dados["contato"]:
        erros["contato"] = "Informe um telefone ou e-mail para contato."
    elif len(dados["contato"]) > MAX_CONTATO:
        erros["contato"] = f"O contato deve ter no máximo {MAX_CONTATO} caracteres."
    elif not contato_valido(dados["contato"]):
        erros["contato"] = "Informe um e-mail válido ou telefone com pelo menos 8 dígitos."

    if not dados["endereco"]:
        erros["endereco"] = "Informe o endereço da coleta."
    elif len(dados["endereco"]) > MAX_ENDERECO:
        erros["endereco"] = f"O endereço deve ter no máximo {MAX_ENDERECO} caracteres."

    tipo_material_id = None
    if not dados["tipo_material_id"]:
        erros["tipo_material_id"] = "Selecione o tipo de material."
    else:
        try:
            tipo_material_id = int(dados["tipo_material_id"])
            if tipo_material_id <= 0 or not tipo_material_ativo(tipo_material_id):
                erros["tipo_material_id"] = "Selecione um tipo de material disponível."
                tipo_material_id = None
        except ValueError:
            erros["tipo_material_id"] = "Selecione um tipo de material válido."

    return dados, erros, tipo_material_id


@solicitacoes_bp.get("/", strict_slashes=False)
def listar():
    """Apresenta os pedidos registrados e permite filtrar por situação."""
    status_selecionado = request.args.get("status", "todos").strip().lower()
    if status_selecionado not in ("todos", *STATUS_PERMITIDOS):
        abort(400, description="O filtro de status informado não é válido.")

    filtro = None if status_selecionado == "todos" else status_selecionado
    solicitacoes = listar_solicitacoes(status=filtro)
    totais = contar_solicitacoes_por_status()

    return render_template(
        "solicitacoes/listar.html",
        solicitacoes=solicitacoes,
        status_selecionado=status_selecionado,
        totais=totais,
    )


@solicitacoes_bp.route("/nova", methods=["GET", "POST"])
def nova():
    """Exibe e processa o formulário de cadastro de uma solicitação."""
    tipos_materiais = listar_tipos_materiais()

    if request.method == "GET":
        return render_template(
            "solicitacoes/nova.html",
            tipos_materiais=tipos_materiais,
            dados={},
            erros={},
            csrf_token=obter_token_csrf(),
        )

    if not validar_token_csrf(request.form.get("csrf_token")):
        abort(400, description="O formulário expirou. Atualize a página e tente novamente.")

    dados, erros, tipo_material_id = validar_formulario(request.form)
    if erros:
        return render_template(
            "solicitacoes/nova.html",
            tipos_materiais=tipos_materiais,
            dados=dados,
            erros=erros,
            csrf_token=obter_token_csrf(),
        ), 422

    try:
        solicitacao_id = criar_solicitacao(
            nome=dados["nome"],
            contato=dados["contato"],
            endereco=dados["endereco"],
            tipo_material_id=tipo_material_id,
        )
    except sqlite3.DatabaseError:
        # Não expõe detalhes internos do banco ao usuário.
        return render_template(
            "solicitacoes/nova.html",
            tipos_materiais=tipos_materiais,
            dados=dados,
            erros={"geral": "Não foi possível salvar a solicitação. Confira os dados e tente novamente."},
            csrf_token=obter_token_csrf(),
        ), 500

    session.pop("csrf_token", None)
    flash("Solicitação cadastrada com sucesso! O status inicial é Pendente.", "success")
    return redirect(url_for("solicitacoes.detalhes", solicitacao_id=solicitacao_id), code=303)


@solicitacoes_bp.get("/<int:solicitacao_id>")
def detalhes(solicitacao_id: int):
    """Exibe a confirmação e os dados persistidos da solicitação criada."""
    solicitacao = buscar_solicitacao(solicitacao_id)
    if solicitacao is None:
        abort(404)
    status_opcoes = sorted(
        TRANSICOES_STATUS.get(solicitacao["status"], set()),
        key=lambda valor: (valor != "em andamento", valor),
    )
    return render_template(
        "solicitacoes/detalhes.html",
        solicitacao=solicitacao,
        status_opcoes=status_opcoes,
        csrf_token=obter_token_csrf(),
    )


@solicitacoes_bp.post("/<int:solicitacao_id>/status")
def atualizar_status(solicitacao_id: int):
    """Valida e persiste uma mudança de status da solicitação."""
    if not validar_token_csrf(request.form.get("csrf_token")):
        abort(400, description="O formulário expirou. Atualize a página e tente novamente.")

    solicitacao = buscar_solicitacao(solicitacao_id)
    if solicitacao is None:
        abort(404)

    novo_status = request.form.get("status", "").strip().lower()
    try:
        atualizada = atualizar_status_solicitacao(solicitacao_id, novo_status)
    except ValueError:
        flash("A mudança de status selecionada não é permitida. Confira a etapa atual do pedido.", "error")
        return redirect(url_for("solicitacoes.detalhes", solicitacao_id=solicitacao_id), code=303)

    if not atualizada:
        abort(404)

    rotulos = {
        "pendente": "Pendente",
        "em andamento": "Em andamento",
        "concluída": "Concluída",
    }
    flash(f"Status atualizado para {rotulos[novo_status]} com sucesso.", "success")
    return redirect(url_for("solicitacoes.detalhes", solicitacao_id=solicitacao_id), code=303)
