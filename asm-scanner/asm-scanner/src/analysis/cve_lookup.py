"""
Consulta a API do NVD (National Vulnerability Database) por CVEs
relacionadas a um produto/versao de servico encontrado no scan.
"""
import time
import requests

from src.config import NVD_API_KEY

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

MAPA_SEVERIDADE = {
    "LOW": "baixa",
    "MEDIUM": "media",
    "HIGH": "alta",
    "CRITICAL": "critica",
}


def buscar_cves(produto: str, versao: str = "", limite: int = 5) -> list[dict]:
    """
    Busca CVEs conhecidas para um produto (e opcionalmente versao).
    Retorna uma lista simplificada com id, severidade (em pt-br) e descricao curta.
    """
    if not produto:
        return []

    termo = f"{produto} {versao}".strip()
    parametros = {"keywordSearch": termo, "resultsPerPage": limite}
    cabecalhos = {"apiKey": NVD_API_KEY} if NVD_API_KEY else {}

    try:
        resposta = requests.get(NVD_URL, params=parametros, headers=cabecalhos, timeout=20)
        resposta.raise_for_status()
    except requests.RequestException as erro:
        print(f"[cve_lookup] falha ao consultar NVD para '{termo}': {erro}")
        return []
    finally:
        # a API do NVD tem limite de requisicoes por segundo sem chave cadastrada
        time.sleep(1 if NVD_API_KEY else 6)

    encontrados = []
    for item in resposta.json().get("vulnerabilities", []):
        cve = item.get("cve", {})
        cve_id = cve.get("id", "")
        descricoes = cve.get("descriptions", [])
        descricao = next((d["value"] for d in descricoes if d.get("lang") == "en"), "")

        metricas = cve.get("metrics", {})
        severidade = "desconhecida"
        for chave in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if chave in metricas:
                bruta = metricas[chave][0]["cvssData"].get("baseSeverity", "")
                severidade = MAPA_SEVERIDADE.get(bruta, "desconhecida")
                break

        encontrados.append({
            "cve_id": cve_id,
            "severidade": severidade,
            "descricao": descricao[:200],
        })

    return encontrados
