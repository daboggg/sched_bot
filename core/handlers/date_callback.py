from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import logging.config
from core.keyboards.inline import kb_get_calendar, kb_select_month, kb_select_year, kb_select_hour
from core.utils.app_data import months_of_year
from core.utils.callbackdata import *
from datetime import date

from core.utils.statesform import StepsDateTime
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('core.handlers.date_callback')

date_callback_router = Router()


# Стартовое меню, выводит две кнопки: Интервал, Дата
@date_callback_router.callback_query(F.data == 'cancel')
async def cb_get_start(callback: CallbackQuery, state: FSMContext) -> None:
    # await state.clear()
    await callback.message.answer(
        f'Для получения сигнала через определенный интервал, выберите в меню <b>/interval</b>\n\n'
        f'Для получения сигнала в определенную дату/время, выберите в меню <b>/date</b>',
        parse_mode="HTML")
    await callback.answer()
    logger.info('get_start callback')


# выводит календарь для ввода даты
@date_callback_router.callback_query(SelectDateCallbackData.filter())
async def cb_get_date(callback: CallbackQuery, callback_data: SelectDateCallbackData) -> None:
    await callback.message.edit_text("Введите дату сигнала")
    await callback.message.edit_reply_markup(
        reply_markup=kb_get_calendar(date(callback_data.year, callback_data.month, 1)))
    await callback.answer()


# колбэк для смены месяца (+1 или -1 месяц)
@date_callback_router.callback_query(ChangeMonthCallbackData.filter())
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
@date_callback_router.callback_query(SelectMonthCallbackData.filter())
async def cb_select_month(callback: CallbackQuery, callback_data: SelectMonthCallbackData) -> None:
    await callback.message.edit_text("Введите месяц сигнала")
    await callback.message.edit_reply_markup(reply_markup=kb_select_month(callback_data.year))
    await callback.answer()
    logger.info(f'выбор месяца: {callback_data}')


# колбэк для смены года (+1 или -1 год)
@date_callback_router.callback_query(ChangeYearCallbackData.filter())
async def cb_change_year(callback: CallbackQuery, callback_data: ChangeYearCallbackData) -> None:
    year = callback_data.year
    if callback_data.increase:
        await callback.message.edit_reply_markup(reply_markup=kb_select_month(year + 1))
    else:
        if year >= date.today().year + 1:
            await callback.message.edit_reply_markup(reply_markup=kb_select_month(year - 1))
    await callback.answer()
    logger.info(f'смена года: {callback_data}')


# колбэк для выбора года
@date_callback_router.callback_query(F.data == 'select_year')
async def cb_select_year(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Введите год сигнала")
    await callback.message.edit_reply_markup(reply_markup=kb_select_year())
    await callback.answer()
    logger.info(f'выбор года: {callback.data}')


# колбэк получает дату сигнала
@date_callback_router.callback_query(ReadyDateCallbackData.filter())
async def cb_ready_date(callback: CallbackQuery, state: FSMContext, callback_data: ReadyDateCallbackData) -> None:
    await state.update_data(year=callback_data.year, month=callback_data.month,day=callback_data.day)
    await callback.message.edit_text(f"выбранная дата: {callback_data.year}-{months_of_year[callback_data.month-1]}-{callback_data.day}\nвыберите час...")
    await callback.message.edit_reply_markup(reply_markup=kb_select_hour())
    await callback.answer()
    await state.set_state(StepsDateTime.GET_HOUR)
    logger.info(f'выбрана дата: {callback.data}')

