import pytz
from datetime import datetime


BRASIL_TZ = pytz.timezone('America/Sao_Paulo')

def now_date_str(format='%Y-%m-%d'):
    return datetime.now(BRASIL_TZ).strftime(format)


def now_datetime_str(format='%Y-%m-%dT%H:%M:%S%z'):
    return datetime.now(BRASIL_TZ).strftime(format)
