from core.apps.common.exceptions import ServiceException


class RetailException(ServiceException):
    pass


class HeadOfficeDeleteException(RetailException):
    def __init__(self):
        super().__init__('Нельзя удалить головной отдел')


class RevenueClearException(RetailException):
    def __init__(self):
        super().__init__('Нельзя обнулить выручку головного отдела')
