import logging.config
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
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
async def cb_confirm_date_time(callback: CallbackQuery, state: FSMContext, ) -> None:
    context = await state.get_data()
    await callback.message.edit_text(f'подтверждено {context.get("year")}')
    await state.clear()
    logger.info('confirm datetime')
