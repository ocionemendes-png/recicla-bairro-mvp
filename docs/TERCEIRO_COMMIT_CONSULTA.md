# Terceiro commit — consulta e listagem de solicitações

Mensagem sugerida após os testes locais:

```text
feat: implementar consulta e listagem de solicitações
```

## O que foi implementado

- Rota GET `/solicitacoes` para listar pedidos gravados no SQLite.
- Filtro por status: todos, pendente, em andamento ou concluída.
- Contadores de solicitações por status.
- Exibição de identificador, solicitante, material, endereço, situação e data.
- Link para abrir os detalhes de cada pedido.
- Estado vazio quando ainda não existem pedidos ou quando o filtro não encontra resultados.
- Página de detalhes reaproveitada após o cadastro e a partir da listagem.

## Testes acrescentados

- Exibição de um pedido persistido na listagem.
- Aplicação do filtro de status.
- Rejeição de status desconhecido.
- Acesso à página de detalhes a partir da listagem.

## Como testar no Windows (PowerShell)

Com o ambiente virtual do projeto ativo ou chamando seu executável diretamente:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe run.py
```

Abra `http://127.0.0.1:5000/solicitacoes`. Cadastre previamente dois ou mais pedidos em `/solicitacoes/nova` para visualizar a lista e experimentar os filtros.

O filtro por situações diferentes de `pendente` pode ser demonstrado com registros já marcados nesses estados em uma futura entrega, pois a atualização do status ainda não faz parte deste commit.

## Publicação

Somente após confirmar que os testes passaram:

```powershell
git status
git add .
git commit -m "feat: implementar consulta e listagem de solicitações"
git push origin main
git log -1 --format="%h | %s | %cd" --date=format:"%d/%m/%Y"
```

Copie SHA e data do commit real para o histórico da atividade. Não utilize valores de exemplo.
