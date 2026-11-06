# Recicla Bairro MVP

Aplicação acadêmica para cadastrar, consultar e acompanhar solicitações de coleta seletiva. O Coletivo Recicla Bairro é um cenário fictício de planejamento; os registros de demonstração não representam pedidos reais.

## Estado atual

O MVP implementa três fluxos principais:

1. **Cadastro:** registro de solicitante, contato, endereço e tipo de material, com validação no servidor, proteção CSRF e gravação transacional no SQLite.
2. **Consulta:** listagem dos pedidos, indicadores por status, filtro por situação e visualização dos detalhes.
3. **Atualização de status:** transições controladas de Pendente para Em andamento ou Concluída; Em andamento pode avançar para Concluída. Concluída é um estado final.

A interface inclui rótulos e foco visual para navegação por teclado. Não há autenticação de usuários nesta versão; por isso, o MVP deve permanecer demonstrativo e não receber dados pessoais ou solicitações operacionais reais.

## Tecnologias

- Python 3.13
- Flask 3.1.3
- SQLite
- HTML5 e CSS próprio
- Waitress como servidor WSGI de produção
- pytest e pytest-cov para testes e cobertura
- GitHub Actions para integração contínua

## Executar localmente no Windows

Na pasta do repositório, abra o PowerShell e execute:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Inicialize o banco local:

```powershell
flask --app run init-db
```

Execute a aplicação para desenvolvimento:

```powershell
python run.py
```

Acesse:

- Página inicial: http://127.0.0.1:5000/
- Consulta: http://127.0.0.1:5000/solicitacoes
- Cadastro: http://127.0.0.1:5000/solicitacoes/nova
- Saúde da aplicação e do banco: http://127.0.0.1:5000/health

O servidor de desenvolvimento do Flask é destinado apenas ao uso local.

## Testes e cobertura

Com o ambiente virtual ativado:

```powershell
python -m pytest -q
python -m pytest --cov=app --cov-report=term-missing -q
```

Os testes usam banco temporário e não alteram o banco local da aplicação. A cobertura deve ser medida novamente após cada alteração; o percentual pode variar conforme o código e os testes presentes.

## Estrutura do projeto

```text
recicla-bairro-mvp/
├── run.py
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── schema.sql
│   ├── routes/
│   │   ├── main.py
│   │   └── solicitacoes.py
│   ├── models/
│   │   └── solicitacao.py
│   ├── templates/
│   └── static/css/
├── tests/
├── instance/
├── requirements.txt
├── requirements-dev.txt
└── .python-version
```

O banco local fica em `instance/recicla.sqlite3` e é excluído do Git pelo `.gitignore`.

## Publicação no Railway

A configuração abaixo prepara a aplicação para ser publicada no Railway. Não coloque chaves ou segredos no repositório.

1. Conecte o repositório público `ocionemendes-png/recicla-bairro-mvp` a um serviço Railway.
2. Crie um Volume para o serviço e defina o ponto de montagem como `/data`.
3. Configure as variáveis do serviço:

   - `RECICLA_DATABASE=/data/recicla.sqlite3`
   - `RECICLA_SECRET_KEY`: uma chave aleatória forte, criada para o ambiente de produção e mantida somente nas variáveis do Railway.

4. Configure o Start Command do serviço:

```bash
flask --app run init-db && waitress-serve --listen=0.0.0.0:$PORT run:app
```

5. Configure o Healthcheck Path como `/health` e gere um domínio público para o serviço.
6. Mantenha apenas uma réplica enquanto o banco for SQLite. Para uso real por múltiplos operadores, implemente autenticação e avalie um banco gerenciado, como PostgreSQL.

O comando de inicialização cria as tabelas se ainda não existirem. O volume em `/data` mantém o arquivo SQLite entre reinicializações e novos deploys. Confirme nos logs que a inicialização foi concluída e que o serviço está ouvindo na porta fornecida pelo Railway.

## Acessibilidade e relação com o ODS 12

A interface inclui rótulos associados aos campos dos formulários, mensagens de orientação e erro vinculadas aos respectivos campos, indicação visual de foco para navegação por teclado e layout responsivo para diferentes tamanhos de tela. Esses recursos ajudam a tornar o cadastro e o acompanhamento das solicitações mais claros e acessíveis em diferentes dispositivos e formas de navegação. No contexto do Recicla Bairro, essa facilidade de uso pode favorecer a participação nas solicitações de coleta seletiva e contribuir indiretamente para o **ODS 12 – Consumo e Produção Responsáveis, especialmente a Meta 12.5**, relacionada à prevenção, redução, reciclagem e reutilização de resíduos. Essa relação representa uma contribuição potencial da ferramenta: não comprova aumento da reciclagem ou redução de resíduos, resultados que dependeriam da adoção do sistema e de coletas reais. Como o projeto utiliza um cenário comunitário fictício, essa contribuição ainda não foi validada com usuários ou organização reais.

## Monitoramento

O endpoint `/health` verifica a existência da tabela principal do SQLite e retorna HTTP 200 quando a aplicação e o banco estão disponíveis; em caso de falha ou esquema não inicializado, retorna HTTP 503. Esse endpoint pode ser acompanhado por uma ferramenta externa de monitoramento de disponibilidade. O Healthcheck do Railway valida a inicialização do deploy, mas não substitui monitoramento contínuo após a publicação.

## Segurança e limitações

- `RECICLA_SECRET_KEY` deve ser definida no Railway; a aplicação interrompe a inicialização em ambiente Railway se a variável estiver ausente.
- O token CSRF protege os formulários de alteração.
- As consultas SQL usam parâmetros e o banco aplica chaves estrangeiras e restrições de status.
- O MVP ainda não possui autenticação/autorização para usuários. Não utilize dados pessoais reais nem o disponibilize como sistema operacional comunitário até implementar controles de acesso e realizar validação real.
- A validação comunitária feita na etapa acadêmica foi simulada. Ela não deve ser descrita como entrevista ou teste real.
