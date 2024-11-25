import webbrowser

from config.config import settings
from desktop_notifier import DEFAULT_SOUND, Button, DesktopNotifier, Urgency
from src.notifier import timeout_notification


PORTAL_URL = settings.urls.portal


async def cancel_notification(
    notifier: DesktopNotifier
):    
    await timeout_notification(
        notifier.send(
            title='A ação de registrar o ponto foi cancelada com sucesso!',
            message='Marque o ponto manualmente...',
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
