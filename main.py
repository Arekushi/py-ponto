import logging

from config.config import settings
from src.selenium.pipeline_automation import PipelineAutomation
from src.selenium.action_type import ActionType as AT
# from src.notifier import failed, success
# from src.date_helper import is_day_off, get_today
from config.logging import setup_logging
from random import randrange

BASE_URL = settings.URLS.base_url

ACTIONS = [
    {
        'type': AT.INPUT,
        'xpath': settings.XPATH.LOGIN.email_input,
        'value': settings.LOGIN.user
    },
    {
        'type': AT.INPUT,
        'xpath': settings.XPATH.LOGIN.password_input,
        'value': settings.LOGIN.password
    },
    {
        'type': AT.CLICK,
        'xpath': settings.XPATH.LOGIN.login_button
    },
    {
        'type': AT.SLEEP,
        'time': randrange(0, settings.VARS.delay_minutes_range * 60)
    },
    {
        'type': AT.CLICK,
        'xpath': settings.XPATH.MAIN.register_button
    },
    {
        'type': AT.WAIT_FOR,
        'xpath': settings.XPATH.MAIN.popup_div
    },
    {
        'type': AT.SLEEP,
        'time': 5,
        'callbacks': [
            # success().show
        ]
    }
]

def main():
    setup_logging()
    
    # if not is_day_off():
    #     start_automation()
    # else:
    #     pass
    #     logging.warning(f'Hoje [{get_today()}] é um dia de folga')


def start_automation():
    automation = PipelineAutomation(BASE_URL)
    
    try:
        automation.execute_pipeline(ACTIONS)
    except Exception as e:
        logging.error(e)
        # failed().show()
        
    automation.quit()


if __name__ == '__main__':
    main()
