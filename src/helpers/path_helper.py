import os
import shutil
import logging


def get_latest_file(directory):
    files = [
        os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    
    if not files:
        return None

    latest_file = max(files, key=os.path.getmtime)
    return latest_file


def delete_directory(dir_path):
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path)
            logging.info(f"O diretório '{dir_path}' foi deletado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao deletar o diretório '{dir_path}': {e}")
    else:
        logging.warning(f"O diretório '{dir_path}' não existe.")
