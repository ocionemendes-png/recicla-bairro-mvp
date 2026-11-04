# Quarto commit — atualização de status

Mensagem sugerida para o commit:

```text
feat: implementar atualização do status das solicitações
```

## O que foi implementado

- Formulário de alteração do status na página de detalhes.
- Gravação da alteração no SQLite.
- Validação das transições permitidas no servidor.
- Proteção CSRF do formulário.
- Repercussão do status atualizado na listagem e nos detalhes.
- Tratamento de status inválido, pedido inexistente e estado final.

## Fluxo de status desta versão

- Pendente -> Em andamento ou Concluída.
- Em andamento -> Concluída.
- Concluída -> sem novas transições.

## Testes

Execute no PowerShell, dentro da pasta do repositório:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

O conjunto inclui os testes existentes de cadastro e consulta, além dos novos testes de atualização, persistência, validação de transição, CSRF e pedido inexistente.

O SHA e a data devem ser copiados do commit real depois da publicação no GitHub.
