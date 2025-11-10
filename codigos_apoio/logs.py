import logging
import os
from datetime import datetime

# Garante que exista a pasta de logs
os.makedirs("logs", exist_ok=True)

# Configuração base de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Logger principal
logger = logging.getLogger("LuminAPI")
logger.info(
    "Logging configurado com sucesso. Sistema pronto para registrar eventos.")


def registrar_acao(id_usuario: int, rota: str, mensagem: str):
    """
    Registra ações no log (arquivo e console).
    """
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{hora}] Usuário {id_usuario} acessou {rota}. {mensagem}")
    for handler in logger.handlers:
        handler.flush()
