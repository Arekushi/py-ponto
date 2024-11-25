import os
import logging

from config.config import settings
from src.helpers.date_helper import now_date_str, now_datetime_str


LOG_DIR = f'{settings.constants.dirs.logging}\\{now_date_str()}'
LOG_FILENAME = os.path.join(LOG_DIR, f"{now_datetime_str('%Hh-%Mmin')}.log")


def setup_logging():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )
