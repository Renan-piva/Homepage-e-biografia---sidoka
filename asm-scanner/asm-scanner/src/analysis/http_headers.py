"""
Verifica a presenca de headers HTTP relacionados a seguranca.
"""
import requests

HEADERS_ESPERADOS = [
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Content-Security-Policy",
]


def checar_headers(url: str) -> list[str]:
    """
    Faz uma requisicao GET na URL e retorna a lista de headers de
    seguranca esperados que NAO foram encontrados na resposta.
    """
    try:
        resposta = requests.get(url, timeout=10, allow_redirects=True)
    except requests.RequestException as erro:
        print(f"[http_headers] falha ao acessar {url}: {erro}")
        return []

    return [h for h in HEADERS_ESPERADOS if h not in resposta.headers]
