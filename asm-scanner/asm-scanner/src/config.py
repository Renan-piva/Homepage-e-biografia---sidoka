"""
Le as variaveis de ambiente e centraliza a configuracao do projeto.
"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///asm_scanner.db")
NVD_API_KEY = os.getenv("NVD_API_KEY", "")

_dominios = os.getenv("TARGET_DOMAINS", "")
TARGET_DOMAINS = [d.strip() for d in _dominios.split(",") if d.strip()]

SCAN_INTERVAL_HOURS = int(os.getenv("SCAN_INTERVAL_HOURS", "24"))
