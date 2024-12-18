from src.exceptions.application_exception import ApplicationException


class AutomationPipelineException(ApplicationException):
    def __init__(
        self,
        message,
        title = 'Automation Pipeline Exception'
    ):
        super().__init__(message, title)
