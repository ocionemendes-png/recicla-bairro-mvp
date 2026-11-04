"""Operações de persistência relacionadas às solicitações de coleta."""

from __future__ import annotations

from datetime import datetime

from app.database import get_db


def listar_tipos_materiais() -> list:
    """Retorna os tipos de materiais ativos para uso no formulário."""
    return get_db().execute(
        """
        SELECT id_tipo_material, nome
        FROM TipoMaterial
        WHERE ativo = 1
        ORDER BY nome COLLATE NOCASE
        """
    ).fetchall()


def tipo_material_ativo(tipo_material_id: int) -> bool:
    """Confirma que o tipo informado existe e está ativo."""
    row = get_db().execute(
        """
        SELECT 1
        FROM TipoMaterial
        WHERE id_tipo_material = ? AND ativo = 1
        """,
        (tipo_material_id,),
    ).fetchone()
    return row is not None


def criar_solicitacao(
    *, nome: str, contato: str, endereco: str, tipo_material_id: int
) -> int:
    """Grava solicitante e solicitação em uma única transação.

    Retorna o identificador da solicitação criada. Se qualquer inserção falhar,
    a transação poderá ser revertida pelo chamador.
    """
    db = get_db()
    cursor_solicitante = db.execute(
        """
        INSERT INTO Solicitante (nome, contato)
        VALUES (?, ?)
        """,
        (nome, contato),
    )
    solicitante_id = cursor_solicitante.lastrowid

    cursor_solicitacao = db.execute(
        """
        INSERT INTO SolicitacaoColeta
            (id_solicitante, id_tipo_material, endereco, status)
        VALUES (?, ?, ?, 'pendente')
        """,
        (solicitante_id, tipo_material_id, endereco),
    )
    db.commit()
    return int(cursor_solicitacao.lastrowid)


def buscar_solicitacao(solicitacao_id: int):
    """Busca os dados da solicitação e do solicitante associado."""
    return get_db().execute(
        """
        SELECT
            sc.id_solicitacao,
            sc.data_solicitacao,
            sc.status,
            sc.endereco,
            s.nome AS nome_solicitante,
            s.contato,
            tm.nome AS tipo_material
        FROM SolicitacaoColeta AS sc
        INNER JOIN Solicitante AS s
            ON s.id_solicitante = sc.id_solicitante
        INNER JOIN TipoMaterial AS tm
            ON tm.id_tipo_material = sc.id_tipo_material
        WHERE sc.id_solicitacao = ?
        """,
        (solicitacao_id,),
    ).fetchone()



def listar_solicitacoes(status: str | None = None) -> list:
    """Lista solicitações com dados do solicitante e do tipo de material.

    O filtro de status é parametrizado para evitar interpolação de valores
    recebidos pela URL diretamente no SQL.
    """
    db = get_db()
    consulta = """
        SELECT
            sc.id_solicitacao,
            sc.data_solicitacao,
            sc.status,
            sc.endereco,
            s.nome AS nome_solicitante,
            tm.nome AS tipo_material
        FROM SolicitacaoColeta AS sc
        INNER JOIN Solicitante AS s
            ON s.id_solicitante = sc.id_solicitante
        INNER JOIN TipoMaterial AS tm
            ON tm.id_tipo_material = sc.id_tipo_material
    """
    parametros: tuple = ()
    if status is not None:
        consulta += " WHERE sc.status = ?"
        parametros = (status,)
    consulta += " ORDER BY sc.data_solicitacao DESC, sc.id_solicitacao DESC"
    return db.execute(consulta, parametros).fetchall()


def contar_solicitacoes_por_status() -> dict[str, int]:
    """Retorna a quantidade de pedidos em cada situação permitida."""
    totais = {
        "pendente": 0,
        "em andamento": 0,
        "concluída": 0,
    }
    rows = get_db().execute(
        """
        SELECT status, COUNT(*) AS quantidade
        FROM SolicitacaoColeta
        GROUP BY status
        """
    ).fetchall()
    for row in rows:
        if row["status"] in totais:
            totais[row["status"]] = int(row["quantidade"])
    totais["total"] = sum(totais.values())
    return totais
