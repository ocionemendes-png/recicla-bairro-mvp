# Como aplicar e testar a atualização de status (quarto commit)

## 1. Preservar o projeto existente

1. Pare o servidor Flask com `Ctrl+C`.
2. Extraia o pacote `recicla-bairro-status-v4.zip` em `C:\Users\ocion\Documents`.
3. Quando solicitado, permita substituir os arquivos do projeto.
4. Não exclua nem substitua a pasta oculta `.git` nem o banco `instance\recicla.sqlite3`.

O pacote não contém a pasta `.git` nem um banco SQLite, para preservar o histórico do GitHub e as solicitações já cadastradas.

## 2. Executar os testes

No PowerShell:

```powershell
cd $HOME\Documents\recicla-bairro-mvp
.\.venv\Scripts\python.exe -m pytest -q
```

A suíte contém 23 testes previstos: os 16 testes anteriores e 7 novos testes relacionados à atualização de status. Só prossiga para o commit se todos passarem.

## 3. Conferir a atualização no navegador

Inicie o servidor:

```powershell
.\.venv\Scripts\python.exe run.py
```

Abra a listagem:

`http://127.0.0.1:5000/solicitacoes`

Abra os detalhes do pedido `SOL-0001`. Na seção **Atualizar status da coleta**, selecione **Em andamento** e clique em **Salvar alteração**. Confirme que:

- a mensagem de sucesso aparece;
- o status no cabeçalho dos detalhes muda para **Em andamento**;
- a listagem também mostra **Em andamento**;
- o filtro **Em andamento** localiza esse pedido.

Depois, atualize o pedido para **Concluída** e confira que a página informa que não há novas etapas disponíveis.

## 4. Criar e publicar o quarto commit

Somente após os testes e a conferência visual:

```powershell
git status
git add .
git commit -m "feat: implementar atualização do status das solicitações"
git push origin main
git log -1 --format="%h | %s | %cd" --date=format:"%d/%m/%Y"
```

Copie o SHA e a data efetivamente exibidos pelo Git. Não invente identificadores nem datas para o formulário acadêmico.
