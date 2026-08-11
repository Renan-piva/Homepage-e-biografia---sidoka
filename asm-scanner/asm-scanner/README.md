# ASM Scanner

Scanner de superficie de ataque (Attack Surface Management) - projeto integrador.

## Estrutura do projeto

```
asm-scanner/
├── main.py                    # ponto de entrada: roda um scan completo ou inicia o agendador
├── requirements.txt
├── .env.example                 # copie para .env e preencha
├── docker-compose.yml            # sobe um PostgreSQL local
└── src/
    ├── config.py                  # le as variaveis de ambiente
    ├── database/                   # modelos e conexao com o banco
    │   ├── db.py
    │   └── models.py
    ├── discovery/                   # descoberta de ativos
    │   ├── subdomains.py             # enumeracao via crt.sh
    │   └── port_scan.py              # scan de portas via Nmap
    ├── analysis/                      # analise de vulnerabilidades
    │   ├── cve_lookup.py               # consulta a API do NVD
    │   ├── ssl_check.py                # validade/forca do certificado TLS
    │   └── http_headers.py             # headers de seguranca ausentes
    ├── scheduler/                       # agendamento dos scans
    │   └── jobs.py
    └── dashboard/                        # interface web simples (Flask)
        ├── app.py
        └── templates/
            └── index.html
```

Cada pasta dentro de `src/` corresponde a um bloco do diagrama de arquitetura:
`discovery` e `analysis` alimentam o `database`, o `scheduler` dispara tudo
periodicamente, e o `dashboard` le do banco pra mostrar os resultados.

## Como rodar

1. Crie o ambiente virtual e instale as dependencias:
   ```
   python -m venv .venv
   source .venv/bin/activate   # no Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copie `.env.example` para `.env` e preencha os valores (principalmente `TARGET_DOMAINS`).

3. Suba o banco de dados (ou use SQLite trocando `DATABASE_URL` no `.env`):
   ```
   docker compose up -d
   ```

4. Rode um scan unico:
   ```
   python main.py
   ```

5. Rode em modo continuo (agendador roda a cada `SCAN_INTERVAL_HOURS`):
   ```
   python main.py --daemon
   ```

6. Suba o dashboard (em outro terminal):
   ```
   python -m src.dashboard.app
   ```
   e acesse http://localhost:5000

## Requisito do sistema

O Nmap precisa estar instalado no sistema operacional (nao so a lib Python):
- Ubuntu/Debian: `sudo apt install nmap`
- macOS: `brew install nmap`
- Windows: instalador em https://nmap.org/download.html

## Aviso importante

So rode scans contra dominios/redes que voces tem autorizacao explicita para
testar. Scan sem autorizacao em ativos de terceiros pode configurar crime
(Lei 12.737/2012). Para o projeto integrador, usem dominios/redes proprios
ou um ambiente de laboratorio isolado (VMs, rede separada).
