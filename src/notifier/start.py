import asyncio
import inspect

from config.config import settings
from desktop_notifier import DEFAULT_SOUND, Button, DesktopNotifier, Urgency


START_DELAY_TIME = settings.constants.start_minutes_delay


async def start_notification(
    notifier: DesktopNotifier,
    on_success_callbacks=[],
    on_cancel_callbacks=[]
):
    add_delay_time_event = asyncio.Event()
    cancel_action_event = asyncio.Event()

    interaction_delay_time = 0

    def add_delay_time(delay_secs: int):
        nonlocal interaction_delay_time
        add_delay_time_event.set()
        interaction_delay_time = delay_secs

    def cancel_action():
        cancel_action_event.set()

    await notifier.send(
        title=f'Py Ponto irá bater o ponto em {START_DELAY_TIME} minuto(s)!',
        message='Deseja adiar em quantos minutos?',
        urgency=Urgency.Critical,
        buttons=[
            Button(
                title='+15min',
                on_pressed=lambda: add_delay_time(15 * 60),
            ),
            Button(
                title='+30min',
                on_pressed=lambda: add_delay_time(30 * 60),
            ),
            Button(
                title='+45min',
                on_pressed=lambda: add_delay_time(45 * 60),
            ),
            Button(
                title='+1h',
                on_pressed=lambda: add_delay_time(60 * 60),
            ),
            Button(
                title='Cancelar',
                on_pressed=lambda: cancel_action(),
            ),
        ],
        on_clicked=None,
        on_dismissed=None,
        sound=DEFAULT_SOUND,
    )

    add_delay_time_task = asyncio.create_task(add_delay_time_event.wait())
    cancel_action_task = asyncio.create_task(cancel_action_event.wait())
    timeout_task = asyncio.create_task(asyncio.sleep(START_DELAY_TIME))

    _, pending = await asyncio.wait(
        [add_delay_time_task, cancel_action_task, timeout_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

    await asyncio.sleep(interaction_delay_time)

    callbacks = on_cancel_callbacks \
        if cancel_action_event.is_set() \
        else on_success_callbacks

    for callback in callbacks:
        await call_callback(callback)


async def call_callback(callback):
    if inspect.iscoroutinefunction(callback):
        await callback()
    else:
        callback()