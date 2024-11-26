import logging

from config.config import settings, ROOT_DIR
from src.helpers.date_helper import now_date_str
from src.helpers.path_helper import get_latest_file


LOG_DIR = settings.constants.dirs.logging


def get_today_last_log():
    today = now_date_str()
    log_path = f'{ROOT_DIR}/{LOG_DIR}/{today}'
    last_log_path = get_latest_file(log_path)
    
    try:
        with open(last_log_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return content
    except FileNotFoundError:
        logging.error(f"Arquivo '{last_log_path}' não encontrado.")
        return f"Erro: Arquivo '{last_log_path}' não encontrado."
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo: {e}")
        return f"Erro ao ler o arquivo: {e}"
