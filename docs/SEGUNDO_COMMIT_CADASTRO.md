# Segundo commit — cadastro de solicitações

## Mensagem sugerida

```text
feat: implementar banco SQLite e cadastro de solicitações
```

## Alterações incluídas

- Formulário Flask para cadastro de uma solicitação.
- Validação no servidor dos campos obrigatórios, limites de tamanho, contato e tipo de material ativo.
- Token CSRF vinculado à sessão para proteger o envio do formulário.
- Cadastro do solicitante e do pedido na mesma transação SQLite.
- Status inicial automático `pendente`.
- Página de confirmação com os dados persistidos.
- Tipos de material iniciais: papel, plástico, vidro e metal.
- Testes automatizados de formulário, persistência e rejeição de dados inválidos.

## Comandos no Windows PowerShell

Dentro da pasta local do repositório, com o ambiente virtual criado:

```powershell
.\.venv\Scripts\python.exe -m flask --app run init-db
.\.venv\Scripts\python.exe -m pytest -q
```

Se os testes passarem:

```powershell
git status
git add .
git commit -m "feat: implementar banco SQLite e cadastro de solicitações"
git push origin main
git log -1 --oneline
```

O SHA e a data para o histórico da atividade devem ser copiados do commit efetivamente publicado. Não os estime nem os invente.

## Banco local já existente

Como esta entrega acrescenta os tipos iniciais de materiais usando `INSERT OR IGNORE`, execute novamente `flask --app run init-db` depois de atualizar os arquivos. A operação é idempotente e não apaga as solicitações existentes.
