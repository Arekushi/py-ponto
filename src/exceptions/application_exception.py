class ApplicationException(Exception):
    def __init__(
        self,
        message,
        title = 'Application Exception'
    ):
        super().__init__(message)
        
        self.title = title
        self.message = message
        self.logmessage = f'{title} - {message}'
