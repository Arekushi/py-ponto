class ApplicationException(Exception):
    def __init__(
        self,
        message,
        title = 'Application Exception',
        notification = None
    ):
        super().__init__(message)
        
        self.title = title
        self.message = message
        self.logmessage = f'{title} - {message}'
        self.notification = notification
