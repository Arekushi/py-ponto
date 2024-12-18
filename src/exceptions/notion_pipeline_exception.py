from src.exceptions.application_exception import ApplicationException


class NotionException(ApplicationException):
    def __init__(
        self,
        message,
        title = 'Notion Exception'
    ):
        super().__init__(message, title)
