from aiogram.filters.callback_data import CallbackData


class SelectHourCallbackData(CallbackData, prefix='select_hour'):
    hour:int


class SelectMinuteCallbackData(CallbackData, prefix='select_minute'):
    minute:int


class ReadyDateCallbackData(CallbackData, prefix='ready_date'):
    year: int
    month: int
    day: int


class SelectDateCallbackData(CallbackData, prefix='select_date'):
    year: int
    month: int


class ChangeMonthCallbackData(CallbackData, prefix='change_month'):
    increase: bool
    year: int
    month: int


class SelectMonthCallbackData(CallbackData, prefix='select_month'):
    year: int


class ChangeYearCallbackData(CallbackData, prefix='change_year'):
    increase: bool
    year: int
