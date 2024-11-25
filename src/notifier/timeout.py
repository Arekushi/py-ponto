import asyncio
from config.config import settings


TIMEOUT_NOTIFICATION_MINUTES = settings.constants.timeout_notification_minutes


async def timeout_notification(
    notification,
    timeout_minutes=TIMEOUT_NOTIFICATION_MINUTES
):    
    await notification
    
    timeout_task = asyncio.create_task(asyncio.sleep(timeout_minutes * 60))

    await asyncio.wait(
        [timeout_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
