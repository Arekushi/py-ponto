from src.notifier.failed import failed_notion_notification


class NotionException(Exception):
    def __init__(
        self,
        message,
        title = 'Notion Exception',
        notification = failed_notion_notification
    ):
        super().__init__(message, title, notification)
