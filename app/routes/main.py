"""Rotas públicas iniciais do projeto."""

from flask import Blueprint, jsonify, render_template

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    """Apresenta a página inicial e o estado atual do MVP."""
    return render_template("index.html")


@main_bp.get("/health")
def health():
    """Endpoint simples para verificar se a aplicação está ativa."""
    return jsonify(
        {
            "application": "Recicla Bairro",
            "status": "ok",
            "message": "Estrutura inicial da aplicação disponível.",
        }
    ), 200
