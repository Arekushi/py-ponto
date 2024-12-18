import asyncio
import logging

from functools import partial
from config.config import settings
from dependency_injector.wiring import inject, Provide

from config.logging import setup_logging
from exceptions.application_exception import ApplicationException
from src.actions import ACTIONS
from src.container import Container
from src.automation.selenium_automation import SeleniumAutomation
from src.cantinho_trabalho.cantinho_trabalho_service import CantinhoTrabalhoService
from src.helpers.log_helper import get_today_last_log
from src.notifier import start_automation_notification, cancel_automation_notification, \
    success_notion_notification, success_clocking_notification


PORTAL_URL = settings.urls.portal


@inject
async def main(
    ct_service: CantinhoTrabalhoService = Provide[Container.cantinho_trabalho_service]
):
    try:
        if (await ct_service.today_is_day_off()):
            return

        await start_automation_notification(
            on_success_callbacks=[
                partial(start_automation),
                partial(record_notion)
            ],
            on_cancel_callbacks=[
                partial(cancel_automation_notification)
            ]
        )
    except ApplicationException as e:
        logging.error(e.logmessage)
        await e.notification()
    except Exception as e:
        logging.error(e)


async def start_automation():
    automation = SeleniumAutomation(PORTAL_URL)
    automation.execute_pipeline(ACTIONS)
    automation.quit()
    
    await success_clocking_notification()


@inject
async def record_notion(
    ct_service: CantinhoTrabalhoService = Provide[Container.cantinho_trabalho_service]
):
    time_entry = await ct_service.register_time_entry()
    
    await ct_service.add_log_time_entry(
        time_entry_id=time_entry['id'],
        log_content=get_today_last_log()
    )
    
    await success_notion_notification(time_entry['url'])


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])
    setup_logging()

    asyncio.run(main())
