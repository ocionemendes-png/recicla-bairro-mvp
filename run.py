"""Ponto de entrada para executar a aplicação localmente."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Servidor de desenvolvimento: não utilizar debug=True em produção.
    app.run(host="127.0.0.1", port=5000, debug=True)
