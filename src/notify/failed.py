from winotify import Notification


def failed_mark():
    notification = Notification(
        app_id='Py Ponto',
        title='Error | Selenium',
        msg='NÃO foi possível realizar o registro do ponto...'
    )

    return notification


def failed_notion():
    notification = Notification(
        app_id='Py Ponto',
        title='Error | Notion',
        msg='NÃO foi possível registrar no Notion o registro do ponto...'
    )

    return notification
