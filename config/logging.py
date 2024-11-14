import os
import logging
from datetime import datetime
from config.config import settings


LOG_DIR = settings.DIRS.logging
LOG_FILENAME = os.path.join(LOG_DIR, datetime.now().strftime('%Y-%m-%d') + '.log')


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
