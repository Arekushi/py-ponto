import asyncio
import logging

from functools import partial
from config.config import settings
from dependency_injector.wiring import inject, Provide

from src.actions import ACTIONS
from src.container import Container
from src.selenium.pipeline_automation import PipelineAutomation
from src.cantinho_trabalho.cantinho_trabalho_service import CantinhoTrabalhoService
from src.helpers.log_helper import get_today_last_log
from src.notifier import start_notification, cancel_notification, \
    failed_notion, success_notion, failed_clocking, success_clocking


PORTAL_URL = settings.urls.portal


@inject
async def main(
    ct_service: CantinhoTrabalhoService = Provide[Container.cantinho_trabalho_service]
):
    if (await ct_service.today_is_day_off()):
        return

    await start_notification(
        on_success_callbacks=[
            partial(start_automation),
            partial(record_notion)
        ],
        on_cancel_callbacks=[
            partial(cancel_notification)
        ]
    )


async def start_automation():
    automation = PipelineAutomation(PORTAL_URL)

    try:
        automation.execute_pipeline(ACTIONS)
        automation.quit()
        await success_clocking()
    except Exception as e:
        logging.error(e)
        await failed_clocking()


@inject
async def record_notion(
    ct_service: CantinhoTrabalhoService = Provide[Container.cantinho_trabalho_service]
):
    try:
        time_entry = await ct_service.register_time_entry()
        
        await ct_service.add_log_time_entry(
            time_entry_id=time_entry['id'],
            log_content=get_today_last_log()
        )
        
        await success_notion(time_entry['url'])
    except Exception as e:
        logging.error(e)
        await failed_notion()


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())
