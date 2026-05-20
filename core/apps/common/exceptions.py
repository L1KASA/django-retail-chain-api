class ServiceException(Exception):
    """Базовое исключение бизнес-логики."""
    
    def __init__(self, message: str = 'Application exception occurred'):
        self.message = message
        super().__init__(self.message)
