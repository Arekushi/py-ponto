import os
import logging

from config.config import settings
from src.helpers.date_helper import today_date_str


LOG_DIR = settings.constants.dirs.logging
LOG_FILENAME = os.path.join(LOG_DIR, today_date_str() + '.log')


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
