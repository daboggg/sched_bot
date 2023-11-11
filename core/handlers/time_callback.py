import logging.config
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.keyboards.inline import kb_select_minute, kb_confirm_date_time
from core.utils.callbackdata import SelectHourCallbackData, SelectMinuteCallbackData
from core.utils.statesform import StepsDateTime
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('core.handlers.time_callback')

time_callback_router = Router()


# колбэк для выбора часа
@time_callback_router.callback_query(SelectHourCallbackData.filter())
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


# колбэк для выбора минуты
@time_callback_router.callback_query(SelectMinuteCallbackData.filter())
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



