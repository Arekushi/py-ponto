import webbrowser
from dependency_injector.wiring import inject, Provide

from config.config import settings
from desktop_notifier import DEFAULT_SOUND, Button, DesktopNotifier, Urgency
from src.notifier import timeout_notification
from src.container import Container


PORTAL_URL = settings.urls.portal


@inject
async def failed_clocking(
    notifier: DesktopNotifier = Provide[Container.notifier]
):
    await timeout_notification(
        notifier.send(
            title='Error | Selenium',
            message='NÃO foi possível realizar o registro do ponto...',
            buttons=[
                Button(
                    title='Abrir o portal',
                    on_pressed=lambda: webbrowser.open(PORTAL_URL),
                ),
            ],
            urgency=Urgency.Critical,
            on_clicked=None,
            on_dismissed=None,
            timeout=10,
            sound=DEFAULT_SOUND,
        )
    )


@inject
async def failed_notion(
    notifier: DesktopNotifier = Provide[Container.notifier],
):
    await timeout_notification(
        notifier.send(
            title='Error | Notion',
            message='NÃO foi possível registrar no Notion o registro do ponto...',
            buttons=[
                Button(
                    title='Abrir o portal',
                    on_pressed=lambda: webbrowser.open(PORTAL_URL),
                ),
            ],
            urgency=Urgency.Critical,
            on_clicked=None,
            on_dismissed=None,
            timeout=10,
            sound=DEFAULT_SOUND,
        )
    )
