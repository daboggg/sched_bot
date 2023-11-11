from aiogram.fsm.state import StatesGroup, State


class StepsDateTime(StatesGroup):
    GET_DATE = State()
    GET_HOUR = State()
    GET_MINUTE = State()
    GET_TEXT = State()
    CONFIRM_DATETIME = State()