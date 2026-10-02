# разные классы технических ошибок калькулятора-конвертора
class toolkit_Error(Exception):
    pass
class divide_by_Zero_Error(toolkit_Error):
    pass
class validation_Error(toolkit_Error):
    pass
class convector_Error(toolkit_Error):
    pass