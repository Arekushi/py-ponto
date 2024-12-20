import webbrowser
from dependency_injector.wiring import inject, Provide

from config.config import settings
from desktop_notifier import DEFAULT_SOUND, Button, DesktopNotifier, Urgency
from src.notifier.timeout import timeout_notification
from src.container import Container


PORTAL_URL = settings.urls.portal


@inject
async def cancel_automation_notification(
    notifier: DesktopNotifier = Provide[Container.notifier]
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
            urgency=Urgency.Normal,
            on_clicked=None,
            on_dismissed=None,
            timeout=10,
            sound=DEFAULT_SOUND,
        )
    )
