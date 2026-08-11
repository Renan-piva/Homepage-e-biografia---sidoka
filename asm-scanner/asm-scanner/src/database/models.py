"""
Modelos do banco de dados: ativos descobertos, execucoes de scan e vulnerabilidades.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Asset(Base):
    """Um ativo descoberto: um subdominio, IP ou porta/servico."""
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)          # "subdominio", "ip", "porta"
    valor = Column(String, nullable=False)          # ex: "app.exemplo.com.br", "22/ssh"
    dominio_pai = Column(String)                     # dominio/host ao qual pertence
    primeira_vez_visto = Column(DateTime, default=datetime.utcnow)
    ultima_vez_visto = Column(DateTime, default=datetime.utcnow)

    vulnerabilidades = relationship("Vulnerabilidade", back_populates="asset")


class ScanRun(Base):
    """Registro de uma execucao de scan."""
    __tablename__ = "scan_runs"

    id = Column(Integer, primary_key=True)
    iniciado_em = Column(DateTime, default=datetime.utcnow)
    finalizado_em = Column(DateTime)
    ativos_encontrados = Column(Integer, default=0)


class Vulnerabilidade(Base):
    """Uma vulnerabilidade ou problema de configuracao encontrado em um ativo."""
    __tablename__ = "vulnerabilidades"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    tipo = Column(String, nullable=False)             # "cve", "ssl_expirado", "header_ausente"
    identificador = Column(String)                      # ex: "CVE-2023-1234"
    severidade = Column(String)                          # "baixa", "media", "alta", "critica"
    descricao = Column(String)
    encontrada_em = Column(DateTime, default=datetime.utcnow)

    asset = relationship("Asset", back_populates="vulnerabilidades")
