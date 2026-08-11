"""
Verifica a validade e a data de expiracao do certificado TLS de um host.
"""
import ssl
import socket
from datetime import datetime


def verificar_certificado(host: str, porta: int = 443, dias_alerta: int = 30):
    """
    Conecta no host via TLS e retorna informacoes do certificado,
    incluindo se ele esta perto de expirar (dentro de 'dias_alerta').
    Retorna None se nao foi possivel conectar/verificar.
    """
    contexto = ssl.create_default_context()
    try:
        with socket.create_connection((host, porta), timeout=10) as sock:
            with contexto.wrap_socket(sock, server_hostname=host) as tls_sock:
                certificado = tls_sock.getpeercert()
    except (socket.error, ssl.SSLError) as erro:
        print(f"[ssl_check] falha ao verificar certificado de {host}:{porta}: {erro}")
        return None

    validade_str = certificado.get("notAfter", "")
    try:
        validade = datetime.strptime(validade_str, "%b %d %H:%M:%S %Y %Z")
    except ValueError:
        return None

    dias_restantes = (validade - datetime.utcnow()).days

    return {
        "valido_ate": validade.isoformat(),
        "dias_restantes": dias_restantes,
        "expirando": dias_restantes <= dias_alerta,
        "expirado": dias_restantes < 0,
    }
