import os
import logging

from src.helpers.date_helper import today_date_str
from config.config import ROOT_DIR


def delete_today_log():
    today = today_date_str()
    log_path = f'{ROOT_DIR}\\logs\\{today}.log'
    
    try:
        logging.shutdown()
        os.remove(f'{ROOT_DIR}\\logs\\{today}.log')
    except FileNotFoundError:
        logging.error(f"Erro: Arquivo '{log_path}' não encontrado.")
        return f"Erro: Arquivo '{log_path}' não encontrado."
    except PermissionError:
        logging.error(f"Erro: Permissão negada para deletar o arquivo '{log_path}'.")
        return f"Erro: Permissão negada para deletar o arquivo '{log_path}'."
    except Exception as e:
        logging.error(f"Erro inesperado ao tentar deletar o arquivo: {e}")
        return f"Erro inesperado ao tentar deletar o arquivo: {e}"


def get_today_log():
    today = today_date_str()
    log_path = f'{ROOT_DIR}\\logs\\{today}.log'
    
    try:
        with open(log_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return content
    except FileNotFoundError:
        logging.error(f"Arquivo '{log_path}' não encontrado.")
        return f"Erro: Arquivo '{log_path}' não encontrado."
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo: {e}")
        return f"Erro ao ler o arquivo: {e}"
