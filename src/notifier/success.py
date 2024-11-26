import webbrowser
from dependency_injector.wiring import inject, Provide

from config.config import settings
from desktop_notifier import DEFAULT_SOUND, Button, DesktopNotifier, Urgency
from src.notifier import timeout_notification
from src.container import Container


@inject
async def success_clocking(
    notifier: DesktopNotifier = Provide[Container.notifier]
):
    await notifier.send(
        title='Marcação finalizada',
        message='Ponto marcado com sucesso!',
        urgency=Urgency.Normal,
        on_clicked=None,
        on_dismissed=None,
        timeout=10,
        sound=DEFAULT_SOUND,
    )


@inject
async def success_notion(
    time_entry_url: str,
    notifier: DesktopNotifier = Provide[Container.notifier],
):
    await timeout_notification(
        notifier.send(
            title='Registro Notion finalizado',
            message='Ponto registrado no Notion com sucesso!',
            buttons=[
                Button(
                    title='Abrir página no Notion',
                    on_pressed=lambda: webbrowser.open(time_entry_url),
                ),
            ],
            urgency=Urgency.Normal,
            on_clicked=None,
            on_dismissed=None,
            timeout=10,
            sound=DEFAULT_SOUND,
        )
    )
