from aiogram.filters.callback_data import CallbackData


class ChangeMonthCallbackData(CallbackData, prefix='change_month'):
    increase: bool
    year: int
    month: int


class SelectMonthCallbackData(CallbackData,prefix='select_month'):
    year: int


class ChangeYearCallbackData(CallbackData, prefix='change_year'):
    increase: bool
    year: int