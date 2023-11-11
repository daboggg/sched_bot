import logging.config
from datetime import date, datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.keyboards.inline import kb_get_calendar, kb_select_month, kb_select_year, kb_select_hour, kb_select_minute, \
    kb_confirm_date_time
from core.utils.app_data import months_of_year
from core.utils.callbackdata import *
from core.utils.statesform import StepsDateTime
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('core.handlers.date')

date_router = Router()


async def send_message_date(bot: Bot, chat_id: int, text: str) -> None:
    await bot.send_message(chat_id, text)


# колбэк без исполнения
@date_router.callback_query(F.data == 'empty')
async def cb_empty(callback: CallbackQuery) -> None:
    await callback.answer()
    logger.info('empty callback')


# выводит календарь для ввода даты
@date_router.message(Command(commands=['date']))
async def cmd_date(message: Message, state: FSMContext) -> None:
    await message.answer("Введите дату сигнала", reply_markup=kb_get_calendar(date.today()))
    await state.set_state(StepsDateTime.GET_DATE)


# Стартовое меню, выводит две кнопки: Интервал, Дата
@date_router.callback_query(F.data == 'cancel')
async def cb_get_start(callback: CallbackQuery) -> None:
    await callback.message.answer(
        f'Для получения сигнала через определенный интервал, выберите в меню <b>/interval</b>\n\n'
        f'Для получения сигнала в определенную дату/время, выберите в меню <b>/date</b>',
        parse_mode="HTML")
    await callback.answer()
    logger.info('get_start callback')


# выводит календарь для ввода даты
@date_router.callback_query(SelectDateCallbackData.filter())
async def cb_get_date(callback: CallbackQuery, callback_data: SelectDateCallbackData) -> None:
    await callback.message.edit_text("Введите дату сигнала")
    await callback.message.edit_reply_markup(
        reply_markup=kb_get_calendar(date(callback_data.year, callback_data.month, 1)))
    await callback.answer()


# смена месяца (+1 или -1 месяц)
@date_router.callback_query(ChangeMonthCallbackData.filter())
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


# выбор месяца
@date_router.callback_query(SelectMonthCallbackData.filter())
async def cb_select_month(callback: CallbackQuery, callback_data: SelectMonthCallbackData) -> None:
    await callback.message.edit_text("Введите месяц сигнала")
    await callback.message.edit_reply_markup(reply_markup=kb_select_month(callback_data.year))
    await callback.answer()
    logger.info(f'выбор месяца: {callback_data}')


#  смена года (+1 или -1 год)
@date_router.callback_query(ChangeYearCallbackData.filter())
async def cb_change_year(callback: CallbackQuery, callback_data: ChangeYearCallbackData) -> None:
    year = callback_data.year
    if callback_data.increase:
        await callback.message.edit_reply_markup(reply_markup=kb_select_month(year + 1))
    else:
        if year >= date.today().year + 1:
            await callback.message.edit_reply_markup(reply_markup=kb_select_month(year - 1))
    await callback.answer()
    logger.info(f'смена года: {callback_data}')


# выбор года
@date_router.callback_query(F.data == 'select_year')
async def cb_select_year(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Введите год сигнала")
    await callback.message.edit_reply_markup(reply_markup=kb_select_year())
    await callback.answer()
    logger.info(f'выбор года: {callback.data}')


# получает дату сигнала
@date_router.callback_query(ReadyDateCallbackData.filter())
async def cb_ready_date(callback: CallbackQuery, state: FSMContext, callback_data: ReadyDateCallbackData) -> None:
    await state.update_data(year=callback_data.year, month=callback_data.month, day=callback_data.day)
    await callback.message.edit_text(
        f"выбранная дата: {callback_data.year}-{months_of_year[callback_data.month - 1]}"
        f"-{callback_data.day}\nвыберите час...")
    await callback.message.edit_reply_markup(reply_markup=kb_select_hour())
    await callback.answer()
    await state.set_state(StepsDateTime.GET_HOUR)
    logger.info(f'выбрана дата: {callback.data}')


# выбор часа
@date_router.callback_query(SelectHourCallbackData.filter())
async def cb_select_hour(callback: CallbackQuery, state: FSMContext, callback_data: SelectHourCallbackData) -> None:
    await state.update_data(hour=callback_data.hour)
    context = await state.get_data()
    await callback.message.edit_text(
        f"выбранная дата: {context.get('year')}-"
        f"{context.get('month')}-{context.get('day')}\n"
        f"выбран час: {callback_data.hour}\nвыберите минуту...")
    await callback.message.edit_reply_markup(reply_markup=kb_select_minute())
    await callback.answer()
    await state.set_state(StepsDateTime.GET_MINUTE)
    logger.info(f'выбран час {callback_data}')


# выбор минуты
@date_router.callback_query(SelectMinuteCallbackData.filter())
async def cb_select_minute(callback: CallbackQuery, state: FSMContext, callback_data: SelectMinuteCallbackData) -> None:
    await state.update_data(minute=callback_data.minute)
    context = await state.get_data()
    await callback.message.edit_text(f"выбранная дата: {context.get('year')}-"
                                     f"{context.get('month')}-{context.get('day')}\n"
                                     f"выбранное время: {context.get('hour')}:{callback_data.minute}:00\n"
                                     f"введите текст...")
    await callback.answer()
    await state.set_state(StepsDateTime.GET_TEXT)
    logger.info(f'выбрана минута {callback_data}')


#  ввод текста
@date_router.message(StepsDateTime.GET_TEXT)
async def cb_get_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    context = await state.get_data()
    await message.answer(f"выбранная дата: {context.get('year')}-"
                         f"{context.get('month')}-{context.get('day')}\n"
                         f"выбранное время: {context.get('hour')}:{context.get('minute')}:00\n"
                         f"набранный текст: {message.text}\n"
                         f"подтвердите ввод",
                         reply_markup=kb_confirm_date_time())
    await state.set_state(StepsDateTime.CONFIRM_DATETIME)
    logger.info(f'набран текст: {message.text}')


# колбэк для подтверждения ввода даты, времени
@date_router.callback_query(F.data == 'сonfirm_datetime')
async def cb_confirm_date_time(callback: CallbackQuery, bot: Bot, state: FSMContext,
                               apscheduler: AsyncIOScheduler) -> None:
    context = await state.get_data()
    apscheduler.add_job(send_message_date, trigger='date', run_date=datetime(
        context.get('year'),
        context.get('month'),
        context.get('day'),
        context.get('hour'),
        context.get('minute'),
        0
    ), kwargs={'bot': bot, 'chat_id': callback.from_user.id, 'text': context.get('text')})
    await callback.message.edit_text(f'готово')
    await state.clear()
    logger.info('confirm datetime')
