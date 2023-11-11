import logging.config
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers.datetime_message import send_message_date
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('core.handlers.callback')

callback_router = Router()


# колбэк без исполнения
@callback_router.callback_query(F.data == 'empty')
async def cb_empty(callback: CallbackQuery) -> None:
    await callback.answer()
    logger.info('empty callback')


# колбэк для подтверждения ввода даты, времени
@callback_router.callback_query(F.data == 'сonfirm_datetime')
async def cb_confirm_date_time(callback: CallbackQuery, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler) -> None:
    context = await state.get_data()
    apscheduler.add_job(send_message_date, trigger='date', run_date=datetime(
        context.get('year'),
        context.get('month'),
        context.get('day'),
        context.get('hour'),
        context.get('minute'),
        0
    ),kwargs={'bot':bot, 'chat_id': callback.from_user.id, 'text': context.get('text')})
    await callback.message.edit_text(f'готово')
    await state.clear()
    logger.info('confirm datetime')
