# Como executar o Recicla Bairro no Windows

Este roteiro utiliza o repositório GitHub já criado:
https://github.com/ocionemendes-png/recicla-bairro-mvp

## 1. Clonar o repositório

Abra o PowerShell e execute:

```powershell
cd $HOME\Documents
git clone https://github.com/ocionemendes-png/recicla-bairro-mvp.git
cd recicla-bairro-mvp
```

Se a pasta já existir no computador, entre nela com `cd` em vez de clonar novamente.

## 2. Copiar os arquivos do pacote inicial

1. Baixe `recicla-bairro-mvp-inicial.zip`.
2. Extraia o conteúdo da pasta `recicla-bairro-mvp` para dentro da pasta local `recicla-bairro-mvp` que foi clonada.
3. Quando o Windows perguntar se deseja substituir o `README.md`, escolha substituir.
4. **Não apague nem substitua a pasta oculta `.git`**. Ela contém a ligação com o GitHub.

## 3. Confirmar o Python e preparar o ambiente

No PowerShell, dentro da pasta do repositório:

```powershell
py -3.13 --version
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Se o PowerShell bloquear a ativação do ambiente virtual, execute apenas nesta janela:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Não é necessário alterar a política permanente do Windows.

## 4. Inicializar o banco e executar os testes

```powershell
flask --app run init-db
python -m pytest -q
```

O teste deverá apresentar três casos aprovados. Se aparecer erro, copie a mensagem completa e encaminhe para análise antes de fazer o commit.

## 5. Abrir a aplicação

```powershell
python run.py
```

Abra `http://127.0.0.1:5000/` no navegador. Para verificar o endpoint de saúde, acesse `http://127.0.0.1:5000/health`.

Para parar o servidor, volte ao PowerShell e pressione `Ctrl+C`.

## 6. Criar o primeiro commit

Somente depois que os testes passarem:

```powershell
git status
git add .
git commit -m "feat: criar estrutura inicial da aplicação Flask"
git push origin main
```

Se o Git solicitar identificação e ela ainda não estiver configurada, informe seu nome e um e-mail associado à sua conta GitHub:

```powershell
git config user.name "Seu nome"
git config user.email "Seu e-mail do GitHub"
```

Essas configurações são locais ao repositório.

## 7. Registrar o commit na atividade

Depois do `git push`:

1. Abra o repositório no GitHub.
2. Clique em **Commits**.
3. Abra o commit mais recente.
4. Copie os primeiros 7 caracteres do SHA.
5. Registre a mensagem e a data efetivamente exibidas.

Não invente SHA nem data. A plataforma da atividade deve receber os dados do commit real.
