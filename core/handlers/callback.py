from aiogram.types import CallbackQuery
import logging.config
from core.keyboards.inline import kb_get_calendar, kb_select_month
from core.utils.callbackdata import ChangeMonthCallbackData, SelectMonthCallbackData, ChangeYearCallbackData
from datetime import date
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('core.handlers.callback')


# колбэк без исполнения
async def cb_empty(callback: CallbackQuery) -> None:
    await callback.answer()
    logger.info('empty callback')


# колбэк для смены месяца (+1 или -1 месяц)
async def cb_change_month(callback: CallbackQuery, callback_data: ChangeMonthCallbackData) -> None:
    today = date.today()
    calculated_month = callback_data.month

    if callback_data.increase:
        if callback_data.month in range(1, 12):
            calculated_month += 1
    else:
        if callback_data.year == today.year:
            if callback_data.month in range(today.month + 1, 13):
                calculated_month -= 1
        else:
            if callback_data.month in range(2, 13):
                calculated_month -= 1

    if calculated_month != callback_data.month:
        await callback.message.edit_reply_markup(
            reply_markup=kb_get_calendar(date(callback_data.year, calculated_month, 1)))
    await callback.answer()
    logger.info(f'смена месяца: {callback_data}')


# колбэк для выбора месяца
async def cb_select_month(callback: CallbackQuery, callback_data: SelectMonthCallbackData) -> None:
    await callback.message.edit_text("Введите месяц сигнала")
    await callback.message.edit_reply_markup(reply_markup=kb_select_month(callback_data.year))
    await callback.answer()
    logger.info(f'выбор месяца: {callback_data}')


# колбэк для смены года (+1 или -1 год)
async def cb_change_year(callback: CallbackQuery, callback_data: ChangeYearCallbackData) -> None:
    year = callback_data.year
    if callback_data.increase:
        await callback.message.edit_reply_markup(reply_markup=kb_select_month(year + 1))
    else:
        if year >= date.today().year + 1:
            await callback.message.edit_reply_markup(reply_markup=kb_select_month(year - 1))
    await callback.answer()
    logger.info(f'смена года: {callback_data}')
