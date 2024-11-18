import asyncio
import logging

from config.config import settings
from dependency_injector.wiring import inject, Provide

from src.actions import ACTIONS
from src.selenium.pipeline_automation import PipelineAutomation
from src.cantinho_trabalho.cantinho_trabalho_service import CantinhoTrabalhoService
from src.notify import failed_mark, failed_notion, success
from src.helpers.log_helper import delete_today_log, get_today_log
from src.container import Container


MAIN_URL = settings.urls.main_url


async def main():
    start_automation()
    await record_notion(log_content=get_today_log())
    
    delete_today_log()
    success().show()


def start_automation():
    automation = PipelineAutomation(MAIN_URL)
    
    try:
        automation.execute_pipeline(ACTIONS)
    except Exception as e:
        logging.error(e)
        failed_mark().show()
    
    automation.quit()


@inject
async def record_notion(
    log_content: str,
    ct_service: CantinhoTrabalhoService = Provide[Container.cantinho_trabalho_service]
):
    try:
        time_entry = await ct_service.register_time_entry()
        await ct_service.add_log_time_entry(time_entry, log_content)
    except Exception as e:
        logging.error(e)
        failed_notion().show()


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])

    asyncio.run(main())
