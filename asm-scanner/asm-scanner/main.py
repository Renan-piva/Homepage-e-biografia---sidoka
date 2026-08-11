"""
Ponto de entrada do scanner ASM.

Uso:
    python main.py              -> roda um scan completo uma unica vez
    python main.py --daemon     -> roda uma vez e depois inicia o agendador
"""
import sys
import time

from src.config import TARGET_DOMAINS
from src.database.db import init_db, SessionLocal, salvar_asset, salvar_vulnerabilidade
from src.discovery.subdomains import enumerar_subdominios
from src.discovery.port_scan import escanear_host
from src.analysis.cve_lookup import buscar_cves
from src.analysis.ssl_check import verificar_certificado
from src.analysis.http_headers import checar_headers
from src.scheduler.jobs import iniciar_agendador


def rodar_scan_completo():
    """Executa um ciclo completo de descoberta + analise para todos os dominios alvo."""
    if not TARGET_DOMAINS:
        print("Nenhum dominio configurado em TARGET_DOMAINS (.env). Encerrando.")
        return

    sessao = SessionLocal()
    try:
        for dominio in TARGET_DOMAINS:
            print(f"\n=== Escaneando {dominio} ===")

            subdominios = enumerar_subdominios(dominio)
            print(f"{len(subdominios)} subdominios encontrados")

            for sub in subdominios:
                salvar_asset(sessao, tipo="subdominio", valor=sub, dominio_pai=dominio)

                portas = escanear_host(sub)
                for p in portas:
                    servico_str = f"{p['porta']}/{p['servico']}"
                    asset_porta = salvar_asset(sessao, tipo="porta", valor=servico_str, dominio_pai=sub)

                    # certificado TLS, se houver servico web seguro
                    if p["porta"] in (443, 8443):
                        cert = verificar_certificado(sub, p["porta"])
                        if cert and (cert["expirando"] or cert["expirado"]):
                            salvar_vulnerabilidade(
                                sessao, asset_porta, tipo="ssl_expirado",
                                identificador=None,
                                severidade="alta" if cert["expirado"] else "media",
                                descricao=f"Certificado expira em {cert['dias_restantes']} dias",
                            )

                    # headers de seguranca, se houver servico web
                    if p["porta"] in (80, 443, 8080, 8443):
                        protocolo = "https" if p["porta"] in (443, 8443) else "http"
                        ausentes = checar_headers(f"{protocolo}://{sub}:{p['porta']}")
                        for header in ausentes:
                            salvar_vulnerabilidade(
                                sessao, asset_porta, tipo="header_ausente",
                                identificador=header, severidade="baixa",
                                descricao=f"Header de seguranca ausente: {header}",
                            )

                    # CVEs conhecidas para o produto/versao detectados
                    if p.get("produto"):
                        cves = buscar_cves(p["produto"], p.get("versao", ""))
                        for cve in cves:
                            salvar_vulnerabilidade(
                                sessao, asset_porta, tipo="cve",
                                identificador=cve["cve_id"],
                                severidade=cve["severidade"],
                                descricao=cve["descricao"],
                            )

            sessao.commit()
            print(f"=== {dominio} concluido e salvo no banco ===")

    finally:
        sessao.close()


if __name__ == "__main__":
    init_db()

    if "--daemon" in sys.argv:
        rodar_scan_completo()  # roda uma vez imediatamente
        agendador = iniciar_agendador(rodar_scan_completo)
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            agendador.shutdown()
    else:
        rodar_scan_completo()
