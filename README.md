# Recicla Bairro MVP

Projeto acadêmico de software para apoiar o cadastro, a consulta e o acompanhamento de solicitações de coleta seletiva.

> **Estado atual:** cadastro e consulta de solicitações implementados, com filtro por status e visualização dos detalhes. A atualização do status será desenvolvida na próxima entrega. Os dados de demonstração são fictícios.

## Tecnologias planejadas

- Python 3.13
- Flask 3.1.3
- CSS responsivo próprio (a adoção de Bootstrap poderá ser ampliada nas próximas entregas)
- SQLite
- pytest para testes automatizados

## Requisitos

- Python 3.11 ou superior.
- Git.
- Acesso à internet para instalar as dependências.

## Preparar o ambiente no Windows (PowerShell)

Na pasta do repositório, execute:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Se o comando `py -3.13` não estiver disponível, instale Python 3.13 ou ajuste o comando para uma versão compatível instalada no computador.

## Inicializar o banco de dados

Com o ambiente virtual ativado:

```powershell
flask --app run init-db
```

O banco SQLite será criado em `instance/recicla.sqlite3`. Esse arquivo é local e está excluído do Git pelo `.gitignore`.

## Executar a aplicação

```powershell
python run.py
```

Abra no navegador:

- Página inicial: http://127.0.0.1:5000/
- Consulta de solicitações: http://127.0.0.1:5000/solicitacoes
- Cadastro de solicitação: http://127.0.0.1:5000/solicitacoes/nova
- Verificação de funcionamento: http://127.0.0.1:5000/health

O servidor embutido do Flask é destinado somente ao desenvolvimento local.

## Executar os testes

Em outro terminal, ou após parar o servidor com `Ctrl+C`:

```powershell
python -m pytest -q
```

Os testes usam um banco temporário e não alteram o banco local da aplicação.

## Estrutura inicial

```text
recicla-bairro-mvp/
├── run.py
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── schema.sql
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── solicitacoes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── solicitacao.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── solicitacoes/
│   │       ├── nova.html
│   │       └── detalhes.html
│   └── static/
│       └── css/
│           └── style.css
├── tests/
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_database.py
│   └── test_solicitacoes.py
├── instance/
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── .gitignore
```

## Modelo de dados inicial

O esquema SQLite contempla as quatro entidades definidas no planejamento:

- `Solicitante`
- `TipoMaterial`
- `UsuarioResponsavel`
- `SolicitacaoColeta`

As restrições do banco incluem campos obrigatórios, identificadores, chaves estrangeiras e os status permitidos: `pendente`, `em andamento` e `concluída`.

## Funcionalidade implementada nesta versão

O cadastro de solicitações está disponível em `/solicitacoes/nova` e inclui:

- Campos obrigatórios para nome, contato, endereço e tipo de material.
- Validação no servidor, com limites de tamanho e verificação de e-mail ou telefone.
- Verificação de que o tipo de material existe e está ativo.
- Token CSRF por sessão para proteger o envio do formulário.
- Gravação do solicitante e do pedido em uma transação SQLite.
- Status inicial automático `pendente`.
- Página de confirmação com identificador `SOL-0001` (numeração conforme o ID gerado).
- Tipos iniciais de material: papel, plástico, vidro e metal.

O cadastro representa um registro persistido no banco local. A consulta geral está disponível em `/solicitacoes`, com filtro por status e acesso à página de detalhes de cada pedido. A atualização de status será desenvolvida em etapa posterior.

## Funcionalidade implementada nesta versão: consulta

A consulta está disponível em `/solicitacoes` e inclui:

- Listagem dos pedidos persistidos no SQLite, com identificação, solicitante, material, endereço, status e data.
- Resumo das quantidades por status.
- Filtro por todos, pendente, em andamento ou concluída.
- Acesso à página de detalhes de cada solicitação.
- Tratamento de filtro inválido e estado vazio da listagem.

## Próximas entregas planejadas

1. Implementar atualização do status das solicitações.
2. Implementar autenticação e controles de acesso.
3. Ampliar testes unitários e de integração.
4. Configurar integração contínua com GitHub Actions.
5. Evoluir a interface e avaliar o fluxo com participantes externos, mediante concordância.

## Observação acadêmica

O Coletivo Recicla Bairro é um cenário fictício utilizado para planejamento acadêmico. A aplicação deverá utilizar dados demonstrativos até que exista validação autorizada com participantes reais.

## Datas e horário

O SQLite mantém `CURRENT_TIMESTAMP` em UTC. Na apresentação, os horários são
convertidos para o fuso de Brasília (UTC-03), sem alterar o valor armazenado.
