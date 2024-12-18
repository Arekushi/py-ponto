from src.exceptions.application_exception import ApplicationException
from src.notifier.failed import failed_clocking_notification


class AutomationPipelineException(ApplicationException):
    def __init__(
        self,
        message,
        title = 'Automation Pipeline Exception',
        notification = failed_clocking_notification
    ):
        super().__init__(message, title, notification)
