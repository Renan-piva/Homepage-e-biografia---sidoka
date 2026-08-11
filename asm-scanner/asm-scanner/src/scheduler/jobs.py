"""
Agendamento dos scans periodicos usando APScheduler.
"""
from apscheduler.schedulers.background import BackgroundScheduler

from src.config import SCAN_INTERVAL_HOURS


def iniciar_agendador(funcao_scan):
    """
    Inicia um agendador em background que roda 'funcao_scan' a cada
    SCAN_INTERVAL_HOURS horas.
    """
    agendador = BackgroundScheduler()
    agendador.add_job(funcao_scan, "interval", hours=SCAN_INTERVAL_HOURS)
    agendador.start()
    print(f"[scheduler] agendador iniciado - scans a cada {SCAN_INTERVAL_HOURS}h")
    return agendador
