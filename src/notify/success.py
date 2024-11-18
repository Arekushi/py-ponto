from winotify import Notification


def success():
    notification = Notification(
        app_id='Py Ponto',
        title='Finalizado',
        msg='O ponto foi registrado com sucesso!'
    )

    return notification
