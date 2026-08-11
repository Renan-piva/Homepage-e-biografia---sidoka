"""
Scan de portas e servicos usando o Nmap (via biblioteca python-nmap).
Requer o binario 'nmap' instalado no sistema operacional.
"""
import nmap

PORTAS_COMUNS = "21,22,25,53,80,110,143,443,445,993,995,3306,3389,5432,8080,8443"


def escanear_host(host: str) -> list[dict]:
    """
    Roda um scan de portas comuns em um host e retorna uma lista de
    dicionarios com porta, protocolo, servico, versao e produto detectados.
    """
    scanner = nmap.PortScanner()
    try:
        scanner.scan(host, PORTAS_COMUNS, arguments="-sV -T4")
    except nmap.PortScannerError as erro:
        print(f"[port_scan] falha ao escanear {host}: {erro}")
        return []

    resultados = []
    if host not in scanner.all_hosts():
        return resultados

    for proto in scanner[host].all_protocols():
        portas = scanner[host][proto].keys()
        for porta in portas:
            info = scanner[host][proto][porta]
            if info.get("state") == "open":
                resultados.append({
                    "porta": porta,
                    "protocolo": proto,
                    "servico": info.get("name", ""),
                    "versao": info.get("version", ""),
                    "produto": info.get("product", ""),
                })

    return resultados
