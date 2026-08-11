"""
Dashboard web simples para visualizar os ativos e vulnerabilidades
encontrados pelo scanner.
"""
from flask import Flask, render_template

from src.database.db import SessionLocal
from src.database.models import Asset, Vulnerabilidade

app = Flask(__name__)


@app.route("/")
def index():
    sessao = SessionLocal()
    try:
        ativos = sessao.query(Asset).order_by(Asset.ultima_vez_visto.desc()).all()
        vulnerabilidades = (
            sessao.query(Vulnerabilidade)
            .order_by(Vulnerabilidade.encontrada_em.desc())
            .limit(50)
            .all()
        )
        return render_template(
            "index.html",
            ativos=ativos,
            vulnerabilidades=vulnerabilidades,
            total_ativos=len(ativos),
            total_vulnerabilidades=sessao.query(Vulnerabilidade).count(),
        )
    finally:
        sessao.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
