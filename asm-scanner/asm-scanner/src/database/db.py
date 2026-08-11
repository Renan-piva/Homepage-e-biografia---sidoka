"""
Conexao com o banco e funcoes auxiliares de persistencia.
"""
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE_URL
from src.database.models import Base, Asset, Vulnerabilidade

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Cria as tabelas caso ainda nao existam."""
    Base.metadata.create_all(engine)


def salvar_asset(sessao, tipo, valor, dominio_pai=None):
    """Insere um ativo novo ou atualiza 'ultima_vez_visto' se ja existir."""
    existente = sessao.query(Asset).filter_by(tipo=tipo, valor=valor).first()
    if existente:
        existente.ultima_vez_visto = datetime.utcnow()
        return existente

    novo = Asset(tipo=tipo, valor=valor, dominio_pai=dominio_pai)
    sessao.add(novo)
    sessao.flush()  # garante que novo.id fique disponivel antes do commit
    return novo


def salvar_vulnerabilidade(sessao, asset, tipo, identificador, severidade, descricao):
    vuln = Vulnerabilidade(
        asset_id=asset.id,
        tipo=tipo,
        identificador=identificador,
        severidade=severidade,
        descricao=descricao,
    )
    sessao.add(vuln)
    return vuln
