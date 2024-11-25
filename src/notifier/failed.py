import webbrowser

from config.config import settings
from desktop_notifier import DEFAULT_SOUND, Button, DesktopNotifier, Urgency
from src.notifier import timeout_notification


PORTAL_URL = settings.urls.portal


async def failed_clocking(
    notifier: DesktopNotifier
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


async def failed_notion(
    notifier: DesktopNotifier
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
            sound=DEFAULT_SOUND,
        )
    )
