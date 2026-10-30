-- Esquema inicial do Recicla Bairro.
-- As tabelas representam o modelo planejado na Experiência Prática II.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Solicitante (
    id_solicitante INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    contato TEXT NOT NULL CHECK (length(trim(contato)) > 0),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS TipoMaterial (
    id_tipo_material INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE CHECK (length(trim(nome)) > 0),
    descricao TEXT,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS UsuarioResponsavel (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    email TEXT NOT NULL UNIQUE CHECK (length(trim(email)) > 0),
    senha_hash TEXT NOT NULL,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS SolicitacaoColeta (
    id_solicitacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_solicitante INTEGER NOT NULL,
    id_tipo_material INTEGER NOT NULL,
    id_usuario_responsavel INTEGER,
    endereco TEXT NOT NULL CHECK (length(trim(endereco)) > 0),
    data_solicitacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'pendente'
        CHECK (status IN ('pendente', 'em andamento', 'concluída')),
    FOREIGN KEY (id_solicitante)
        REFERENCES Solicitante (id_solicitante),
    FOREIGN KEY (id_tipo_material)
        REFERENCES TipoMaterial (id_tipo_material),
    FOREIGN KEY (id_usuario_responsavel)
        REFERENCES UsuarioResponsavel (id_usuario)
);

CREATE INDEX IF NOT EXISTS idx_solicitacao_status
    ON SolicitacaoColeta (status);

CREATE INDEX IF NOT EXISTS idx_solicitacao_data
    ON SolicitacaoColeta (data_solicitacao);
