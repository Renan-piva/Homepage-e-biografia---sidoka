"""
Descoberta de subdominios via Certificate Transparency (crt.sh).
"""
import requests


def enumerar_subdominios(dominio: str) -> list[str]:
    """
    Consulta o crt.sh e retorna a lista de subdominios unicos encontrados
    nos certificados emitidos para o dominio informado.
    """
    url = f"https://crt.sh/?q=%25.{dominio}&output=json"
    try:
        resposta = requests.get(url, timeout=15)
        resposta.raise_for_status()
    except requests.RequestException as erro:
        print(f"[subdominios] falha ao consultar crt.sh para {dominio}: {erro}")
        return []

    encontrados = set()
    for registro in resposta.json():
        nomes = registro.get("name_value", "")
        for nome in nomes.split("\n"):
            nome = nome.strip().lower()
            if nome and "*" not in nome:
                encontrados.add(nome)

    return sorted(encontrados)
