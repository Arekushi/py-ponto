import webbrowser

from config.config import settings
from desktop_notifier import DEFAULT_SOUND, Button, DesktopNotifier, Urgency
from src.notifier import timeout_notification


async def success_clocking(
    notifier: DesktopNotifier
):
    await notifier.send(
        title='Marcação finalizada',
        message='Ponto marcado com sucesso!',
        urgency=Urgency.Critical,
        on_clicked=None,
        on_dismissed=None,
        timeout=10,
        sound=DEFAULT_SOUND,
    )


async def success_notion(
    notifier: DesktopNotifier,
    time_entry_url: str
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
            urgency=Urgency.Critical,
            on_clicked=None,
            on_dismissed=None,
            timeout=10,
            sound=DEFAULT_SOUND,
        )
    )
