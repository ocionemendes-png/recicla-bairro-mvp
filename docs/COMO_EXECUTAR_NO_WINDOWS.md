# Atualizar e executar o Recicla Bairro no Windows

Este roteiro parte do princípio de que o repositório já foi clonado em:

```text
C:\Users\SEU_USUARIO\Documents\recicla-bairro-mvp
```

O pacote de atualização não contém a pasta `.git` nem o banco SQLite local. Assim, a ligação com o GitHub e os dados já existentes serão preservados.

## 1. Substituir os arquivos do projeto

1. Pare o servidor Flask, se estiver aberto, pressionando `Ctrl+C` no PowerShell que o executa.
2. Baixe o arquivo `recicla-bairro-cadastro-v2.zip`.
3. Extraia o conteúdo para `C:\Users\SEU_USUARIO\Documents`.
4. Quando o Windows perguntar se deseja substituir arquivos existentes, escolha substituir.
5. Não apague a pasta oculta `.git` e não exclua `instance\recicla.sqlite3`.

## 2. Entrar na pasta e inicializar os tipos de material

Abra o PowerShell:

```powershell
cd $HOME\Documents\recicla-bairro-mvp
```

Execute novamente a inicialização do banco. Ela cria as tabelas caso ainda não existam e inclui os tipos Papel, Plástico, Vidro e Metal sem duplicá-los:

```powershell
.\.venv\Scripts\python.exe -m flask --app run init-db
```

## 3. Executar os testes

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Resultado esperado nesta versão: `11 passed`. Se algum teste falhar, guarde a mensagem completa e corrija antes do commit.

## 4. Executar a aplicação

```powershell
.\.venv\Scripts\python.exe run.py
```

Abra no navegador:

- Página inicial: http://127.0.0.1:5000/
- Cadastro: http://127.0.0.1:5000/solicitacoes/nova
- Verificação: http://127.0.0.1:5000/health

Use apenas dados demonstrativos, por exemplo `Carlos Exemplo`, `carlos.exemplo@teste.invalid`, `Rua das Acácias, 100` e material `Papel`. Não use dados pessoais reais.

Depois de salvar, a aplicação deverá apresentar o identificador SOL seguido do número gerado, os dados registrados e o status inicial Pendente.

## 5. Criar o segundo commit

Depois de confirmar os testes e executar um cadastro demonstrativo:

```powershell
git status
git add .
git commit -m "feat: implementar banco SQLite e cadastro de solicitações"
git push origin main
git log -1 --oneline
```

Copie SHA, mensagem e data do commit efetivamente publicado para a atividade acadêmica. Não invente identificadores ou datas.

## Observação sobre data e horário

O SQLite registra `CURRENT_TIMESTAMP` em UTC. A aplicação converte esse valor
para o horário de Brasília (UTC-03) somente na tela de confirmação. Portanto,
o dado original do banco permanece em UTC.
