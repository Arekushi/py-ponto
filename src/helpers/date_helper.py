from datetime import datetime, timedelta
import pytz


BRASIL_TZ = pytz.timezone('America/Sao_Paulo')


def now_adjusted_by_days(days, format='%Y-%m-%d'):    
    original_date = datetime.now(BRASIL_TZ)
    adjusted_date = original_date + timedelta(days=days)
    return adjusted_date.strftime(format)


def now_date_str(format='%Y-%m-%d'):
    return datetime.now(BRASIL_TZ).strftime(format)


def now_datetime_str(format='%Y-%m-%dT%H:%M:%S%z'):
    return datetime.now(BRASIL_TZ).strftime(format)
